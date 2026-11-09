<?php
/**
 * Expiring public preview links for drafts, so an agent (or a client) can view
 * an unpublished Cornerstone page without logging in.
 *
 * URL shape: /?page_id=123&pxe_preview=<token>  (or ?p=123 for posts)
 * Token + expiry live in post meta; revoked by generating a new one or expiry.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

class Pro_Extended_Preview {

	const META  = '_pxe_preview';
	const PARAM = 'pxe_preview';

	public static function init() {
		add_action( 'pre_get_posts', array( __CLASS__, 'pre_get_posts' ) );
	}

	/** Create (or replace) a preview token. Returns the URL. */
	public static function create( $post_id, $hours ) {
		$token = wp_generate_password( 24, false );
		update_post_meta(
			$post_id,
			self::META,
			array(
				'token'   => $token,
				'expires' => time() + max( 1, (int) $hours ) * HOUR_IN_SECONDS,
			)
		);
		$post = get_post( $post_id );
		$key  = 'page' === $post->post_type ? 'page_id' : 'p';
		$args = array(
			$key        => $post_id,
			self::PARAM => $token,
		);
		if ( ! in_array( $post->post_type, array( 'page', 'post' ), true ) ) {
			$args['post_type'] = $post->post_type;
		}
		return add_query_arg( $args, home_url( '/' ) );
	}

	private static function valid( $post_id, $token ) {
		$m = get_post_meta( $post_id, self::META, true );
		return is_array( $m ) && ! empty( $m['token'] ) && hash_equals( $m['token'], (string) $token ) && time() < (int) $m['expires'];
	}

	public static function pre_get_posts( $query ) {
		if ( is_admin() || ! $query->is_main_query() || empty( $_GET[ self::PARAM ] ) ) { // phpcs:ignore WordPress.Security.NonceVerification
			return;
		}
		$post_id = (int) ( $query->get( 'page_id' ) ? $query->get( 'page_id' ) : $query->get( 'p' ) );
		$token   = sanitize_text_field( wp_unslash( $_GET[ self::PARAM ] ) ); // phpcs:ignore WordPress.Security.NonceVerification
		if ( ! $post_id || ! self::valid( $post_id, $token ) ) {
			return;
		}
		$query->set( 'post_status', array( 'publish', 'draft', 'pending', 'private', 'future' ) );
		add_filter(
			'posts_results',
			function ( $posts ) use ( $post_id ) {
				foreach ( $posts as $p ) {
					if ( (int) $p->ID === $post_id ) {
						$p->post_status = 'publish'; // In-memory only, so WP lets anonymous visitors see it.
					}
				}
				return $posts;
			}
		);
		add_action(
			'send_headers',
			function () {
				nocache_headers();
				header( 'X-Robots-Tag: noindex, nofollow' );
			}
		);
		add_action(
			'wp_head',
			function () {
				echo "<meta name=\"robots\" content=\"noindex,nofollow\">\n";
			},
			1
		);
	}
}
