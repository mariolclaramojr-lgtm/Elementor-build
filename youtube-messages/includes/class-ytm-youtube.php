<?php
defined( 'ABSPATH' ) || exit;

/**
 * Talks to YouTube. Uses the YouTube Data API v3 when an API key is set (full archive,
 * durations, live/upcoming status) and the public RSS feeds (latest 15 videos) otherwise.
 *
 * Every video comes back in one normalised shape:
 *   id, title, description, published (UTC timestamp), thumb, duration (seconds, 0 = unknown),
 *   live ('none' | 'live' | 'upcoming'), short (true | false | null = unknown)
 */
class YTM_YouTube {

	const API = 'https://www.googleapis.com/youtube/v3/';

	private $key;

	public function __construct( $api_key = '' ) {
		$this->key = (string) $api_key;
	}

	public function has_key() {
		return '' !== $this->key;
	}

	/* ------------------------------------------------------------------ Channel */

	/**
	 * Turn whatever the admin typed (channel ID, @handle, or any channel URL) into a channel ID.
	 *
	 * @return array|WP_Error [ 'id' => 'UC…', 'title' => '…' ]
	 */
	public function resolve_channel( $input ) {
		$input = trim( (string) $input );
		if ( '' === $input ) {
			return new WP_Error( 'ytm_no_channel', __( 'Enter your YouTube channel in the settings.', 'youtube-messages' ) );
		}

		$id     = '';
		$handle = '';
		$user   = '';
		if ( preg_match( '/(UC[A-Za-z0-9_\-]{22})/', $input, $m ) ) {
			$id = $m[1];
		} elseif ( preg_match( '#(?:youtube\.com/)?(@[A-Za-z0-9._\-]+)#', $input, $m ) ) {
			$handle = $m[1];
		} elseif ( preg_match( '#youtube\.com/user/([A-Za-z0-9_\-]+)#', $input, $m ) ) {
			$user = $m[1];
		} elseif ( preg_match( '/^[A-Za-z0-9._\-]+$/', $input ) ) {
			$handle = '@' . $input;
		}

		if ( $this->has_key() ) {
			$params = array( 'part' => 'snippet' );
			if ( $id ) {
				$params['id'] = $id;
			} elseif ( $handle ) {
				$params['forHandle'] = $handle;
			} elseif ( $user ) {
				$params['forUsername'] = $user;
			}
			if ( count( $params ) > 1 ) {
				$data = $this->api( 'channels', $params );
				if ( is_wp_error( $data ) ) {
					return $data;
				}
				if ( ! empty( $data['items'][0]['id'] ) ) {
					return array(
						'id'    => $data['items'][0]['id'],
						'title' => $data['items'][0]['snippet']['title'] ?? '',
					);
				}
			}
		} elseif ( $id ) {
			return array( 'id' => $id, 'title' => '' );
		}

		// No key (or the API didn't know it): read the channel page's canonical link.
		$url = $id ? 'https://www.youtube.com/channel/' . $id
			: ( $handle ? 'https://www.youtube.com/' . $handle
			: ( $user ? 'https://www.youtube.com/user/' . $user : esc_url_raw( $input ) ) );
		$res = wp_remote_get( $url, array(
			'timeout'    => 20,
			'user-agent' => 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36',
			'headers'    => array( 'Accept-Language' => 'en-US,en;q=0.8', 'Cookie' => 'CONSENT=YES+1' ),
		) );
		if ( ! is_wp_error( $res ) ) {
			$html = wp_remote_retrieve_body( $res );
			if ( preg_match( '#<link rel="canonical" href="https://www\.youtube\.com/channel/(UC[A-Za-z0-9_\-]{22})"#', $html, $m )
				|| preg_match( '#"externalId":"(UC[A-Za-z0-9_\-]{22})"#', $html, $m ) ) {
				$title = '';
				if ( preg_match( '#<meta property="og:title" content="([^"]*)"#', $html, $t ) ) {
					$title = html_entity_decode( $t[1], ENT_QUOTES, 'UTF-8' );
				}
				return array( 'id' => $m[1], 'title' => $title );
			}
		}
		return new WP_Error( 'ytm_channel_not_found', sprintf(
			/* translators: %s: what the admin typed */
			__( 'Could not find the YouTube channel "%s". Paste the channel URL or its ID (starts with UC).', 'youtube-messages' ),
			$input
		) );
	}

	/** Every channel has an "uploads" playlist: UC… → UU…. */
	public static function uploads_playlist( $channel_id ) {
		return 'UU' . substr( $channel_id, 2 );
	}

	/* ------------------------------------------------------------------ Data API */

	private function api( $endpoint, array $params ) {
		$params['key'] = $this->key;
		$res           = wp_remote_get( self::API . $endpoint . '?' . http_build_query( $params ), array(
			'timeout' => 20,
			'headers' => array( 'Referer' => home_url( '/' ) ), // Lets keys restricted to the site's domain work.
		) );
		if ( is_wp_error( $res ) ) {
			return $res;
		}
		$code = wp_remote_retrieve_response_code( $res );
		$data = json_decode( wp_remote_retrieve_body( $res ), true );
		if ( 200 !== $code ) {
			$msg = $data['error']['message'] ?? 'HTTP ' . $code;
			return new WP_Error( 'ytm_api', sprintf( __( 'YouTube API error: %s', 'youtube-messages' ), wp_strip_all_tags( $msg ) ) );
		}
		return is_array( $data ) ? $data : new WP_Error( 'ytm_api', __( 'YouTube API returned an unreadable response.', 'youtube-messages' ) );
	}

	/**
	 * One page (up to 50) of video IDs from a playlist.
	 *
	 * @return array|WP_Error [ 'ids' => [], 'next' => page token or '' ]
	 */
	public function playlist_page( $playlist_id, $page_token = '' ) {
		$params = array( 'part' => 'contentDetails', 'playlistId' => $playlist_id, 'maxResults' => 50 );
		if ( $page_token ) {
			$params['pageToken'] = $page_token;
		}
		$data = $this->api( 'playlistItems', $params );
		if ( is_wp_error( $data ) ) {
			return $data;
		}
		$ids = array();
		foreach ( (array) ( $data['items'] ?? array() ) as $item ) {
			if ( ! empty( $item['contentDetails']['videoId'] ) ) {
				$ids[] = $item['contentDetails']['videoId'];
			}
		}
		return array( 'ids' => $ids, 'next' => $data['nextPageToken'] ?? '' );
	}

	/** @return string|WP_Error */
	public function playlist_title( $playlist_id ) {
		$data = $this->api( 'playlists', array( 'part' => 'snippet', 'id' => $playlist_id ) );
		if ( is_wp_error( $data ) ) {
			return $data;
		}
		return $data['items'][0]['snippet']['title'] ?? '';
	}

	/**
	 * Full details for up to 50 videos. Private/deleted videos are left out.
	 *
	 * @return array|WP_Error list of normalised videos
	 */
	public function videos( array $ids ) {
		$out = array();
		foreach ( array_chunk( array_values( array_unique( $ids ) ), 50 ) as $chunk ) {
			$data = $this->api( 'videos', array(
				'part' => 'snippet,contentDetails,status,liveStreamingDetails',
				'id'   => implode( ',', $chunk ),
			) );
			if ( is_wp_error( $data ) ) {
				return $data;
			}
			foreach ( (array) ( $data['items'] ?? array() ) as $item ) {
				if ( 'public' !== ( $item['status']['privacyStatus'] ?? '' ) ) {
					continue;
				}
				$sn     = $item['snippet'];
				$thumbs = $sn['thumbnails'] ?? array();
				$thumb  = '';
				foreach ( array( 'maxres', 'high', 'standard', 'medium', 'default' ) as $size ) {
					if ( ! empty( $thumbs[ $size ]['url'] ) ) {
						$thumb = $thumbs[ $size ]['url'];
						break;
					}
				}
				$published = $item['liveStreamingDetails']['actualStartTime'] ?? $sn['publishedAt'];
				$out[]     = array(
					'id'          => $item['id'],
					'title'       => $sn['title'] ?? '',
					'description' => $sn['description'] ?? '',
					'published'   => strtotime( $published ),
					'thumb'       => $thumb,
					'duration'    => self::iso_duration( $item['contentDetails']['duration'] ?? '' ),
					'live'        => in_array( $sn['liveBroadcastContent'] ?? '', array( 'live', 'upcoming' ), true ) ? $sn['liveBroadcastContent'] : 'none',
					'short'       => null,
				);
			}
		}
		return $out;
	}

	public static function iso_duration( $iso ) {
		if ( ! preg_match( '/^P(?:(\d+)D)?(?:T(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?)?$/', (string) $iso, $m ) ) {
			return 0;
		}
		return ( (int) ( $m[1] ?? 0 ) ) * 86400 + ( (int) ( $m[2] ?? 0 ) ) * 3600 + ( (int) ( $m[3] ?? 0 ) ) * 60 + (int) ( $m[4] ?? 0 );
	}

	/* ------------------------------------------------------------------ RSS (no key) */

	/**
	 * Latest ~15 videos from a channel or playlist RSS feed.
	 *
	 * @param string $kind 'channel_id' or 'playlist_id'.
	 * @return array|WP_Error [ 'title' => feed title, 'videos' => [] ]
	 */
	public function feed( $kind, $id ) {
		$res = wp_remote_get( 'https://www.youtube.com/feeds/videos.xml?' . $kind . '=' . rawurlencode( $id ), array( 'timeout' => 20 ) );
		if ( is_wp_error( $res ) ) {
			return $res;
		}
		$code = wp_remote_retrieve_response_code( $res );
		if ( 200 !== $code ) {
			return new WP_Error( 'ytm_feed', sprintf(
				/* translators: %d: HTTP status */
				__( 'YouTube\'s RSS feed answered HTTP %d. YouTube\'s feeds are unreliable; add a free YouTube API key in the settings for dependable imports.', 'youtube-messages' ),
				$code
			) );
		}
		$prev = libxml_use_internal_errors( true );
		$xml  = simplexml_load_string( wp_remote_retrieve_body( $res ), 'SimpleXMLElement', LIBXML_NONET );
		libxml_use_internal_errors( $prev );
		if ( ! $xml ) {
			return new WP_Error( 'ytm_feed', __( 'YouTube\'s RSS feed could not be read.', 'youtube-messages' ) );
		}

		$videos = array();
		foreach ( $xml->entry as $entry ) {
			$yt    = $entry->children( 'http://www.youtube.com/xml/schemas/2015' );
			$media = $entry->children( 'http://search.yahoo.com/mrss/' );
			$id    = (string) $yt->videoId;
			if ( '' === $id ) {
				continue;
			}
			$link  = (string) $entry->link->attributes()->href;
			$group = $media->group;
			$thumb = '';
			$desc  = '';
			if ( $group ) {
				$desc = (string) $group->description;
				if ( $group->thumbnail ) {
					$thumb = (string) $group->thumbnail->attributes()->url;
				}
			}
			$videos[] = array(
				'id'          => $id,
				'title'       => (string) $entry->title,
				'description' => $desc,
				'published'   => strtotime( (string) $entry->published ),
				'thumb'       => $thumb ? $thumb : 'https://i.ytimg.com/vi/' . $id . '/hqdefault.jpg',
				'duration'    => 0,
				'live'        => 'none',
				'short'       => false !== strpos( $link, '/shorts/' ),
			);
		}
		return array( 'title' => (string) $xml->title, 'videos' => $videos );
	}

	/* ------------------------------------------------------------------ Shorts */

	/** youtube.com/shorts/ID answers 200 for a Short and redirects for a normal video. */
	public static function is_short( $video_id ) {
		$res = wp_remote_head( 'https://www.youtube.com/shorts/' . rawurlencode( $video_id ), array(
			'timeout'     => 10,
			'redirection' => 0,
			'user-agent'  => 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36',
		) );
		if ( is_wp_error( $res ) ) {
			return null;
		}
		return 200 === wp_remote_retrieve_response_code( $res );
	}
}
