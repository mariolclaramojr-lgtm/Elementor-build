<?php
/**
 * Plugin Name: RRS Site Assistant
 * Description: AI chat assistant in WP Admin that edits this Cornerstone site through the CSMCP plugin's tools (create pages, update sections, menus, forms...). Requires CSMCP.
 * Version:     0.1.0
 * Author:      ReachRight Studios
 * Requires PHP: 8.0
 * Requires at least: 6.4
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

define( 'RRS_AI_VERSION', '0.1.0' );
define( 'RRS_AI_DIR', plugin_dir_path( __FILE__ ) );
define( 'RRS_AI_URL', plugin_dir_url( __FILE__ ) );

require_once RRS_AI_DIR . 'includes/class-settings.php';
require_once RRS_AI_DIR . 'includes/class-mcp-bridge.php';
require_once RRS_AI_DIR . 'includes/class-claude.php';
require_once RRS_AI_DIR . 'includes/class-chat.php';

RRS_AI_Settings::init();
RRS_AI_Chat::init();
