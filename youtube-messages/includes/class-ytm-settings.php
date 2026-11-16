<?php
defined( 'ABSPATH' ) || exit;

/**
 * Plugin settings, stored in a single option.
 */
class YTM_Settings {

	const OPTION = 'ytm_settings';

	public static function defaults() {
		return array(
			'channel'          => '',
			'api_key'          => '',
			'playlists'        => '',
			'interval'         => 'hourly',
			'skip_shorts'      => 1,
			'skip_upcoming'    => 1,
			'include_keywords' => '',
			'exclude_keywords' => '',
			'type_rules'       => "Sermon = Sermon\nWorship = Worship Service",
			'default_type'     => '',
			'update_existing'  => 1,
			'featured_images'  => 0,
			'new_tab'          => 1,
			'accent_color'     => '#A51C30',
		);
	}

	public static function all() {
		$saved = get_option( self::OPTION, array() );
		return wp_parse_args( is_array( $saved ) ? $saved : array(), self::defaults() );
	}

	public static function get( $key ) {
		$all = self::all();
		return isset( $all[ $key ] ) ? $all[ $key ] : null;
	}

	/**
	 * Sanitize callback for register_setting().
	 */
	public static function sanitize( $input ) {
		$d   = self::defaults();
		$in  = is_array( $input ) ? $input : array();
		$out = array();

		$out['channel']          = sanitize_text_field( $in['channel'] ?? '' );
		$out['api_key']          = preg_replace( '/[^A-Za-z0-9_\-]/', '', $in['api_key'] ?? '' );
		$out['playlists']        = sanitize_textarea_field( $in['playlists'] ?? '' );
		$out['interval']         = in_array( $in['interval'] ?? '', array( 'ytm_15min', 'ytm_30min', 'hourly', 'twicedaily', 'daily' ), true ) ? $in['interval'] : $d['interval'];
		$out['skip_shorts']      = empty( $in['skip_shorts'] ) ? 0 : 1;
		$out['skip_upcoming']    = empty( $in['skip_upcoming'] ) ? 0 : 1;
		$out['include_keywords'] = sanitize_text_field( $in['include_keywords'] ?? '' );
		$out['exclude_keywords'] = sanitize_text_field( $in['exclude_keywords'] ?? '' );
		$out['type_rules']       = sanitize_textarea_field( $in['type_rules'] ?? '' );
		$out['default_type']     = sanitize_text_field( $in['default_type'] ?? '' );
		$out['update_existing']  = empty( $in['update_existing'] ) ? 0 : 1;
		$out['featured_images']  = empty( $in['featured_images'] ) ? 0 : 1;
		$out['new_tab']          = empty( $in['new_tab'] ) ? 0 : 1;
		$out['accent_color']     = sanitize_hex_color( $in['accent_color'] ?? '' ) ?: $d['accent_color'];

		$old = self::all();
		if ( $old['channel'] !== $out['channel'] || $old['api_key'] !== $out['api_key'] ) {
			delete_option( 'ytm_channel' ); // Re-resolve the channel on next sync.
		}
		if ( $old['interval'] !== $out['interval'] ) {
			wp_clear_scheduled_hook( YTM_Importer::CRON_HOOK );
			wp_schedule_event( time() + 60, $out['interval'], YTM_Importer::CRON_HOOK );
		}
		return $out;
	}

	/** Comma-separated keywords → lowercase array. */
	public static function keywords( $key ) {
		$list = array_map( 'trim', explode( ',', (string) self::get( $key ) ) );
		return array_values( array_filter( array_map( 'strtolower', $list ), 'strlen' ) );
	}

	/** "Keyword = Type" lines → [ [keyword, type], ... ]. */
	public static function type_rules() {
		$rules = array();
		foreach ( preg_split( '/\r\n|\r|\n/', (string) self::get( 'type_rules' ) ) as $line ) {
			$parts = array_map( 'trim', explode( '=', $line, 2 ) );
			if ( 2 === count( $parts ) && '' !== $parts[0] && '' !== $parts[1] ) {
				$rules[] = $parts;
			}
		}
		return $rules;
	}

	/** Playlist IDs pulled from URLs or bare IDs, one per line or comma-separated. */
	public static function playlist_ids() {
		$ids = array();
		foreach ( preg_split( '/[\s,]+/', (string) self::get( 'playlists' ) ) as $item ) {
			if ( preg_match( '/[?&]list=([A-Za-z0-9_\-]+)/', $item, $m ) ) {
				$ids[] = $m[1];
			} elseif ( preg_match( '/^(PL|OL|UU|FL)[A-Za-z0-9_\-]{10,}$/', $item ) ) {
				$ids[] = $item;
			}
		}
		return array_values( array_unique( $ids ) );
	}
}
