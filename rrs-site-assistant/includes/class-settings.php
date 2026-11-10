<?php
/**
 * Settings: API key, model, CSMCP route, monthly token cap.
 *
 * The API key can be set in wp-config.php instead of the database:
 *   define( 'RRS_AI_API_KEY', 'sk-ant-...' );
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
	}

	public static function defaults() {
		return array(
			'api_key'     => '',
			'model'       => 'claude-opus-5-5',
			'effort'      => 'medium',
			'mcp_route'   => '/cs-mcp/v1/mcp',
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
		if ( ! empty( $in['api_key'] ) ) {
			$out['api_key'] = sanitize_text_field( $in['api_key'] );
		}
		if ( ! empty( $in['clear_key'] ) ) {
			$out['api_key'] = '';
		}
		$out['model']       = sanitize_text_field( $in['model'] ?? $old['model'] );
		$out['effort']      = in_array( $in['effort'] ?? '', array( 'low', 'medium', 'high', 'xhigh', 'max' ), true ) ? $in['effort'] : $old['effort'];
		$out['mcp_route']   = '/' . ltrim( sanitize_text_field( $in['mcp_route'] ?? $old['mcp_route'] ), '/' );
		$out['monthly_cap'] = max( 0, (int) ( $in['monthly_cap'] ?? $old['monthly_cap'] ) );

		delete_transient( RRS_AI_MCP_Bridge::TOOLS_CACHE );
		return $out;
	}

	public static function render() {
		$o        = wp_parse_args( get_option( self::OPTION, array() ), self::defaults() );
		$from_cfg = defined( 'RRS_AI_API_KEY' ) && RRS_AI_API_KEY;
		$has_key  = (bool) self::get( 'api_key' );

		// Live check of the CSMCP connection.
		$tools = RRS_AI_MCP_Bridge::list_tools( true );
		?>
		<div class="wrap">
			<h1>Site Assistant</h1>

			<h2>Status</h2>
			<ul>
				<li><strong>API key:</strong> <?php echo $has_key ? ( $from_cfg ? 'set in wp-config.php ✅' : 'saved ✅' ) : '<span style="color:#b32d2e">missing</span>'; ?></li>
				<li><strong>CSMCP tools:</strong>
					<?php
					if ( is_wp_error( $tools ) ) {
						echo '<span style="color:#b32d2e">' . esc_html( $tools->get_error_message() ) . '</span>';
					} else {
						echo esc_html( count( $tools ) . ' tools found ✅' );
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
								<p class="description">The agency's key. Site users never see it. Prefer <code>define( 'RRS_AI_API_KEY', '...' );</code> in wp-config.php.</p>
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
						<th><label for="rrs-route">CSMCP REST route</label></th>
						<td><input id="rrs-route" class="regular-text" name="<?php echo esc_attr( self::OPTION ); ?>[mcp_route]" value="<?php echo esc_attr( $o['mcp_route'] ); ?>"></td>
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
