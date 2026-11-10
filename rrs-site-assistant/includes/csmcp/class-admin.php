<?php
/**
 * WP Admin screen: CSMCP → Connect / Tools / Activity.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

class Pro_Extended_Admin {

	const SLUG     = 'pro-extended';
	const KEY_NAME = 'Claude MCP';

	public static function init() {
		add_action( 'admin_menu', array( __CLASS__, 'menu' ) );
		add_action( 'admin_init', array( __CLASS__, 'register_settings' ) );
		add_action( 'admin_init', array( __CLASS__, 'redirect_old_url' ) );
		add_filter( 'plugin_action_links_' . plugin_basename( PRO_EXTENDED_DIR . 'pro-extended.php' ), array( __CLASS__, 'action_links' ) );
	}

	public static function action_links( $links ) {
		array_unshift( $links, '<a href="' . esc_url( self::url() ) . '">' . esc_html__( 'Connect to Claude', 'pro-extended' ) . '</a>' );
		return $links;
	}

	public static function menu() {
		// Lives under Settings → CSMCP (not a top-level menu item).
		add_options_page( 'CSMCP - By Mario C', 'CSMCP', 'edit_pages', self::SLUG, array( __CLASS__, 'render' ) );
	}

	/** Old top-level URL (admin.php?page=…, before 0.7.1) → Settings → CSMCP. */
	public static function redirect_old_url() {
		global $pagenow;
		if ( 'admin.php' === $pagenow && isset( $_GET['page'] ) && self::SLUG === $_GET['page'] ) { // phpcs:ignore WordPress.Security.NonceVerification
			$args = array_map( 'sanitize_text_field', wp_unslash( $_GET ) ); // phpcs:ignore WordPress.Security.NonceVerification
			unset( $args['page'] );
			wp_safe_redirect( self::url( $args ) );
			exit;
		}
	}

	public static function register_settings() {
		register_setting(
			'pro_extended',
			Pro_Extended_Tools::OPTION_SETTINGS,
			array(
				'type'              => 'array',
				'sanitize_callback' => array( __CLASS__, 'sanitize_settings' ),
			)
		);
	}

	public static function sanitize_settings( $in ) {
		$all     = array_keys( Pro_Extended_Tools::catalog_for_admin() );
		$enabled = isset( $in['enabled'] ) ? array_map( 'sanitize_key', (array) $in['enabled'] ) : array();
		return array(
			'read_only'      => ! empty( $in['read_only'] ),
			'disabled_tools' => array_values( array_diff( $all, $enabled ) ),
		);
	}

	private static function url( $args = array() ) {
		return add_query_arg( array_merge( array( 'page' => self::SLUG ), $args ), admin_url( 'options-general.php' ) );
	}

	public static function endpoint() {
		return rest_url( Pro_Extended_MCP_Server::NS . Pro_Extended_MCP_Server::ROUTE );
	}

	/* ============================================================== render */

	public static function render() {
		if ( ! current_user_can( 'edit_pages' ) ) {
			return;
		}
		$tab  = isset( $_GET['tab'] ) ? sanitize_key( $_GET['tab'] ) : 'connect'; // phpcs:ignore WordPress.Security.NonceVerification
		$tabs = array(
			'connect'  => 'Connect',
			'tools'    => 'Tools & permissions',
			'activity' => 'Activity & backups',
		);
		echo '<div class="wrap pxe">';
		echo '<h1>CSMCP <span class="pxe-sub">By Mario C · Cornerstone MCP for Claude</span></h1>';
		self::styles();
		echo '<nav class="nav-tab-wrapper">';
		foreach ( $tabs as $k => $label ) {
			printf( '<a href="%s" class="nav-tab %s">%s</a>', esc_url( self::url( array( 'tab' => $k ) ) ), $tab === $k ? 'nav-tab-active' : '', esc_html( $label ) );
		}
		echo '</nav>';

		if ( 'tools' === $tab ) {
			self::render_tools();
		} elseif ( 'activity' === $tab ) {
			self::render_activity();
		} else {
			self::render_connect();
		}
		echo '</div>';
	}

	/* ------------------------------------------------------------- connect */

	private static function render_connect() {
		$user    = wp_get_current_user();
		$notice  = '';
		$new_key = null;

		// Handle generate / revoke on this request so the secret is shown once and never stored.
		if ( isset( $_POST['pxe_action'] ) && check_admin_referer( 'pxe_connect' ) ) {
			if ( 'generate' === $_POST['pxe_action'] ) {
				$created = WP_Application_Passwords::create_new_application_password(
					$user->ID,
					array( 'name' => self::KEY_NAME . ' — ' . wp_date( 'Y-m-d H:i' ) )
				);
				if ( is_wp_error( $created ) ) {
					$notice = '<div class="notice notice-error"><p>' . esc_html( $created->get_error_message() ) . '</p></div>';
				} else {
					$new_key = 'Basic ' . base64_encode( $user->user_login . ':' . $created[0] ); // phpcs:ignore WordPress.PHP.DiscouragedPHPFunctions
				}
			} elseif ( 'revoke' === $_POST['pxe_action'] && ! empty( $_POST['uuid'] ) ) {
				WP_Application_Passwords::delete_application_password( $user->ID, sanitize_text_field( wp_unslash( $_POST['uuid'] ) ) );
				$notice = '<div class="notice notice-success"><p>Key revoked. Anything using it is disconnected.</p></div>';
			}
		}
		echo $notice; // phpcs:ignore WordPress.Security.EscapeOutput

		$env      = Pro_Extended_Tools::call( 'cs_environment', array() );
		$cs_ok    = ! empty( $env['cornerstone_detected'] );
		$ap_ok    = wp_is_application_passwords_available_for_user( $user );
		$endpoint = self::endpoint();
		$cs_ver   = self::cornerstone_version( $env );

		echo '<div class="pxe-card"><h2>Status</h2><table class="pxe-status">';
		self::status_row( 'Cornerstone / Pro', $cs_ok, $cs_ok ? $cs_ver : 'Not detected — activate the Pro theme or Cornerstone plugin.' );
		self::status_row( 'Application Passwords', $ap_ok, $ap_ok ? 'Available' : 'Unavailable — requires HTTPS, or blocked by a security plugin.' );
		self::status_row( 'MCP endpoint', true, '<code>' . esc_html( $endpoint ) . '</code>', true );
		echo '</table></div>';

		echo '<div class="pxe-card"><h2>1. Generate a connection key</h2>';
		echo '<p>Creates a WordPress Application Password for <strong>' . esc_html( $user->user_login ) . '</strong>. Claude acts with this user\'s permissions. The key is shown once — copy it straight into Claude.</p>';
		if ( $ap_ok ) {
			echo '<form method="post">';
			wp_nonce_field( 'pxe_connect' );
			echo '<input type="hidden" name="pxe_action" value="generate"><button class="button button-primary button-hero">Generate connection key</button></form>';
		}
		echo '</div>';

		if ( $new_key ) {
			self::render_snippets( $endpoint, $new_key );
		} else {
			echo '<div class="pxe-card pxe-muted"><h2>2. Add it to Claude</h2><p>Generate a key above and the ready-to-paste setup for Claude Code and Claude Desktop appears here.</p></div>';
		}

		self::render_keys( $user );
	}

	private static function cornerstone_version( $env ) {
		if ( ! is_array( $env ) ) {
			return '';
		}
		foreach ( array( 'CS_VERSION', 'CORNERSTONE_VERSION', 'PRO_VERSION', 'X_VERSION' ) as $c ) {
			if ( isset( $env['constants'][ $c ] ) ) {
				return $c . ' ' . $env['constants'][ $c ] . ' · ' . $env['theme'];
			}
		}
		return $env['theme'];
	}

	private static function status_row( $label, $ok, $detail, $detail_is_html = false ) {
		printf(
			'<tr><td><span class="pxe-dot %s"></span>%s</td><td>%s</td></tr>',
			$ok ? 'ok' : 'bad',
			esc_html( $label ),
			$detail_is_html ? $detail : esc_html( $detail ) // phpcs:ignore WordPress.Security.EscapeOutput
		);
	}

	private static function render_snippets( $endpoint, $auth ) {
		$test = self::loopback_test( $endpoint, $auth );

		$code_cmd = sprintf( 'claude mcp add --transport http --scope user cs-mcp %s --header "Authorization: %s"', $endpoint, $auth );

		$mcp_json = wp_json_encode(
			array(
				'mcpServers' => array(
					'cs-mcp' => array(
						'type'    => 'http',
						'url'     => $endpoint,
						'headers' => array( 'Authorization' => $auth ),
					),
				),
			),
			JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES
		);

		$desktop_json = wp_json_encode(
			array(
				'mcpServers' => array(
					'cs-mcp' => array(
						'command' => 'npx',
						'args'    => array( '-y', 'mcp-remote', $endpoint, '--header', 'Authorization:${PXE_AUTH}' ),
						'env'     => array( 'PXE_AUTH' => $auth ),
					),
				),
			),
			JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES
		);

		echo '<div class="pxe-card pxe-key"><h2>2. Add it to Claude</h2>';
		if ( true === $test['ok'] ) {
			echo '<p class="pxe-test ok">✓ Connection test passed — ' . esc_html( $test['message'] ) . '</p>';
		} else {
			echo '<p class="pxe-test bad">✗ Connection test failed — ' . esc_html( $test['message'] ) . '</p>';
			if ( ! empty( $test['hint'] ) ) {
				echo '<p>' . wp_kses_post( $test['hint'] ) . '</p>';
			}
		}
		echo '<p><strong>This key is shown only once.</strong> Treat it like a password. Revoke it below at any time.</p>';

		self::snippet( 'Claude Code (terminal) — run once', $code_cmd, 'Adds the server for every project. Then start <code>claude</code> and run <code>/mcp</code> to confirm.' );
		self::snippet( 'Claude Code — or per project, in <code>.mcp.json</code>', $mcp_json, 'Keep this file out of git; it contains the key.' );
		self::snippet( 'Claude Desktop — Settings → Developer → Edit Config (<code>claude_desktop_config.json</code>)', $desktop_json, 'Merge into the existing <code>mcpServers</code> block, then fully quit and reopen Claude Desktop. Requires Node.js.' );
		echo '</div>';

		?>
		<script>
		document.querySelectorAll('.pxe-copy').forEach(function (b) {
			b.addEventListener('click', function () {
				var t = b.parentNode.querySelector('textarea');
				t.select();
				(navigator.clipboard ? navigator.clipboard.writeText(t.value) : Promise.reject()).catch(function () { document.execCommand('copy'); });
				b.textContent = 'Copied'; setTimeout(function () { b.textContent = 'Copy'; }, 1500);
			});
		});
		</script>
		<?php
	}

	private static function snippet( $title, $text, $help ) {
		$rows = min( 14, substr_count( $text, "\n" ) + 2 );
		echo '<div class="pxe-snippet"><h3>' . wp_kses_post( $title ) . '</h3>';
		echo '<textarea readonly rows="' . (int) $rows . '">' . esc_textarea( $text ) . '</textarea>';
		echo '<button type="button" class="button pxe-copy">Copy</button>';
		echo '<p class="description">' . wp_kses_post( $help ) . '</p></div>';
	}

	/** Call our own endpoint with the new key, exactly like Claude will. */
	private static function loopback_test( $endpoint, $auth ) {
		$res = wp_remote_post(
			$endpoint,
			array(
				'timeout'   => 15,
				'sslverify' => apply_filters( 'https_local_ssl_verify', false ),
				'headers'   => array(
					'Authorization' => $auth,
					'Content-Type'  => 'application/json',
					'Accept'        => 'application/json, text/event-stream',
				),
				'body'      => wp_json_encode(
					array(
						'jsonrpc' => '2.0',
						'id'      => 1,
						'method'  => 'tools/list',
					)
				),
			)
		);
		if ( is_wp_error( $res ) ) {
			return array(
				'ok'      => false,
				'message' => 'the site could not call itself (' . $res->get_error_message() . '). This is common on local/staging hosts; try connecting from Claude anyway.',
			);
		}
		$code = wp_remote_retrieve_response_code( $res );
		$body = json_decode( wp_remote_retrieve_body( $res ), true );
		if ( 200 === $code && isset( $body['result']['tools'] ) ) {
			return array(
				'ok'      => true,
				'message' => count( $body['result']['tools'] ) . ' tools available.',
			);
		}
		if ( 401 === $code ) {
			return array(
				'ok'      => false,
				'message' => 'the server rejected the key (HTTP 401).',
				'hint'    => 'Your host is probably stripping the <code>Authorization</code> header before WordPress sees it. On Apache, add this to the top of <code>.htaccess</code>:<br><code>SetEnvIf Authorization "(.*)" HTTP_AUTHORIZATION=$1</code><br>On WP Engine, ask support to pass the Authorization header through. A security plugin that disables Application Passwords can also cause this.',
			);
		}
		return array(
			'ok'      => false,
			'message' => 'HTTP ' . $code . ': ' . substr( wp_strip_all_tags( wp_remote_retrieve_body( $res ) ), 0, 200 ),
		);
	}

	private static function render_keys( $user ) {
		$keys = array_filter(
			WP_Application_Passwords::get_user_application_passwords( $user->ID ),
			function ( $k ) {
				return 0 === strpos( $k['name'], self::KEY_NAME );
			}
		);
		echo '<div class="pxe-card"><h2>Active keys</h2>';
		if ( ! $keys ) {
			echo '<p class="pxe-muted">No Claude keys for your user yet.</p></div>';
			return;
		}
		echo '<table class="widefat striped"><thead><tr><th>Name</th><th>Created</th><th>Last used</th><th></th></tr></thead><tbody>';
		foreach ( $keys as $k ) {
			echo '<tr><td>' . esc_html( $k['name'] ) . '</td><td>' . esc_html( wp_date( 'Y-m-d H:i', $k['created'] ) ) . '</td><td>' . esc_html( $k['last_used'] ? wp_date( 'Y-m-d H:i', $k['last_used'] ) : 'never' ) . '</td><td>';
			echo '<form method="post" onsubmit="return confirm(\'Revoke this key? Claude will lose access until you add a new one.\')">';
			wp_nonce_field( 'pxe_connect' );
			echo '<input type="hidden" name="pxe_action" value="revoke"><input type="hidden" name="uuid" value="' . esc_attr( $k['uuid'] ) . '"><button class="button button-link-delete">Revoke</button></form></td></tr>';
		}
		echo '</tbody></table></div>';
	}

	/* --------------------------------------------------------------- tools */

	private static function render_tools() {
		$s     = Pro_Extended_Tools::settings();
		$tools = Pro_Extended_Tools::catalog_for_admin();
		$admin = current_user_can( 'manage_options' );

		echo '<form method="post" action="options.php">';
		settings_fields( 'pro_extended' );
		$opt = Pro_Extended_Tools::OPTION_SETTINGS;

		echo '<div class="pxe-card"><h2>Safety</h2><label><input type="checkbox" name="' . esc_attr( $opt ) . '[read_only]" value="1" ' . checked( $s['read_only'], true, false ) . ( $admin ? '' : ' disabled' ) . '> <strong>Read-only mode</strong> — Claude can inspect the site but every tool that changes something is switched off.</label>';
		echo '<p class="description">Regardless of this setting: new pages are created as drafts, every page change is backed up first, and Claude can only do what the connected user can do.</p></div>';

		echo '<div class="pxe-card"><h2>Tools</h2><table class="widefat striped"><thead><tr><th style="width:3em">On</th><th>Tool</th><th>What it does</th><th>Type</th></tr></thead><tbody>';
		foreach ( $tools as $name => $t ) {
			$on = ! in_array( $name, (array) $s['disabled_tools'], true );
			printf(
				'<tr><td><input type="checkbox" name="%s[enabled][]" value="%s" %s %s></td><td><code>%s</code></td><td>%s</td><td>%s</td></tr>',
				esc_attr( $opt ),
				esc_attr( $name ),
				checked( $on, true, false ),
				$admin ? '' : 'disabled',
				esc_html( $name ),
				esc_html( $t['description'] ),
				$t['write'] ? '<span class="pxe-tag w">writes</span>' : '<span class="pxe-tag r">read</span>'
			);
		}
		echo '</tbody></table></div>';
		if ( $admin ) {
			submit_button( 'Save' );
		} else {
			echo '<p class="pxe-muted">Only administrators can change these settings.</p>';
		}
		echo '</form>';
		echo '<p class="pxe-muted">Changes apply immediately; in Claude Code, reconnect the server (<code>/mcp</code>) to refresh the tool list.</p>';
	}

	/* ------------------------------------------------------------ activity */

	private static function render_activity() {
		$post_id = isset( $_GET['post'] ) ? (int) $_GET['post'] : 0; // phpcs:ignore WordPress.Security.NonceVerification

		if ( $post_id && isset( $_POST['pxe_restore'] ) && check_admin_referer( 'pxe_restore_' . $post_id ) && current_user_can( 'edit_post', $post_id ) ) {
			$r = Pro_Extended_Tools::call(
				'cs_restore_backup',
				array(
					'id'    => $post_id,
					'index' => (int) $_POST['pxe_restore'],
				)
			);
			echo is_wp_error( $r )
				? '<div class="notice notice-error"><p>' . esc_html( $r->get_error_message() ) . '</p></div>'
				: '<div class="notice notice-success"><p>Restored. The state before the restore was backed up too.</p></div>';
		}

		if ( $post_id ) {
			self::render_backups( $post_id );
			return;
		}

		$log = Pro_Extended_Tools::get_log();
		echo '<div class="pxe-card"><h2>Recent changes made through Claude</h2>';
		if ( ! $log ) {
			echo '<p class="pxe-muted">Nothing yet.</p></div>';
			return;
		}
		echo '<table class="widefat striped"><thead><tr><th>When</th><th>User</th><th>Tool</th><th>Page</th><th>What happened</th><th></th></tr></thead><tbody>';
		foreach ( $log as $e ) {
			$u    = get_userdata( $e['user'] );
			$post = $e['post_id'] ? get_post( $e['post_id'] ) : null;
			echo '<tr><td>' . esc_html( wp_date( 'Y-m-d H:i', strtotime( $e['time'] ) ) ) . '</td>';
			echo '<td>' . esc_html( $u ? $u->user_login : '#' . $e['user'] ) . '</td>';
			echo '<td><code>' . esc_html( $e['tool'] ) . '</code></td>';
			echo '<td>' . ( $post ? '<a href="' . esc_url( get_edit_post_link( $post->ID ) ) . '">' . esc_html( $post->post_title ? $post->post_title : '#' . $post->ID ) . '</a>' : '—' ) . '</td>';
			echo '<td>' . esc_html( $e['summary'] ) . '</td>';
			echo '<td>' . ( $post ? '<a class="button button-small" href="' . esc_url( self::url( array( 'tab' => 'activity', 'post' => $post->ID ) ) ) . '">Backups</a>' : '' ) . '</td></tr>';
		}
		echo '</tbody></table></div>';
	}

	private static function render_backups( $post_id ) {
		$post    = get_post( $post_id );
		$backups = Pro_Extended_CS_Store::list_backups( $post_id );
		echo '<p><a href="' . esc_url( self::url( array( 'tab' => 'activity' ) ) ) . '">← All activity</a></p>';
		echo '<div class="pxe-card"><h2>Backups — ' . esc_html( $post ? $post->post_title : '#' . $post_id ) . '</h2>';
		echo '<p class="description">A snapshot is taken automatically before every change Claude makes (the last ' . (int) Pro_Extended_CS_Store::MAX_BACKUPS . ' are kept). Restoring puts the page back exactly as it was at that moment.</p>';
		if ( ! $backups ) {
			echo '<p class="pxe-muted">No backups for this page.</p></div>';
			return;
		}
		echo '<table class="widefat striped"><thead><tr><th>Taken</th><th>Before</th><th></th></tr></thead><tbody>';
		foreach ( $backups as $b ) {
			echo '<tr><td>' . esc_html( wp_date( 'Y-m-d H:i:s', strtotime( $b['time'] ) ) ) . '</td><td><code>' . esc_html( $b['reason'] ) . '</code></td><td>';
			echo '<form method="post" onsubmit="return confirm(\'Restore this version of the page?\')">';
			wp_nonce_field( 'pxe_restore_' . $post_id );
			echo '<button class="button" name="pxe_restore" value="' . (int) $b['index'] . '">Restore</button></form></td></tr>';
		}
		echo '</tbody></table></div>';
	}

	/* -------------------------------------------------------------- styles */

	private static function styles() {
		?>
		<style>
		.pxe .pxe-sub{font-size:13px;font-weight:400;color:#646970;margin-left:8px}
		.pxe .pxe-card{background:#fff;border:1px solid #dcdcde;border-radius:6px;padding:16px 20px;margin:16px 0;max-width:980px}
		.pxe .pxe-card h2{margin-top:0}
		.pxe .pxe-muted{color:#646970}
		.pxe .pxe-status td{padding:4px 16px 4px 0}
		.pxe .pxe-dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:8px;background:#d63638}
		.pxe .pxe-dot.ok{background:#00a32a}
		.pxe .pxe-key{border-color:#2271b1;box-shadow:0 0 0 1px #2271b1}
		.pxe .pxe-test{font-weight:600}.pxe .pxe-test.ok{color:#00a32a}.pxe .pxe-test.bad{color:#d63638}
		.pxe .pxe-snippet{margin:18px 0}.pxe .pxe-snippet h3{font-size:13px;margin:0 0 6px}
		.pxe .pxe-snippet textarea{width:100%;font-family:Menlo,Consolas,monospace;font-size:12px;background:#f6f7f7}
		.pxe .pxe-snippet .pxe-copy{margin-top:4px}
		.pxe .pxe-tag{font-size:11px;padding:2px 6px;border-radius:3px}
		.pxe .pxe-tag.r{background:#e7f5ea;color:#00692a}.pxe .pxe-tag.w{background:#fcf0e3;color:#8a4b00}
		</style>
		<?php
	}
}
