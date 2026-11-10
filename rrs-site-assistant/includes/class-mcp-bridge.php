<?php
/**
 * Talks to the CSMCP plugin's MCP endpoint *inside* WordPress (rest_do_request),
 * as the logged-in user. No HTTP loopback, no application password, nothing exposed.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

class RRS_AI_MCP_Bridge {

	const TOOLS_CACHE    = 'rrs_ai_tools';
	const MAX_RESULT_LEN = 80000; // characters of tool output passed back to the model.

	private static $session_id = null;
	private static $rpc_id     = 0;

	/** Claude-safe tool name => original MCP tool name. */
	private static $name_map = array();

	/**
	 * Tool definitions in Claude API format.
	 *
	 * @return array|WP_Error
	 */
	public static function list_tools( $fresh = false ) {
		$cached = $fresh ? false : get_transient( self::TOOLS_CACHE );
		if ( is_array( $cached ) ) {
			self::$name_map = $cached['map'];
			return $cached['tools'];
		}

		$result = self::rpc( 'tools/list', new stdClass() );
		if ( is_wp_error( $result ) ) {
			return $result;
		}
		if ( empty( $result['tools'] ) || ! is_array( $result['tools'] ) ) {
			return new WP_Error( 'rrs_ai_no_tools', 'CSMCP answered but listed no tools.' );
		}

		$tools = array();
		$map   = array();
		foreach ( $result['tools'] as $t ) {
			if ( empty( $t['name'] ) ) {
				continue;
			}
			$safe         = substr( preg_replace( '/[^a-zA-Z0-9_-]/', '_', $t['name'] ), 0, 64 );
			$map[ $safe ] = $t['name'];
			$tools[]      = array(
				'name'         => $safe,
				'description'  => (string) ( $t['description'] ?? '' ),
				'input_schema' => self::normalize_schema( $t['inputSchema'] ?? array() ),
			);
		}

		self::$name_map = $map;
		set_transient( self::TOOLS_CACHE, array( 'tools' => $tools, 'map' => $map ), HOUR_IN_SECONDS );
		return $tools;
	}

	/**
	 * Run one tool. Returns Claude tool_result content blocks and an error flag.
	 *
	 * @param string   $name  Claude-side tool name.
	 * @param stdClass $input Tool input exactly as the model sent it.
	 * @return array{content: array, is_error: bool}
	 */
	public static function call_tool( $name, $input ) {
		if ( empty( self::$name_map ) ) {
			self::list_tools();
		}
		$mcp_name = self::$name_map[ $name ] ?? $name;

		$result = self::rpc(
			'tools/call',
			(object) array(
				'name'      => $mcp_name,
				'arguments' => is_object( $input ) ? $input : (object) $input,
			)
		);

		if ( is_wp_error( $result ) ) {
			return array(
				'content'  => array( array( 'type' => 'text', 'text' => 'Tool error: ' . $result->get_error_message() ) ),
				'is_error' => true,
			);
		}

		$blocks = array();
		$budget = self::MAX_RESULT_LEN;
		foreach ( (array) ( $result['content'] ?? array() ) as $c ) {
			$type = $c['type'] ?? '';
			if ( 'text' === $type ) {
				$text = (string) $c['text'];
				if ( strlen( $text ) > $budget ) {
					$text = substr( $text, 0, max( 0, $budget ) ) . "\n\n[Output truncated by the assistant plugin at " . self::MAX_RESULT_LEN . ' characters. Ask the tool for a narrower result (one page, one element path) if you need the rest.]';
				}
				$budget  -= strlen( $text );
				$blocks[] = array( 'type' => 'text', 'text' => $text );
			} elseif ( 'image' === $type && ! empty( $c['data'] ) ) {
				$blocks[] = array(
					'type'   => 'image',
					'source' => array(
						'type'       => 'base64',
						'media_type' => $c['mimeType'] ?? 'image/png',
						'data'       => $c['data'],
					),
				);
			}
		}
		if ( ! $blocks && isset( $result['structuredContent'] ) ) {
			$blocks[] = array( 'type' => 'text', 'text' => substr( wp_json_encode( $result['structuredContent'] ), 0, self::MAX_RESULT_LEN ) );
		}
		if ( ! $blocks ) {
			$blocks[] = array( 'type' => 'text', 'text' => '(no output)' );
		}

		return array(
			'content'  => $blocks,
			'is_error' => ! empty( $result['isError'] ),
		);
	}

	/* ---------------------------------------------------------------- */

	/**
	 * One JSON-RPC call to the CSMCP endpoint, in-process.
	 *
	 * @return array|WP_Error The JSON-RPC "result" member.
	 */
	private static function rpc( $method, $params ) {
		if ( null === self::$session_id && 'initialize' !== $method ) {
			$init = self::rpc(
				'initialize',
				(object) array(
					'protocolVersion' => '2025-06-18',
					'capabilities'    => new stdClass(),
					'clientInfo'      => array( 'name' => 'rrs-site-assistant', 'version' => RRS_AI_VERSION ),
				)
			);
			// A server that rejects "initialize" as a method can still serve tools; anything else is fatal.
			if ( is_wp_error( $init ) && 'rrs_ai_mcp_error' !== $init->get_error_code() ) {
				return $init;
			}
			self::$session_id = self::$session_id ?? '';
			self::send( array( 'jsonrpc' => '2.0', 'method' => 'notifications/initialized' ) );
		}

		$payload = array(
			'jsonrpc' => '2.0',
			'id'      => ++self::$rpc_id,
			'method'  => $method,
			'params'  => $params,
		);

		$data = self::send( $payload );
		if ( is_wp_error( $data ) ) {
			return $data;
		}
		if ( isset( $data['error'] ) ) {
			return new WP_Error( 'rrs_ai_mcp_error', $data['error']['message'] ?? 'MCP error' );
		}
		if ( ! array_key_exists( 'result', $data ) ) {
			return new WP_Error( 'rrs_ai_mcp_bad', 'Unexpected reply from CSMCP for ' . $method . '.' );
		}
		return (array) $data['result'];
	}

	/** @return array|WP_Error Decoded JSON-RPC message. */
	private static function send( array $payload ) {
		$route = RRS_AI_Settings::get( 'mcp_route' );

		$req = new WP_REST_Request( 'POST', $route );
		$req->set_header( 'Content-Type', 'application/json' );
		$req->set_header( 'Accept', 'application/json, text/event-stream' );
		if ( self::$session_id ) {
			$req->set_header( 'Mcp-Session-Id', self::$session_id );
		}
		$req->set_body( wp_json_encode( $payload ) );

		$res = rest_do_request( $req );

		if ( 'initialize' === ( $payload['method'] ?? '' ) ) {
			foreach ( $res->get_headers() as $k => $v ) {
				if ( 0 === strcasecmp( $k, 'Mcp-Session-Id' ) ) {
					self::$session_id = (string) $v;
				}
			}
		}

		$status = $res->get_status();
		$data   = rest_get_server()->response_to_data( $res, false );

		if ( 404 === $status && isset( $data['code'] ) && 'rest_no_route' === $data['code'] ) {
			return new WP_Error( 'rrs_ai_no_csmcp', 'CSMCP is not active (no route ' . $route . '). Install/activate the CSMCP plugin.' );
		}
		if ( $status >= 400 ) {
			$msg = is_array( $data ) ? ( $data['message'] ?? $data['error']['message'] ?? wp_json_encode( $data ) ) : (string) $data;
			return new WP_Error( 'rrs_ai_mcp_http', 'CSMCP returned HTTP ' . $status . ': ' . $msg );
		}

		// Notifications have no reply.
		if ( ! isset( $payload['id'] ) ) {
			return array();
		}

		// Some servers answer with an SSE body instead of JSON.
		if ( is_string( $data ) ) {
			$decoded = null;
			foreach ( preg_split( '/\r?\n/', $data ) as $line ) {
				if ( 0 === strpos( $line, 'data:' ) ) {
					$try = json_decode( trim( substr( $line, 5 ) ), true );
					if ( is_array( $try ) && isset( $try['id'] ) ) {
						$decoded = $try;
					}
				}
			}
			if ( null === $decoded ) {
				$decoded = json_decode( $data, true );
			}
			$data = $decoded;
		}

		// A batch reply: pick ours.
		if ( is_array( $data ) && isset( $data[0] ) && is_array( $data[0] ) ) {
			foreach ( $data as $m ) {
				if ( ( $m['id'] ?? null ) === $payload['id'] ) {
					$data = $m;
					break;
				}
			}
		}

		if ( ! is_array( $data ) ) {
			return new WP_Error( 'rrs_ai_mcp_bad', 'Could not read the reply from CSMCP.' );
		}
		return $data;
	}

	/** Make a tool schema valid JSON Schema for the API (empty PHP arrays -> objects). */
	private static function normalize_schema( $schema ) {
		$schema = is_array( $schema ) ? $schema : array();
		if ( empty( $schema['type'] ) ) {
			$schema['type'] = 'object';
		}
		return self::objectify( $schema );
	}

	private static function objectify( $node ) {
		if ( ! is_array( $node ) ) {
			return $node;
		}
		foreach ( $node as $k => $v ) {
			if ( in_array( $k, array( 'properties', 'patternProperties', '$defs', 'definitions' ), true ) && is_array( $v ) ) {
				// Map of name => schema; an empty schema {} must stay an object.
				$out = new stdClass();
				foreach ( $v as $pk => $ps ) {
					$out->{$pk} = ( is_array( $ps ) && empty( $ps ) ) ? new stdClass() : self::objectify( $ps );
				}
				$node[ $k ] = $out;
			} elseif ( in_array( $k, array( 'items', 'additionalProperties' ), true ) && is_array( $v ) && empty( $v ) ) {
				$node[ $k ] = new stdClass();
			} elseif ( is_array( $v ) ) {
				$node[ $k ] = self::objectify( $v );
			}
		}
		return $node;
	}
}
