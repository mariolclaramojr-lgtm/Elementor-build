<?php
/**
 * Plugin Name: CSMCP - By Mario C
 * Description: MCP server for Themeco Pro / Cornerstone. Lets an AI agent inspect, create and edit Cornerstone pages, including importing existing HTML designs.
 * Version:     0.7.3
 * Author:      Mario C
 * Requires PHP: 7.4
 * License:     GPL-2.0-or-later
 *
 * Endpoint: POST /wp-json/cs-mcp/v1/mcp  (MCP Streamable HTTP, JSON responses)
 * Auth:     WordPress Application Password (HTTP Basic). User needs the edit_pages capability.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

define( 'PRO_EXTENDED_VERSION', '0.7.3' );
define( 'PRO_EXTENDED_DIR', plugin_dir_path( __FILE__ ) );

require_once PRO_EXTENDED_DIR . 'includes/class-cs-store.php';
require_once PRO_EXTENDED_DIR . 'includes/class-tools.php';
require_once PRO_EXTENDED_DIR . 'includes/class-mcp-server.php';
require_once PRO_EXTENDED_DIR . 'includes/class-admin.php';
require_once PRO_EXTENDED_DIR . 'includes/class-preview.php';
require_once PRO_EXTENDED_DIR . 'includes/class-seo.php';

add_action( 'rest_api_init', array( 'Pro_Extended_MCP_Server', 'register_routes' ) );
Pro_Extended_Preview::init();
Pro_Extended_SEO::init();

if ( is_admin() ) {
	Pro_Extended_Admin::init();
}
