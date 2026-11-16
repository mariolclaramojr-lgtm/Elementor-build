<?php
defined( 'ABSPATH' ) || exit;

/**
 * The "Message" post type that holds imported videos, plus Series and Type taxonomies.
 * Messages have no front-end page of their own: cards link straight to YouTube.
 */
class YTM_Post_Type {

	const POST_TYPE = 'ytm_message';
	const SERIES    = 'ytm_series';
	const TYPE      = 'ytm_type';

	public static function init() {
		add_action( 'init', array( __CLASS__, 'register' ) );
		add_filter( 'post_type_link', array( __CLASS__, 'permalink' ), 10, 2 );
		add_filter( 'manage_' . self::POST_TYPE . '_posts_columns', array( __CLASS__, 'columns' ) );
		add_action( 'manage_' . self::POST_TYPE . '_posts_custom_column', array( __CLASS__, 'column' ), 10, 2 );
		add_action( 'before_delete_post', array( __CLASS__, 'remember_deleted' ) );
	}

	public static function register() {
		register_post_type( self::POST_TYPE, array(
			'labels'              => array(
				'name'               => __( 'Messages', 'youtube-messages' ),
				'singular_name'      => __( 'Message', 'youtube-messages' ),
				'all_items'          => __( 'All Messages', 'youtube-messages' ),
				'edit_item'          => __( 'Edit Message', 'youtube-messages' ),
				'search_items'       => __( 'Search Messages', 'youtube-messages' ),
				'not_found'          => __( 'No messages imported yet.', 'youtube-messages' ),
				'not_found_in_trash' => __( 'No messages in Trash.', 'youtube-messages' ),
			),
			'public'              => true,
			'publicly_queryable'  => false, // Cards open YouTube; no thin single pages.
			'exclude_from_search' => true,
			'has_archive'         => false,
			'rewrite'             => false,
			'show_in_rest'        => true,
			'menu_icon'           => 'dashicons-video-alt3',
			'menu_position'       => 21,
			'supports'            => array( 'title', 'editor', 'thumbnail', 'custom-fields' ),
			'capability_type'     => 'post',
			'map_meta_cap'        => true,
			'capabilities'        => array( 'create_posts' => 'do_not_allow' ), // Added by the importer only.
		) );

		register_taxonomy( self::SERIES, self::POST_TYPE, array(
			'labels'            => array(
				'name'          => __( 'Series', 'youtube-messages' ),
				'singular_name' => __( 'Series', 'youtube-messages' ),
			),
			'public'            => true,
			'publicly_queryable' => false,
			'rewrite'           => false,
			'hierarchical'      => false,
			'show_admin_column' => true,
			'show_in_rest'      => true,
		) );

		register_taxonomy( self::TYPE, self::POST_TYPE, array(
			'labels'            => array(
				'name'          => __( 'Service Types', 'youtube-messages' ),
				'singular_name' => __( 'Service Type', 'youtube-messages' ),
			),
			'public'            => true,
			'publicly_queryable' => false,
			'rewrite'           => false,
			'hierarchical'      => false,
			'show_admin_column' => true,
			'show_in_rest'      => true,
		) );
	}

	/** Anywhere WordPress (or a page builder loop) asks for a message's link, give the YouTube URL. */
	public static function permalink( $url, $post ) {
		if ( self::POST_TYPE === $post->post_type ) {
			$video = get_post_meta( $post->ID, '_ytm_video_id', true );
			if ( $video ) {
				return self::watch_url( $video );
			}
		}
		return $url;
	}

	public static function watch_url( $video_id ) {
		return 'https://www.youtube.com/watch?v=' . rawurlencode( $video_id );
	}

	/** Best thumbnail URL for a message (featured image if set, otherwise YouTube's). */
	public static function thumbnail_url( $post_id ) {
		if ( has_post_thumbnail( $post_id ) ) {
			$src = wp_get_attachment_image_url( get_post_thumbnail_id( $post_id ), 'large' );
			if ( $src ) {
				return $src;
			}
		}
		$thumb = get_post_meta( $post_id, '_ytm_thumb', true );
		if ( $thumb ) {
			return $thumb;
		}
		return 'https://i.ytimg.com/vi/' . rawurlencode( get_post_meta( $post_id, '_ytm_video_id', true ) ) . '/hqdefault.jpg';
	}

	public static function format_duration( $seconds ) {
		$seconds = (int) $seconds;
		if ( $seconds <= 0 ) {
			return '';
		}
		$h = intdiv( $seconds, 3600 );
		$m = intdiv( $seconds % 3600, 60 );
		$s = $seconds % 60;
		return $h ? sprintf( '%d:%02d:%02d', $h, $m, $s ) : sprintf( '%d:%02d', $m, $s );
	}

	public static function columns( $cols ) {
		$new = array();
		foreach ( $cols as $key => $label ) {
			if ( 'title' === $key ) {
				$new['ytm_thumb'] = '';
			}
			$new[ $key ] = $label;
			if ( 'title' === $key ) {
				$new['ytm_video'] = __( 'YouTube', 'youtube-messages' );
			}
		}
		return $new;
	}

	public static function column( $col, $post_id ) {
		if ( 'ytm_thumb' === $col ) {
			printf( '<img src="%s" alt="" style="width:96px;height:54px;object-fit:cover;border-radius:3px" loading="lazy">', esc_url( self::thumbnail_url( $post_id ) ) );
		} elseif ( 'ytm_video' === $col ) {
			$id = get_post_meta( $post_id, '_ytm_video_id', true );
			if ( $id ) {
				$dur = self::format_duration( get_post_meta( $post_id, '_ytm_duration', true ) );
				printf( '<a href="%s" target="_blank" rel="noopener">%s</a>%s', esc_url( self::watch_url( $id ) ), esc_html__( 'Watch', 'youtube-messages' ), $dur ? ' &middot; ' . esc_html( $dur ) : '' );
			}
		}
	}

	/** A message deleted for good stays deleted: never re-import that video. */
	public static function remember_deleted( $post_id ) {
		if ( self::POST_TYPE !== get_post_type( $post_id ) ) {
			return;
		}
		$id = get_post_meta( $post_id, '_ytm_video_id', true );
		if ( $id ) {
			$ignored        = (array) get_option( 'ytm_ignored', array() );
			$ignored[ $id ] = 1;
			update_option( 'ytm_ignored', $ignored, false );
		}
	}
}
