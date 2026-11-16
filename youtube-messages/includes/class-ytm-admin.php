<?php
defined( 'ABSPATH' ) || exit;

/**
 * Messages › Settings & Sync screen.
 */
class YTM_Admin {

	const PAGE = 'ytm-settings';

	public static function init() {
		add_action( 'admin_menu', array( __CLASS__, 'menu' ) );
		add_action( 'admin_init', array( __CLASS__, 'register' ) );
		add_action( 'admin_post_ytm_sync', array( __CLASS__, 'handle_sync' ) );
		add_filter( 'plugin_action_links_' . plugin_basename( YTM_FILE ), array( __CLASS__, 'action_links' ) );
	}

	public static function page_url() {
		return admin_url( 'edit.php?post_type=' . YTM_Post_Type::POST_TYPE . '&page=' . self::PAGE );
	}

	public static function action_links( $links ) {
		array_unshift( $links, '<a href="' . esc_url( self::page_url() ) . '">' . esc_html__( 'Settings', 'youtube-messages' ) . '</a>' );
		return $links;
	}

	public static function menu() {
		add_submenu_page(
			'edit.php?post_type=' . YTM_Post_Type::POST_TYPE,
			__( 'YouTube Settings & Sync', 'youtube-messages' ),
			__( 'Settings & Sync', 'youtube-messages' ),
			'manage_options',
			self::PAGE,
			array( __CLASS__, 'render' )
		);
	}

	public static function register() {
		register_setting( 'ytm', YTM_Settings::OPTION, array(
			'type'              => 'array',
			'sanitize_callback' => array( 'YTM_Settings', 'sanitize' ),
			'default'           => YTM_Settings::defaults(),
		) );
	}

	public static function handle_sync() {
		if ( ! current_user_can( 'manage_options' ) ) {
			wp_die( esc_html__( 'You do not have permission to do that.', 'youtube-messages' ) );
		}
		check_admin_referer( 'ytm_sync' );
		$full = ! empty( $_POST['full'] );
		YTM_Importer::sync( $full );
		wp_safe_redirect( add_query_arg( 'ytm_synced', '1', self::page_url() ) );
		exit;
	}

	private static function field_text( $key, $placeholder = '', $type = 'text', $class = 'regular-text' ) {
		printf(
			'<input type="%1$s" class="%2$s" id="ytm_%3$s" name="%4$s[%3$s]" value="%5$s" placeholder="%6$s" autocomplete="off">',
			esc_attr( $type ),
			esc_attr( $class ),
			esc_attr( $key ),
			esc_attr( YTM_Settings::OPTION ),
			esc_attr( YTM_Settings::get( $key ) ),
			esc_attr( $placeholder )
		);
	}

	private static function field_check( $key, $label ) {
		printf(
			'<label><input type="checkbox" name="%1$s[%2$s]" value="1" %3$s> %4$s</label>',
			esc_attr( YTM_Settings::OPTION ),
			esc_attr( $key ),
			checked( 1, (int) YTM_Settings::get( $key ), false ),
			esc_html( $label )
		);
	}

	public static function render() {
		if ( ! current_user_can( 'manage_options' ) ) {
			return;
		}
		$opt     = YTM_Settings::OPTION;
		$last    = get_option( 'ytm_last_sync' );
		$channel = get_option( 'ytm_channel' );
		$count   = wp_count_posts( YTM_Post_Type::POST_TYPE );
		$next    = wp_next_scheduled( YTM_Importer::CRON_HOOK );
		$has_key = '' !== YTM_Settings::get( 'api_key' );
		?>
		<div class="wrap">
			<h1><?php esc_html_e( 'YouTube Messages', 'youtube-messages' ); ?></h1>

			<?php if ( isset( $_GET['ytm_synced'] ) && is_array( $last ) ) : // phpcs:ignore WordPress.Security.NonceVerification ?>
				<div class="notice <?php echo $last['errors'] ? 'notice-warning' : 'notice-success'; ?> is-dismissible">
					<p><strong><?php echo esc_html( self::summary_line( $last ) ); ?></strong></p>
					<?php foreach ( array_unique( $last['errors'] ) as $err ) : ?>
						<p><?php echo esc_html( $err ); ?></p>
					<?php endforeach; ?>
				</div>
			<?php endif; ?>

			<div style="display:flex;gap:24px;flex-wrap:wrap;align-items:flex-start">
			<div style="flex:1 1 560px;min-width:0">

			<h2><?php esc_html_e( 'Status', 'youtube-messages' ); ?></h2>
			<table class="widefat striped" style="max-width:760px">
				<tbody>
					<tr><th style="width:180px"><?php esc_html_e( 'Channel', 'youtube-messages' ); ?></th><td>
						<?php
						if ( is_array( $channel ) && ! empty( $channel['id'] ) ) {
							printf( '<a href="%s" target="_blank" rel="noopener">%s</a> <code>%s</code>', esc_url( 'https://www.youtube.com/channel/' . $channel['id'] ), esc_html( $channel['title'] ? $channel['title'] : $channel['input'] ), esc_html( $channel['id'] ) );
						} else {
							esc_html_e( 'Not connected yet. Save your channel below, then click "Check for new videos".', 'youtube-messages' );
						}
						?>
					</td></tr>
					<tr><th><?php esc_html_e( 'Source', 'youtube-messages' ); ?></th><td>
						<?php echo $has_key ? esc_html__( 'YouTube Data API (full archive, live/Shorts detection)', 'youtube-messages' ) : esc_html__( 'RSS feed (newest 15 videos only; add an API key for the full archive)', 'youtube-messages' ); ?>
					</td></tr>
					<tr><th><?php esc_html_e( 'Messages imported', 'youtube-messages' ); ?></th><td>
						<?php
						printf(
							'<a href="%s">%s</a>',
							esc_url( admin_url( 'edit.php?post_type=' . YTM_Post_Type::POST_TYPE ) ),
							esc_html( sprintf( _n( '%s published', '%s published', (int) $count->publish, 'youtube-messages' ), number_format_i18n( $count->publish ) ) )
						);
						?>
					</td></tr>
					<tr><th><?php esc_html_e( 'Last check', 'youtube-messages' ); ?></th><td>
						<?php echo is_array( $last ) ? esc_html( self::summary_line( $last ) ) : esc_html__( 'Never', 'youtube-messages' ); ?>
						<?php if ( is_array( $last ) && $last['errors'] && ! isset( $_GET['ytm_synced'] ) ) : // phpcs:ignore WordPress.Security.NonceVerification ?>
							<br><span style="color:#b32d2e"><?php echo esc_html( implode( ' ', array_unique( $last['errors'] ) ) ); ?></span>
						<?php endif; ?>
					</td></tr>
					<tr><th><?php esc_html_e( 'Next automatic check', 'youtube-messages' ); ?></th><td>
						<?php echo $next ? esc_html( sprintf( __( 'in %s', 'youtube-messages' ), human_time_diff( time(), $next ) ) ) : '&mdash;'; ?>
					</td></tr>
				</tbody>
			</table>

			<form method="post" action="<?php echo esc_url( admin_url( 'admin-post.php' ) ); ?>" style="margin:12px 0 28px;display:flex;gap:8px;flex-wrap:wrap">
				<?php wp_nonce_field( 'ytm_sync' ); ?>
				<input type="hidden" name="action" value="ytm_sync">
				<button class="button button-primary" name="full" value="0"><?php esc_html_e( 'Check for new videos now', 'youtube-messages' ); ?></button>
				<button class="button" name="full" value="1" <?php disabled( ! $has_key ); ?> onclick="return confirm('<?php echo esc_js( __( 'Import every video on the channel? This can take a few minutes.', 'youtube-messages' ) ); ?>')"><?php esc_html_e( 'Import full archive', 'youtube-messages' ); ?></button>
			</form>

			<form method="post" action="options.php">
				<?php settings_fields( 'ytm' ); ?>

				<h2><?php esc_html_e( 'YouTube', 'youtube-messages' ); ?></h2>
				<table class="form-table" role="presentation">
					<tr><th><label for="ytm_channel"><?php esc_html_e( 'YouTube channel', 'youtube-messages' ); ?></label></th><td>
						<?php self::field_text( 'channel', 'https://www.youtube.com/@YourChurch' ); ?>
						<p class="description"><?php esc_html_e( 'Channel URL, @handle, or channel ID.', 'youtube-messages' ); ?></p>
					</td></tr>
					<tr><th><label for="ytm_api_key"><?php esc_html_e( 'YouTube API key', 'youtube-messages' ); ?></label></th><td>
						<?php self::field_text( 'api_key', 'AIza…', 'password' ); ?>
						<p class="description">
							<?php esc_html_e( 'Recommended. Free. Without it only the newest 15 videos can be read, and YouTube\'s RSS feed is often down.', 'youtube-messages' ); ?>
							<a href="https://console.cloud.google.com/apis/library/youtube.googleapis.com" target="_blank" rel="noopener"><?php esc_html_e( 'Get a key', 'youtube-messages' ); ?></a>:
							<?php esc_html_e( 'create a Google Cloud project, enable "YouTube Data API v3", then Credentials › Create credentials › API key.', 'youtube-messages' ); ?>
						</p>
					</td></tr>
					<tr><th><label for="ytm_playlists"><?php esc_html_e( 'Series playlists', 'youtube-messages' ); ?></label></th><td>
						<textarea class="large-text" rows="3" id="ytm_playlists" name="<?php echo esc_attr( $opt ); ?>[playlists]" placeholder="https://www.youtube.com/playlist?list=PL…"><?php echo esc_textarea( YTM_Settings::get( 'playlists' ) ); ?></textarea>
						<p class="description"><?php esc_html_e( 'Optional. One playlist URL per line. Each playlist becomes a Series, and its videos are tagged with it.', 'youtube-messages' ); ?></p>
					</td></tr>
					<tr><th><label for="ytm_interval"><?php esc_html_e( 'Check for new videos', 'youtube-messages' ); ?></label></th><td>
						<select id="ytm_interval" name="<?php echo esc_attr( $opt ); ?>[interval]">
							<?php
							$intervals = array(
								'ytm_15min'  => __( 'Every 15 minutes', 'youtube-messages' ),
								'ytm_30min'  => __( 'Every 30 minutes', 'youtube-messages' ),
								'hourly'     => __( 'Every hour', 'youtube-messages' ),
								'twicedaily' => __( 'Twice a day', 'youtube-messages' ),
								'daily'      => __( 'Once a day', 'youtube-messages' ),
							);
							foreach ( $intervals as $value => $label ) {
								printf( '<option value="%s" %s>%s</option>', esc_attr( $value ), selected( YTM_Settings::get( 'interval' ), $value, false ), esc_html( $label ) );
							}
							?>
						</select>
					</td></tr>
				</table>

				<h2><?php esc_html_e( 'What to import', 'youtube-messages' ); ?></h2>
				<table class="form-table" role="presentation">
					<tr><th><?php esc_html_e( 'Skip', 'youtube-messages' ); ?></th><td>
						<?php self::field_check( 'skip_shorts', __( 'YouTube Shorts', 'youtube-messages' ) ); ?><br>
						<?php self::field_check( 'skip_upcoming', __( 'Scheduled live streams that haven\'t started yet (they\'re added once they go live)', 'youtube-messages' ) ); ?>
					</td></tr>
					<tr><th><label for="ytm_include_keywords"><?php esc_html_e( 'Only titles containing', 'youtube-messages' ); ?></label></th><td>
						<?php self::field_text( 'include_keywords', 'Sermon, Worship' ); ?>
						<p class="description"><?php esc_html_e( 'Optional, comma-separated. Leave blank to import every video.', 'youtube-messages' ); ?></p>
					</td></tr>
					<tr><th><label for="ytm_exclude_keywords"><?php esc_html_e( 'Skip titles containing', 'youtube-messages' ); ?></label></th><td>
						<?php self::field_text( 'exclude_keywords', 'Trailer, Announcement' ); ?>
					</td></tr>
					<tr><th><label for="ytm_type_rules"><?php esc_html_e( 'Service type rules', 'youtube-messages' ); ?></label></th><td>
						<textarea class="regular-text" rows="4" id="ytm_type_rules" name="<?php echo esc_attr( $opt ); ?>[type_rules]"><?php echo esc_textarea( YTM_Settings::get( 'type_rules' ) ); ?></textarea>
						<p class="description"><?php esc_html_e( 'One per line: "word in the title = Service Type". The first match wins.', 'youtube-messages' ); ?></p>
					</td></tr>
					<tr><th><label for="ytm_default_type"><?php esc_html_e( 'Default service type', 'youtube-messages' ); ?></label></th><td>
						<?php self::field_text( 'default_type', 'Message' ); ?>
						<p class="description"><?php esc_html_e( 'Used when no rule matches. Leave blank for none.', 'youtube-messages' ); ?></p>
					</td></tr>
					<tr><th><?php esc_html_e( 'Updates', 'youtube-messages' ); ?></th><td>
						<?php self::field_check( 'update_existing', __( 'Keep titles and descriptions in sync when they\'re edited on YouTube (edits made here in WordPress are never overwritten)', 'youtube-messages' ) ); ?><br>
						<?php self::field_check( 'featured_images', __( 'Save thumbnails to the Media Library as featured images (only needed for page-builder loops)', 'youtube-messages' ) ); ?>
					</td></tr>
				</table>

				<h2><?php esc_html_e( 'Display', 'youtube-messages' ); ?></h2>
				<table class="form-table" role="presentation">
					<tr><th><?php esc_html_e( 'Opening videos', 'youtube-messages' ); ?></th><td>
						<?php self::field_check( 'new_tab', __( 'Open YouTube in a new tab', 'youtube-messages' ) ); ?>
					</td></tr>
					<tr><th><label for="ytm_accent_color"><?php esc_html_e( 'Accent colour', 'youtube-messages' ); ?></label></th><td>
						<?php self::field_text( 'accent_color', '#A51C30', 'text', 'small-text' ); ?>
						<p class="description"><?php esc_html_e( 'Hex colour for the play button, buttons and active filters.', 'youtube-messages' ); ?></p>
					</td></tr>
				</table>

				<?php submit_button(); ?>
			</form>
			</div>

			<div style="flex:0 1 340px;background:#fff;border:1px solid #c3c4c7;padding:4px 18px 14px">
				<h2><?php esc_html_e( 'Show messages on a page', 'youtube-messages' ); ?></h2>
				<p><?php esc_html_e( 'Add this shortcode to any page (Cornerstone: Raw Content or Text element; Elementor: Shortcode widget; block editor: Shortcode block):', 'youtube-messages' ); ?></p>
				<p><code>[youtube_messages]</code></p>
				<p><?php esc_html_e( 'Options (all optional):', 'youtube-messages' ); ?></p>
				<ul style="list-style:disc;padding-left:18px">
					<li><code>per_page="12"</code> <?php esc_html_e( 'messages per page', 'youtube-messages' ); ?></li>
					<li><code>columns="3"</code> <?php esc_html_e( '1–4', 'youtube-messages' ); ?></li>
					<li><code>layout="grid"</code> <?php esc_html_e( 'or "list"', 'youtube-messages' ); ?></li>
					<li><code>featured="yes"</code> <?php esc_html_e( 'show the newest message large on top', 'youtube-messages' ); ?></li>
					<li><code>filters="yes"</code> <?php esc_html_e( 'search box + series/type dropdowns', 'youtube-messages' ); ?></li>
					<li><code>pagination="yes"</code></li>
					<li><code>series="advent-2026"</code> <?php esc_html_e( 'only one series (slug)', 'youtube-messages' ); ?></li>
					<li><code>type="sermon"</code> <?php esc_html_e( 'only one service type (slug)', 'youtube-messages' ); ?></li>
					<li><code>show_date="yes" show_type="yes" show_duration="yes" show_excerpt="no"</code></li>
				</ul>
				<p><?php esc_html_e( 'Latest message only:', 'youtube-messages' ); ?><br><code>[youtube_messages per_page="1" columns="1" filters="no" pagination="no"]</code></p>
				<p><?php esc_html_e( 'To hide a video, trash it or set it to Draft under Messages. Deleted messages are never re-imported.', 'youtube-messages' ); ?></p>
			</div>
			</div>
		</div>
		<?php
	}

	private static function summary_line( array $last ) {
		return sprintf(
			/* translators: 1: time ago, 2: created, 3: updated, 4: skipped */
			__( '%1$s ago: %2$d new, %3$d updated, %4$d skipped.', 'youtube-messages' ),
			human_time_diff( $last['time'], time() ),
			$last['created'],
			$last['updated'],
			$last['skipped']
		);
	}
}
