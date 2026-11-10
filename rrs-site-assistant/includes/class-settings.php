<?php
/**
 * Settings: API key, model, effort, MCP endpoint switch, monthly token cap.
 *
 * Everything is set on Settings → Site Assistant. (Developers may instead define
 * RRS_AI_API_KEY in wp-config.php; that is optional.)
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

class RRS_AI_Settings {

	const OPTION = 'rrs_ai_settings';
	const USAGE  = 'rrs_ai_usage';

	public static function init() {
		add_action( 'admin_menu', array( __CLASS__, 'menu' ) );
		add_action( 'admin_init', array( __CLASS__, 'register' ) );
		add_action( 'admin_init', array( __CLASS__, 'activation_redirect' ) );
		add_action( 'admin_notices', array( __CLASS__, 'setup_notice' ) );
	}

	public static function url() {
		return admin_url( 'options-general.php?page=rrs-ai-settings' );
	}

	/** First visit to wp-admin after activation → the setup page. */
	public static function activation_redirect() {
		if ( ! get_option( 'rrs_ai_activation_redirect' ) ) {
			return;
		}
		delete_option( 'rrs_ai_activation_redirect' );
		if ( wp_doing_ajax() || isset( $_GET['activate-multi'] ) || ! current_user_can( 'manage_options' ) ) { // phpcs:ignore WordPress.Security.NonceVerification
			return;
		}
		wp_safe_redirect( self::url() );
		exit;
	}

	/** Reminder on every admin page until the key is set. */
	public static function setup_notice() {
		if ( self::get( 'api_key' ) || ! current_user_can( 'manage_options' ) ) {
			return;
		}
		$screen = get_current_screen();
		if ( $screen && 'settings_page_rrs-ai-settings' === $screen->id ) {
			return;
		}
		echo '<div class="notice notice-warning"><p><strong>Site Assistant</strong> is almost ready: add the API key to turn on the chat. <a class="button button-primary" style="margin-left:8px" href="' . esc_url( self::url() ) . '">Finish setup</a></p></div>';
	}

	/**
	 * Check a key against the API (lists one model; costs nothing).
	 *
	 * @return true|string True, or an error message.
	 */
	public static function check_key( $key ) {
		$res = wp_remote_get(
			'https://api.anthropic.com/v1/models?limit=1',
			array(
				'headers' => array(
					'x-api-key'         => $key,
					'anthropic-version' => RRS_AI_Claude::API_VERSION,
				),
				'timeout' => 20,
			)
		);
		if ( is_wp_error( $res ) ) {
			return 'Could not reach the AI service from this server (' . $res->get_error_message() . ').';
		}
		$code = wp_remote_retrieve_response_code( $res );
		if ( 200 === $code ) {
			return true;
		}
		if ( 401 === $code || 403 === $code ) {
			return 'That API key was not accepted. Check that you copied the whole key (it starts with sk-ant-).';
		}
		$data = json_decode( wp_remote_retrieve_body( $res ) );
		return 'The AI service answered with an error: ' . ( $data->error->message ?? 'HTTP ' . $code );
	}

	public static function defaults() {
		return array(
			'api_key'     => '',
			'model'       => 'claude-opus-5-5',
			'effort'      => 'medium',
			'mcp_endpoint' => 1, // CSMCP endpoint for Claude Code.
			'monthly_cap' => 5000000, // input + output tokens per calendar month.
		);
	}

	public static function get( $key ) {
		$opts = wp_parse_args( get_option( self::OPTION, array() ), self::defaults() );
		if ( 'api_key' === $key && defined( 'RRS_AI_API_KEY' ) && RRS_AI_API_KEY ) {
			return RRS_AI_API_KEY;
		}
		return $opts[ $key ] ?? null;
	}

	/** Who may use the assistant. Writes run as this user through CSMCP. */
	public static function capability() {
		return apply_filters( 'rrs_ai_capability', 'manage_options' );
	}

	/* ---------- usage tracking ---------- */

	public static function usage_this_month() {
		$u = get_option( self::USAGE, array() );
		return (int) ( $u[ gmdate( 'Y-m' ) ] ?? 0 );
	}

	public static function add_usage( $tokens ) {
		$u                    = get_option( self::USAGE, array() );
		$m                    = gmdate( 'Y-m' );
		$u[ $m ]              = (int) ( $u[ $m ] ?? 0 ) + (int) $tokens;
		update_option( self::USAGE, array_slice( $u, -12, null, true ), false );
	}

	public static function over_cap() {
		$cap = (int) self::get( 'monthly_cap' );
		return $cap > 0 && self::usage_this_month() >= $cap;
	}

	/* ---------- admin page ---------- */

	public static function menu() {
		add_options_page( 'Site Assistant', 'Site Assistant', 'manage_options', 'rrs-ai-settings', array( __CLASS__, 'render' ) );
	}

	public static function register() {
		register_setting(
			'rrs_ai',
			self::OPTION,
			array(
				'sanitize_callback' => array( __CLASS__, 'sanitize' ),
			)
		);
	}

	public static function sanitize( $in ) {
		$old = wp_parse_args( get_option( self::OPTION, array() ), self::defaults() );
		$out = $old;

		// Empty key field = keep the saved key (the field is never echoed back).
		$new_key = trim( sanitize_text_field( $in['api_key'] ?? '' ) );
		if ( '' !== $new_key && $new_key !== $old['api_key'] ) {
			$ok = self::check_key( $new_key );
			if ( true === $ok ) {
				$out['api_key'] = $new_key;
				add_settings_error( self::OPTION, 'rrs_ai_key_ok', 'API key works. The chat is on: look for the blue bubble at the bottom right.', 'success' );
			} else {
				add_settings_error( self::OPTION, 'rrs_ai_key_bad', $ok . ' The key was not saved.', 'error' );
			}
		}
		if ( ! empty( $in['clear_key'] ) ) {
			$out['api_key'] = '';
		}
		$out['model']       = sanitize_text_field( $in['model'] ?? $old['model'] );
		$out['effort']      = in_array( $in['effort'] ?? '', array( 'low', 'medium', 'high', 'xhigh', 'max' ), true ) ? $in['effort'] : $old['effort'];
		$out['mcp_endpoint'] = empty( $in['mcp_endpoint'] ) ? 0 : 1;
		$out['monthly_cap'] = max( 0, (int) ( $in['monthly_cap'] ?? $old['monthly_cap'] ) );

		return $out;
	}

	public static function render() {
		$o        = wp_parse_args( get_option( self::OPTION, array() ), self::defaults() );
		$from_cfg = defined( 'RRS_AI_API_KEY' ) && RRS_AI_API_KEY;
		$has_key  = (bool) self::get( 'api_key' );

		$tools = RRS_AI_Tools_Bridge::list_tools();
		?>
		<div class="wrap">
			<h1>Site Assistant</h1>

			<h2>Status</h2>
			<ul>
				<li><strong>API key:</strong> <?php echo $has_key ? ( $from_cfg ? 'set in wp-config.php ✅' : 'saved ✅' ) : '<span style="color:#b32d2e">not set yet: paste it below and click Save</span>'; ?></li>
				<li><strong>Cornerstone tools:</strong>
					<?php
					if ( is_wp_error( $tools ) ) {
						echo '<span style="color:#b32d2e">' . esc_html( $tools->get_error_message() ) . '</span>';
					} else {
						echo esc_html( count( $tools ) . ' tools available ✅' ) . ' — <a href="' . esc_url( admin_url( 'options-general.php?page=pro-extended&tab=tools' ) ) . '">turn tools on/off, read-only mode, activity &amp; backups</a>';
					}
					?>
				</li>
				<li><strong>Tokens used this month:</strong> <?php echo esc_html( number_format( self::usage_this_month() ) ); ?>
					/ <?php echo $o['monthly_cap'] ? esc_html( number_format( $o['monthly_cap'] ) ) : 'no cap'; ?></li>
			</ul>

			<form method="post" action="options.php">
				<?php settings_fields( 'rrs_ai' ); ?>
				<table class="form-table" role="presentation">
					<tr>
						<th><label for="rrs-key">Anthropic API key</label></th>
						<td>
							<?php if ( $from_cfg ) : ?>
								<em>Defined in wp-config.php (RRS_AI_API_KEY).</em>
							<?php else : ?>
								<input id="rrs-key" type="password" class="regular-text" name="<?php echo esc_attr( self::OPTION ); ?>[api_key]" value="" autocomplete="off" placeholder="<?php echo $has_key ? '•••••••• (saved — leave blank to keep)' : 'sk-ant-...'; ?>">
								<?php if ( $has_key ) : ?>
									<label><input type="checkbox" name="<?php echo esc_attr( self::OPTION ); ?>[clear_key]" value="1"> Remove saved key</label>
								<?php endif; ?>
								<p class="description">Get it at <a href="https://console.anthropic.com/settings/keys" target="_blank" rel="noopener">console.anthropic.com → API Keys</a>, paste it here and click <strong>Save Changes</strong>. The key is checked when you save. It is kept on the server and never shown to site users or sent to the browser.</p>
							<?php endif; ?>
						</td>
					</tr>
					<tr>
						<th><label for="rrs-model">Model</label></th>
						<td><input id="rrs-model" class="regular-text" name="<?php echo esc_attr( self::OPTION ); ?>[model]" value="<?php echo esc_attr( $o['model'] ); ?>"></td>
					</tr>
					<tr>
						<th><label for="rrs-effort">Effort</label></th>
						<td>
							<select id="rrs-effort" name="<?php echo esc_attr( self::OPTION ); ?>[effort]">
								<?php foreach ( array( 'low', 'medium', 'high', 'xhigh', 'max' ) as $e ) : ?>
									<option value="<?php echo esc_attr( $e ); ?>" <?php selected( $o['effort'], $e ); ?>><?php echo esc_html( $e ); ?></option>
								<?php endforeach; ?>
							</select>
							<p class="description">Higher = more careful but slower and more tokens.</p>
						</td>
					</tr>
					<tr>
						<th>Claude Code connection</th>
						<td>
							<label><input type="checkbox" name="<?php echo esc_attr( self::OPTION ); ?>[mcp_endpoint]" value="1" <?php checked( $o['mcp_endpoint'], 1 ); ?>> Allow the MCP endpoint <code>/wp-json/cs-mcp/v1/mcp</code></label>
							<p class="description">For the team's Claude Code builds (Application Password, see Settings → CSMCP). Not needed by the chat. Switch off on sites where nobody builds with Claude Code.</p>
						</td>
					</tr>
					<tr>
						<th><label for="rrs-cap">Monthly token cap</label></th>
						<td><input id="rrs-cap" type="number" min="0" step="100000" name="<?php echo esc_attr( self::OPTION ); ?>[monthly_cap]" value="<?php echo esc_attr( $o['monthly_cap'] ); ?>"> <span class="description">0 = no cap</span></td>
					</tr>
				</table>
				<?php submit_button(); ?>
			</form>
		</div>
		<?php
	}
}
