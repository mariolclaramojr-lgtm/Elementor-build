<?php
defined( 'ABSPATH' ) || exit;

/**
 * Pulls videos from YouTube on a schedule and creates/updates Message posts.
 */
class YTM_Importer {

	const CRON_HOOK = 'ytm_sync';

	public static function init() {
		add_filter( 'cron_schedules', array( __CLASS__, 'cron_schedules' ) );
		add_action( self::CRON_HOOK, array( __CLASS__, 'cron' ) );
		add_action( 'init', array( __CLASS__, 'schedule' ), 20 );
	}

	public static function cron_schedules( $schedules ) {
		$schedules['ytm_15min'] = array( 'interval' => 15 * MINUTE_IN_SECONDS, 'display' => __( 'Every 15 minutes', 'youtube-messages' ) );
		$schedules['ytm_30min'] = array( 'interval' => 30 * MINUTE_IN_SECONDS, 'display' => __( 'Every 30 minutes', 'youtube-messages' ) );
		return $schedules;
	}

	public static function schedule() {
		if ( ! wp_next_scheduled( self::CRON_HOOK ) ) {
			wp_schedule_event( time() + 60, YTM_Settings::get( 'interval' ), self::CRON_HOOK );
		}
	}

	public static function cron() {
		if ( '' !== YTM_Settings::get( 'channel' ) ) {
			self::sync( false );
		}
	}

	/**
	 * Run an import.
	 *
	 * @param bool $full true = walk the whole channel history (needs an API key), false = newest videos only.
	 * @return array summary (also saved to the ytm_last_sync option)
	 */
	public static function sync( $full = false ) {
		$summary = array(
			'time'    => time(),
			'mode'    => $full ? 'full' : 'latest',
			'source'  => '',
			'created' => 0,
			'updated' => 0,
			'skipped' => 0,
			'errors'  => array(),
		);

		if ( get_transient( 'ytm_sync_lock' ) ) {
			$summary['errors'][] = __( 'Another import is already running. Try again in a few minutes.', 'youtube-messages' );
			return $summary;
		}
		set_transient( 'ytm_sync_lock', 1, 10 * MINUTE_IN_SECONDS );
		if ( function_exists( 'set_time_limit' ) ) {
			@set_time_limit( $full ? 900 : 300 ); // phpcs:ignore WordPress.PHP.NoSilencedErrors
		}

		try {
			$summary = self::run( $full, $summary );
		} catch ( Throwable $e ) {
			$summary['errors'][] = $e->getMessage();
		}

		delete_transient( 'ytm_sync_lock' );
		update_option( 'ytm_last_sync', $summary, false );
		return $summary;
	}

	private static function run( $full, array $summary ) {
		$yt      = new YTM_YouTube( YTM_Settings::get( 'api_key' ) );
		$channel = self::channel( $yt );
		if ( is_wp_error( $channel ) ) {
			$summary['errors'][] = $channel->get_error_message();
			return $summary;
		}

		$videos = array(); // id => normalised video
		$series = array(); // id => [ series names ]

		if ( $yt->has_key() ) {
			$summary['source'] = 'api';
			$ids               = self::api_playlist_ids( $yt, YTM_YouTube::uploads_playlist( $channel['id'] ), $full, $summary );

			$titles = (array) get_option( 'ytm_playlist_titles', array() );
			foreach ( YTM_Settings::playlist_ids() as $pl ) {
				if ( empty( $titles[ $pl ] ) ) {
					$t = $yt->playlist_title( $pl );
					if ( is_wp_error( $t ) || '' === $t ) {
						$summary['errors'][] = is_wp_error( $t ) ? $t->get_error_message() : sprintf( __( 'Playlist %s not found.', 'youtube-messages' ), $pl );
						continue;
					}
					$titles[ $pl ] = $t;
				}
				foreach ( self::api_playlist_ids( $yt, $pl, $full, $summary ) as $id ) {
					$series[ $id ][] = $titles[ $pl ];
					$ids[]           = $id;
				}
			}
			update_option( 'ytm_playlist_titles', $titles, false );

			// Only ask for details we need: new videos, or all of them when keeping titles up to date.
			$ids = array_values( array_unique( $ids ) );
			if ( ! YTM_Settings::get( 'update_existing' ) ) {
				$existing = self::existing_map();
				$ids      = array_values( array_filter( $ids, function ( $id ) use ( $existing ) {
					return ! isset( $existing[ $id ] );
				} ) );
			}
			$details = $yt->videos( $ids );
			if ( is_wp_error( $details ) ) {
				$summary['errors'][] = $details->get_error_message();
				$details             = array();
			}
			foreach ( $details as $v ) {
				$videos[ $v['id'] ] = $v;
			}
		} else {
			$summary['source'] = 'rss';
			if ( $full ) {
				$summary['errors'][] = __( 'Without an API key YouTube only shares the newest 15 videos. Add an API key to import the full archive.', 'youtube-messages' );
			}
			$feed = $yt->feed( 'channel_id', $channel['id'] );
			if ( is_wp_error( $feed ) ) {
				$summary['errors'][] = $feed->get_error_message();
			} else {
				foreach ( $feed['videos'] as $v ) {
					$videos[ $v['id'] ] = $v;
				}
			}
			foreach ( YTM_Settings::playlist_ids() as $pl ) {
				$feed = $yt->feed( 'playlist_id', $pl );
				if ( is_wp_error( $feed ) ) {
					$summary['errors'][] = $feed->get_error_message();
					continue;
				}
				foreach ( $feed['videos'] as $v ) {
					$series[ $v['id'] ][] = $feed['title'];
					if ( ! isset( $videos[ $v['id'] ] ) ) {
						$videos[ $v['id'] ] = $v;
					}
				}
			}
		}

		$existing = self::existing_map();
		$ignored  = (array) get_option( 'ytm_ignored', array() );

		// Oldest first, so posts are created in the same order they were published.
		uasort( $videos, function ( $a, $b ) {
			return $a['published'] <=> $b['published'];
		} );

		foreach ( $videos as $id => $video ) {
			if ( isset( $ignored[ $id ] ) ) {
				continue;
			}
			$post_id = $existing[ $id ] ?? 0;
			if ( ! $post_id && ! self::wanted( $video ) ) {
				++$summary['skipped'];
				continue;
			}
			$result = self::save( $video, $post_id, $series[ $id ] ?? array() );
			if ( is_wp_error( $result ) ) {
				$summary['errors'][] = $result->get_error_message();
			} elseif ( 'created' === $result ) {
				++$summary['created'];
			} elseif ( 'updated' === $result ) {
				++$summary['updated'];
			}
		}

		// Videos that only had series info this run (already imported, details not refetched).
		foreach ( $series as $id => $names ) {
			if ( ! isset( $videos[ $id ] ) && isset( $existing[ $id ] ) ) {
				wp_set_object_terms( $existing[ $id ], $names, YTM_Post_Type::SERIES, true );
			}
		}

		if ( YTM_Settings::get( 'featured_images' ) ) {
			self::attach_featured_images( $full ? 50 : 10 );
		}

		return $summary;
	}

	/** Resolve (and cache) the channel the admin entered. */
	private static function channel( YTM_YouTube $yt ) {
		$input  = YTM_Settings::get( 'channel' );
		$cached = get_option( 'ytm_channel' );
		if ( is_array( $cached ) && ( $cached['input'] ?? '' ) === $input && ! empty( $cached['id'] ) ) {
			return $cached;
		}
		$channel = $yt->resolve_channel( $input );
		if ( ! is_wp_error( $channel ) ) {
			$channel['input'] = $input;
			update_option( 'ytm_channel', $channel, false );
		}
		return $channel;
	}

	private static function api_playlist_ids( YTM_YouTube $yt, $playlist_id, $full, array &$summary ) {
		$ids   = array();
		$token = '';
		$pages = 0;
		do {
			$page = $yt->playlist_page( $playlist_id, $token );
			if ( is_wp_error( $page ) ) {
				$summary['errors'][] = $page->get_error_message();
				break;
			}
			$ids   = array_merge( $ids, $page['ids'] );
			$token = $page['next'];
			++$pages;
		} while ( $full && $token && $pages < 200 );
		return $ids;
	}

	/** Should a not-yet-imported video be imported? */
	private static function wanted( array &$video ) {
		if ( 'upcoming' === $video['live'] && YTM_Settings::get( 'skip_upcoming' ) ) {
			return false;
		}

		$title   = strtolower( $video['title'] );
		$include = YTM_Settings::keywords( 'include_keywords' );
		if ( $include ) {
			$hit = false;
			foreach ( $include as $word ) {
				if ( false !== strpos( $title, $word ) ) {
					$hit = true;
					break;
				}
			}
			if ( ! $hit ) {
				return false;
			}
		}
		foreach ( YTM_Settings::keywords( 'exclude_keywords' ) as $word ) {
			if ( false !== strpos( $title, $word ) ) {
				return false;
			}
		}

		if ( YTM_Settings::get( 'skip_shorts' ) ) {
			if ( null === $video['short'] ) {
				// Shorts are at most 3 minutes; only ask YouTube about videos that short.
				$video['short'] = ( $video['duration'] > 0 && $video['duration'] <= 180 ) ? self::cached_is_short( $video['id'], $video['duration'] ) : false;
			}
			if ( $video['short'] ) {
				return false;
			}
		}
		return true;
	}

	private static function cached_is_short( $id, $duration ) {
		$cache = (array) get_option( 'ytm_shorts_cache', array() );
		if ( isset( $cache[ $id ] ) ) {
			return (bool) $cache[ $id ];
		}
		$short = YTM_YouTube::is_short( $id );
		if ( null === $short ) {
			return $duration <= 60; // Couldn't ask YouTube: treat a minute or less as a Short.
		}
		$cache[ $id ] = $short ? 1 : 0;
		if ( count( $cache ) > 3000 ) {
			$cache = array_slice( $cache, -2000, null, true );
		}
		update_option( 'ytm_shorts_cache', $cache, false );
		return $short;
	}

	/** video ID => post ID for every imported message, whatever its status (draft, trash…). */
	public static function existing_map() {
		global $wpdb;
		$rows = $wpdb->get_results( $wpdb->prepare(
			"SELECT pm.meta_value AS vid, pm.post_id AS pid FROM {$wpdb->postmeta} pm
			 INNER JOIN {$wpdb->posts} p ON p.ID = pm.post_id
			 WHERE pm.meta_key = '_ytm_video_id' AND p.post_type = %s",
			YTM_Post_Type::POST_TYPE
		) );
		$map = array();
		foreach ( $rows as $row ) {
			$map[ $row->vid ] = (int) $row->pid;
		}
		return $map;
	}

	/**
	 * Create or update one message.
	 *
	 * @return string|WP_Error 'created', 'updated' or 'unchanged'
	 */
	private static function save( array $video, $post_id, array $series ) {
		$title   = wp_strip_all_tags( $video['title'] );
		$content = trim( $video['description'] );
		$gmt     = gmdate( 'Y-m-d H:i:s', $video['published'] ? $video['published'] : time() );

		if ( ! $post_id ) {
			$post_id = wp_insert_post( wp_slash( array(
				'post_type'     => YTM_Post_Type::POST_TYPE,
				'post_status'   => 'publish',
				'post_title'    => $title,
				'post_content'  => $content,
				'post_date_gmt' => $gmt,
				'post_date'     => get_date_from_gmt( $gmt ),
				'post_author'   => self::author_id(),
			) ), true );
			if ( is_wp_error( $post_id ) ) {
				return $post_id;
			}
			update_post_meta( $post_id, '_ytm_video_id', $video['id'] );
			update_post_meta( $post_id, '_ytm_synced_title', $title );
			update_post_meta( $post_id, '_ytm_synced_content', md5( $content ) );
			self::save_meta( $post_id, $video );
			self::assign_type( $post_id, $title );
			if ( $series ) {
				wp_set_object_terms( $post_id, $series, YTM_Post_Type::SERIES, true );
			}
			return 'created';
		}

		$changed = self::save_meta( $post_id, $video );
		if ( $series ) {
			wp_set_object_terms( $post_id, $series, YTM_Post_Type::SERIES, true );
		}
		if ( ! YTM_Settings::get( 'update_existing' ) ) {
			return $changed ? 'updated' : 'unchanged';
		}

		// Follow YouTube edits, but never overwrite a title/description someone changed in WordPress.
		$post   = get_post( $post_id );
		$update = array();
		if ( $title !== $post->post_title && get_post_meta( $post_id, '_ytm_synced_title', true ) === $post->post_title ) {
			$update['post_title'] = $title;
		}
		if ( md5( $content ) !== md5( $post->post_content ) && get_post_meta( $post_id, '_ytm_synced_content', true ) === md5( $post->post_content ) ) {
			$update['post_content'] = $content;
		}
		if ( $update ) {
			$update['ID'] = $post_id;
			$res          = wp_update_post( wp_slash( $update ), true );
			if ( is_wp_error( $res ) ) {
				return $res;
			}
			// Store what WordPress actually saved (content filters may alter it).
			$post = get_post( $post_id );
			update_post_meta( $post_id, '_ytm_synced_title', $post->post_title );
			update_post_meta( $post_id, '_ytm_synced_content', md5( $post->post_content ) );
			$changed = true;
		}
		return $changed ? 'updated' : 'unchanged';
	}

	/** @return bool whether anything changed */
	private static function save_meta( $post_id, array $video ) {
		$changed = false;
		$meta    = array( '_ytm_thumb' => $video['thumb'], '_ytm_live' => $video['live'] );
		if ( $video['duration'] ) {
			$meta['_ytm_duration'] = (int) $video['duration'];
		}
		foreach ( $meta as $key => $value ) {
			if ( (string) get_post_meta( $post_id, $key, true ) !== (string) $value ) {
				update_post_meta( $post_id, $key, $value );
				$changed = true;
			}
		}
		return $changed;
	}

	private static function assign_type( $post_id, $title ) {
		$type  = '';
		$lower = strtolower( $title );
		foreach ( YTM_Settings::type_rules() as $rule ) {
			if ( false !== strpos( $lower, strtolower( $rule[0] ) ) ) {
				$type = $rule[1];
				break;
			}
		}
		if ( '' === $type ) {
			$type = YTM_Settings::get( 'default_type' );
		}
		if ( '' !== $type ) {
			wp_set_object_terms( $post_id, $type, YTM_Post_Type::TYPE, false );
		}
	}

	private static function author_id() {
		$admins = get_users( array( 'role' => 'administrator', 'number' => 1, 'fields' => 'ID' ) );
		return $admins ? (int) $admins[0] : 0;
	}

	/** Copy YouTube thumbnails into the Media Library as featured images, a few per run. */
	private static function attach_featured_images( $limit ) {
		require_once ABSPATH . 'wp-admin/includes/media.php';
		require_once ABSPATH . 'wp-admin/includes/file.php';
		require_once ABSPATH . 'wp-admin/includes/image.php';

		$posts = get_posts( array(
			'post_type'      => YTM_Post_Type::POST_TYPE,
			'post_status'    => 'publish',
			'posts_per_page' => $limit,
			'fields'         => 'ids',
			'meta_query'     => array( // phpcs:ignore WordPress.DB.SlowDBQuery
				array( 'key' => '_thumbnail_id', 'compare' => 'NOT EXISTS' ),
				array( 'key' => '_ytm_thumb_failed', 'compare' => 'NOT EXISTS' ),
			),
		) );
		foreach ( $posts as $post_id ) {
			$url = get_post_meta( $post_id, '_ytm_thumb', true );
			$att = $url ? media_sideload_image( $url, $post_id, get_the_title( $post_id ), 'id' ) : new WP_Error( 'none', '' );
			if ( is_wp_error( $att ) ) {
				update_post_meta( $post_id, '_ytm_thumb_failed', 1 );
			} else {
				set_post_thumbnail( $post_id, $att );
			}
		}
	}
}
