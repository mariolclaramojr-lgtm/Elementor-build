<?php
/**
 * Minimal MCP (Model Context Protocol) server over the WordPress REST API.
 *
 * Implements the Streamable HTTP transport in JSON-response mode: every client
 * message is a POST, every request gets a single JSON-RPC response, and
 * notifications get an empty 202. No SSE stream is opened.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

class Pro_Extended_MCP_Server {

	const NS       = 'cs-mcp/v1';
	const ROUTE    = '/mcp';
	const VERSIONS = array( '2025-06-18', '2025-03-26', '2024-11-05' );

	public static function register_routes() {
		register_rest_route(
			self::NS,
			self::ROUTE,
			array(
				array(
					'methods'             => 'POST',
					'callback'            => array( __CLASS__, 'handle_post' ),
					'permission_callback' => array( __CLASS__, 'can_access' ),
				),
				array(
					// Streamable HTTP clients may try GET (SSE) or DELETE (end session); we support neither.
					'methods'             => array( 'GET', 'DELETE' ),
					'callback'            => function () {
						return new WP_REST_Response( array( 'error' => 'Method not allowed' ), 405 );
					},
					'permission_callback' => '__return_true',
				),
			)
		);
	}

	public static function can_access() {
		if ( ! is_user_logged_in() ) {
			return new WP_Error( 'pro_extended_unauthorized', 'Authenticate with a WordPress Application Password (HTTP Basic).', array( 'status' => 401 ) );
		}
		if ( ! current_user_can( 'edit_pages' ) ) {
			return new WP_Error( 'pro_extended_forbidden', 'This user cannot edit pages.', array( 'status' => 403 ) );
		}
		return true;
	}

	public static function handle_post( WP_REST_Request $request ) {
		$body = json_decode( $request->get_body(), true );
		if ( null === $body ) {
			return new WP_REST_Response( self::error( null, -32700, 'Parse error' ), 400 );
		}

		// JSON-RPC batch (older protocol versions).
		if ( is_array( $body ) && array_keys( $body ) === range( 0, count( $body ) - 1 ) ) {
			$out = array();
			foreach ( $body as $msg ) {
				$res = self::dispatch( $msg );
				if ( null !== $res ) {
					$out[] = $res;
				}
			}
			return $out ? new WP_REST_Response( $out, 200 ) : new WP_REST_Response( null, 202 );
		}

		$res = self::dispatch( $body );
		return null === $res ? new WP_REST_Response( null, 202 ) : new WP_REST_Response( $res, 200 );
	}

	/** Returns a JSON-RPC response array, or null for notifications/responses. */
	private static function dispatch( $msg ) {
		if ( ! is_array( $msg ) || ! isset( $msg['method'] ) ) {
			return null; // Client responses or junk: nothing to answer.
		}
		$has_id = array_key_exists( 'id', $msg );
		$id     = $has_id ? $msg['id'] : null;
		$params = isset( $msg['params'] ) && is_array( $msg['params'] ) ? $msg['params'] : array();

		if ( ! $has_id ) {
			return null; // notifications/initialized, notifications/cancelled, ...
		}

		switch ( $msg['method'] ) {
			case 'initialize':
				$requested = isset( $params['protocolVersion'] ) ? $params['protocolVersion'] : '';
				return self::result(
					$id,
					array(
						'protocolVersion' => in_array( $requested, self::VERSIONS, true ) ? $requested : self::VERSIONS[0],
						'capabilities'    => array( 'tools' => (object) array() ),
						'serverInfo'      => array(
							'name'    => 'csmcp',
							'version' => PRO_EXTENDED_VERSION,
						),
						'instructions'    => Pro_Extended_Tools::instructions(),
					)
				);

			case 'ping':
				return self::result( $id, (object) array() );

			case 'tools/list':
				return self::result( $id, array( 'tools' => Pro_Extended_Tools::definitions() ) );

			case 'tools/call':
				$name = isset( $params['name'] ) ? (string) $params['name'] : '';
				$args = isset( $params['arguments'] ) && is_array( $params['arguments'] ) ? $params['arguments'] : array();
				if ( ! Pro_Extended_Tools::exists( $name ) ) {
					return self::error( $id, -32602, 'Unknown tool: ' . $name );
				}
				try {
					$data = Pro_Extended_Tools::call( $name, $args );
					if ( is_wp_error( $data ) ) {
						return self::result( $id, self::tool_text( array( 'error' => $data->get_error_message() ), true ) );
					}
					return self::result( $id, self::tool_text( $data, false ) );
				} catch ( Throwable $e ) {
					return self::result( $id, self::tool_text( array( 'error' => $e->getMessage() ), true ) );
				}

			case 'resources/list':
				return self::result( $id, array( 'resources' => array() ) );

			case 'prompts/list':
				return self::result( $id, array( 'prompts' => array() ) );

			default:
				return self::error( $id, -32601, 'Method not found: ' . $msg['method'] );
		}
	}

	private static function tool_text( $data, $is_error ) {
		return array(
			'content' => array(
				array(
					'type' => 'text',
					'text' => is_string( $data ) ? $data : wp_json_encode( $data, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE ),
				),
			),
			'isError' => $is_error,
		);
	}

	private static function result( $id, $result ) {
		return array(
			'jsonrpc' => '2.0',
			'id'      => $id,
			'result'  => $result,
		);
	}

	private static function error( $id, $code, $message ) {
		return array(
			'jsonrpc' => '2.0',
			'id'      => $id,
			'error'   => array(
				'code'    => $code,
				'message' => $message,
			),
		);
	}
}
