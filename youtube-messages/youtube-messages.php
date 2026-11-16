<?php
/**
 * Plugin Name:       YouTube Messages Auto Import
 * Description:       Automatically imports videos from a YouTube channel (and its playlists) and shows them as a sermon/message grid. Clicking a message opens it on YouTube. Use the [youtube_messages] shortcode.
 * Version:           1.0.0
 * Requires at least: 5.8
 * Requires PHP:      7.4
 * Author:            Reach Right Studios
 * License:           GPL-2.0-or-later
 * Text Domain:       youtube-messages
 */

defined( 'ABSPATH' ) || exit;

define( 'YTM_VERSION', '1.0.0' );
define( 'YTM_FILE', __FILE__ );
define( 'YTM_DIR', plugin_dir_path( __FILE__ ) );
define( 'YTM_URL', plugin_dir_url( __FILE__ ) );

require_once YTM_DIR . 'includes/class-ytm-settings.php';
require_once YTM_DIR . 'includes/class-ytm-post-type.php';
require_once YTM_DIR . 'includes/class-ytm-youtube.php';
require_once YTM_DIR . 'includes/class-ytm-importer.php';
require_once YTM_DIR . 'includes/class-ytm-admin.php';
require_once YTM_DIR . 'includes/class-ytm-shortcode.php';

YTM_Post_Type::init();
YTM_Importer::init();
YTM_Admin::init();
YTM_Shortcode::init();

register_activation_hook( __FILE__, function () {
	YTM_Post_Type::register();
	YTM_Importer::schedule();
} );

register_deactivation_hook( __FILE__, function () {
	wp_clear_scheduled_hook( YTM_Importer::CRON_HOOK );
} );
