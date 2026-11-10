<?php
/**
 * Plugin Name: RRS Site Assistant
 * Description: AI chat in WordPress that edits this Themeco Pro / Cornerstone site: create pages, update sections, menus, forms. Includes CSMCP (Cornerstone tools + MCP endpoint for Claude Code); no other plugin needed.
 * Version:     0.3.0
 * Author:      ReachRight Studios
 * Requires PHP: 7.4
 * Requires at least: 6.4
 * License:     GPL-2.0-or-later
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

define( 'RRS_AI_VERSION', '0.3.0' );
define( 'RRS_AI_DIR', plugin_dir_path( __FILE__ ) );
define( 'RRS_AI_URL', plugin_dir_url( __FILE__ ) );

/*
 * Bundled CSMCP 0.8.0 (class names, options and post meta unchanged, so a site that ran the
 * standalone CSMCP keeps its settings, activity log, backups and SEO fields).
 * If the standalone CSMCP plugin is still active it has already loaded these classes: use it,
 * and ask the admin to deactivate it.
 */
if ( class_exists( 'Pro_Extended_Tools' ) ) {
	add_action(
		'admin_notices',
		function () {
			if ( current_user_can( 'activate_plugins' ) ) {
				echo '<div class="notice notice-warning"><p><strong>RRS Site Assistant</strong> already includes CSMCP. Deactivate and delete the separate <em>CSMCP</em> plugin; settings, logs and backups carry over.</p></div>';
			}
		}
	);
} else {
	define( 'PRO_EXTENDED_VERSION', '0.8.0' );
	define( 'PRO_EXTENDED_DIR', RRS_AI_DIR . 'includes/csmcp/' );

	require_once PRO_EXTENDED_DIR . 'class-cs-store.php';
	require_once PRO_EXTENDED_DIR . 'class-tools.php';
	require_once PRO_EXTENDED_DIR . 'class-mcp-server.php';
	require_once PRO_EXTENDED_DIR . 'class-admin.php';
	require_once PRO_EXTENDED_DIR . 'class-preview.php';
	require_once PRO_EXTENDED_DIR . 'class-seo.php';

	// MCP endpoint for Claude Code (Application Password). Can be switched off in Settings → Site Assistant.
	add_action(
		'rest_api_init',
		function () {
			if ( RRS_AI_Settings::get( 'mcp_endpoint' ) ) {
				Pro_Extended_MCP_Server::register_routes();
			}
		}
	);
	Pro_Extended_Preview::init();
	Pro_Extended_SEO::init();
	if ( is_admin() ) {
		Pro_Extended_Admin::init();
	}
}

/*
 * On activation, switch off the standalone CSMCP plugin (whatever its folder is called):
 * from the next page load the bundled copy takes over with the same data.
 */
register_activation_hook(
	__FILE__,
	function () {
		// Open Settings → Site Assistant on the next admin page load.
		update_option( 'rrs_ai_activation_redirect', 1, false );

		if ( ! class_exists( 'Pro_Extended_Tools' ) ) {
			return;
		}
		$file = ( new ReflectionClass( 'Pro_Extended_Tools' ) )->getFileName();
		if ( 0 === strpos( wp_normalize_path( $file ), wp_normalize_path( RRS_AI_DIR ) ) ) {
			return; // Our own bundled copy.
		}
		require_once ABSPATH . 'wp-admin/includes/plugin.php';
		foreach ( (array) get_option( 'active_plugins', array() ) as $plugin ) {
			$dir = wp_normalize_path( WP_PLUGIN_DIR . '/' . dirname( $plugin ) . '/' );
			if ( '.' !== dirname( $plugin ) && 0 === strpos( wp_normalize_path( $file ), $dir ) ) {
				deactivate_plugins( $plugin, true );
			}
		}
	}
);

require_once RRS_AI_DIR . 'includes/class-settings.php';
require_once RRS_AI_DIR . 'includes/class-tools-bridge.php';
require_once RRS_AI_DIR . 'includes/class-claude.php';
require_once RRS_AI_DIR . 'includes/class-chat.php';

RRS_AI_Settings::init();
RRS_AI_Chat::init();
