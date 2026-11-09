<?php
/**
 * Minimal SEO output: per-post SEO title + meta description, Open Graph and
 * Twitter Card tags (featured image as share image).
 *
 * Values live in post meta `_csmcp_seo_title` / `_csmcp_seo_description`,
 * editable in a meta box on the edit screen (and via the cs_save_post tool).
 * Stays silent when a dedicated SEO plugin (Yoast, The SEO Framework,
 * Rank Math, AIOSEO) is active so tags are never duplicated.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

class Pro_Extended_SEO {

	const TITLE = '_csmcp_seo_title';
	const DESC  = '_csmcp_seo_description';

	public static function init() {
		add_action( 'init', array( __CLASS__, 'register_meta' ) );
		add_action( 'add_meta_boxes', array( __CLASS__, 'add_box' ) );
		add_action( 'save_post', array( __CLASS__, 'save_box' ), 10, 2 );
		if ( ! self::seo_plugin_active() ) {
			add_filter( 'pre_get_document_title', array( __CLASS__, 'document_title' ), 20 );
			add_action( 'wp_head', array( __CLASS__, 'head_tags' ), 1 );
		}
	}

	public static function seo_plugin_active() {
		return defined( 'WPSEO_VERSION' ) || defined( 'THE_SEO_FRAMEWORK_VERSION' ) || class_exists( 'RankMath' )
			|| defined( 'AIOSEO_VERSION' );
	}

	public static function register_meta() {
		foreach ( array( self::TITLE, self::DESC ) as $key ) {
			register_post_meta(
				'',
				$key,
				array(
					'type'              => 'string',
					'single'            => true,
					'show_in_rest'      => true,
					'sanitize_callback' => 'sanitize_text_field',
					'auth_callback'     => function () {
						return current_user_can( 'edit_posts' );
					},
				)
			);
		}
	}

	/* ------------------------------------------------------------ editing */

	public static function add_box() {
		foreach ( get_post_types( array( 'public' => true ) ) as $pt ) {
			if ( 'attachment' !== $pt ) {
				add_meta_box( 'csmcp-seo', 'SEO (CSMCP)', array( __CLASS__, 'render_box' ), $pt, 'normal', 'low' );
			}
		}
	}

	public static function render_box( $post ) {
		wp_nonce_field( 'csmcp_seo', 'csmcp_seo_nonce' );
		$title = get_post_meta( $post->ID, self::TITLE, true );
		$desc  = get_post_meta( $post->ID, self::DESC, true );
		if ( self::seo_plugin_active() ) {
			echo '<p><em>An SEO plugin is active, so these fields are not output. Use that plugin\'s settings instead.</em></p>';
		}
		echo '<p><label for="csmcp_seo_title"><strong>SEO title</strong> (browser tab &amp; search results; blank = page title)</label><br>';
		echo '<input type="text" class="widefat" id="csmcp_seo_title" name="csmcp_seo_title" value="' . esc_attr( $title ) . '" maxlength="70"></p>';
		echo '<p><label for="csmcp_seo_description"><strong>Meta description</strong> (≈150 characters)</label><br>';
		echo '<textarea class="widefat" rows="3" id="csmcp_seo_description" name="csmcp_seo_description" maxlength="320">' . esc_textarea( $desc ) . '</textarea></p>';
		echo '<p class="description">The featured image is used as the social sharing image.</p>';
	}

	public static function save_box( $post_id, $post ) {
		if ( ! isset( $_POST['csmcp_seo_nonce'] ) || ! wp_verify_nonce( sanitize_text_field( wp_unslash( $_POST['csmcp_seo_nonce'] ) ), 'csmcp_seo' ) ) {
			return;
		}
		if ( ( defined( 'DOING_AUTOSAVE' ) && DOING_AUTOSAVE ) || ! current_user_can( 'edit_post', $post_id ) ) {
			return;
		}
		foreach ( array( 'csmcp_seo_title' => self::TITLE, 'csmcp_seo_description' => self::DESC ) as $field => $key ) {
			$val = isset( $_POST[ $field ] ) ? sanitize_text_field( wp_unslash( $_POST[ $field ] ) ) : '';
			if ( '' === $val ) {
				delete_post_meta( $post_id, $key );
			} else {
				update_post_meta( $post_id, $key, $val );
			}
		}
	}

	/* ------------------------------------------------------------- output */

	private static function current_id() {
		if ( is_front_page() && 'page' === get_option( 'show_on_front' ) ) {
			return (int) get_option( 'page_on_front' );
		}
		return is_singular() ? (int) get_queried_object_id() : 0;
	}

	public static function document_title( $title ) {
		$id = self::current_id();
		if ( $id ) {
			$custom = get_post_meta( $id, self::TITLE, true );
			if ( '' !== $custom ) {
				return $custom;
			}
		}
		return $title;
	}

	public static function head_tags() {
		$id = self::current_id();
		if ( ! $id ) {
			return;
		}
		$desc  = get_post_meta( $id, self::DESC, true );
		$title = get_post_meta( $id, self::TITLE, true );
		$title = '' !== $title ? $title : wp_get_document_title();
		$url   = is_front_page() ? home_url( '/' ) : get_permalink( $id );
		$img   = has_post_thumbnail( $id ) ? wp_get_attachment_image_src( get_post_thumbnail_id( $id ), 'full' ) : null;

		$tags = array();
		if ( '' !== $desc ) {
			$tags[] = array( 'name', 'description', $desc );
		}
		$tags[] = array( 'property', 'og:type', is_front_page() ? 'website' : 'article' );
		$tags[] = array( 'property', 'og:site_name', get_bloginfo( 'name' ) );
		$tags[] = array( 'property', 'og:title', $title );
		if ( '' !== $desc ) {
			$tags[] = array( 'property', 'og:description', $desc );
		}
		$tags[] = array( 'property', 'og:url', $url );
		$tags[] = array( 'property', 'og:locale', str_replace( '-', '_', get_bloginfo( 'language' ) ) );
		if ( $img ) {
			$tags[] = array( 'property', 'og:image', $img[0] );
			$tags[] = array( 'property', 'og:image:width', $img[1] );
			$tags[] = array( 'property', 'og:image:height', $img[2] );
		}
		$tags[] = array( 'name', 'twitter:card', $img ? 'summary_large_image' : 'summary' );
		$tags[] = array( 'name', 'twitter:title', $title );
		if ( '' !== $desc ) {
			$tags[] = array( 'name', 'twitter:description', $desc );
		}
		if ( $img ) {
			$tags[] = array( 'name', 'twitter:image', $img[0] );
		}

		echo "\n<!-- CSMCP SEO -->\n";
		foreach ( $tags as $t ) {
			printf( '<meta %s="%s" content="%s" />' . "\n", $t[0], esc_attr( $t[1] ), esc_attr( $t[2] ) );
		}
	}
}
