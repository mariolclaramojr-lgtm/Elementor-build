<?php
/**
 * Removes the plugin's settings. Imported messages are kept (delete them under Messages first
 * if you want them gone).
 */
defined( 'WP_UNINSTALL_PLUGIN' ) || exit;

foreach ( array( 'ytm_settings', 'ytm_channel', 'ytm_last_sync', 'ytm_playlist_titles', 'ytm_shorts_cache', 'ytm_ignored' ) as $option ) {
	delete_option( $option );
}
delete_transient( 'ytm_sync_lock' );
wp_clear_scheduled_hook( 'ytm_sync' );
