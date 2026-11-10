<?php
/**
 * Exposes the bundled CSMCP tools to the chat: direct PHP calls, as the logged-in user.
 * Tools switched off (or read-only mode) in Settings → CSMCP are hidden here too.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

class RRS_AI_Tools_Bridge {

	const MAX_RESULT_LEN = 80000; // characters of tool output passed back to the model.

	/** @return array|WP_Error Tool definitions in Claude API format. */
	public static function list_tools() {
		if ( ! class_exists( 'Pro_Extended_Tools' ) ) {
			return new WP_Error( 'rrs_ai_no_tools', 'The Cornerstone tools did not load.' );
		}
		$tools = array();
		foreach ( Pro_Extended_Tools::definitions() as $t ) {
			$tools[] = array(
				'name'         => $t['name'],
				'description'  => $t['description'],
				'input_schema' => self::objectify( $t['inputSchema'] ),
			);
		}
		return $tools;
	}

	/**
	 * Run one tool.
	 *
	 * @param string $name  Tool name.
	 * @param mixed  $input Tool input as the model sent it (stdClass).
	 * @return array{content: array, is_error: bool}
	 */
	public static function call_tool( $name, $input ) {
		if ( ! Pro_Extended_Tools::exists( $name ) ) {
			return self::text( 'Unknown or disabled tool: ' . $name, true );
		}
		// Same decoding the MCP endpoint does (json_decode(..., true)).
		$args = json_decode( wp_json_encode( $input ), true );
		$args = is_array( $args ) ? $args : array();

		try {
			$data = Pro_Extended_Tools::call( $name, $args );
		} catch ( Throwable $e ) {
			return self::text( wp_json_encode( array( 'error' => $e->getMessage() ) ), true );
		}
		if ( is_wp_error( $data ) ) {
			return self::text( wp_json_encode( array( 'error' => $data->get_error_message() ) ), true );
		}

		$text = is_string( $data ) ? $data : wp_json_encode( $data, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE );
		if ( strlen( $text ) > self::MAX_RESULT_LEN ) {
			$text = substr( $text, 0, self::MAX_RESULT_LEN ) . "\n\n[Output truncated at " . self::MAX_RESULT_LEN . ' characters. Ask for a narrower result (one page, one element path) if you need the rest.]';
		}
		return self::text( $text, false );
	}

	private static function text( $text, $is_error ) {
		return array(
			'content'  => array( array( 'type' => 'text', 'text' => (string) $text ) ),
			'is_error' => $is_error,
		);
	}

	/** Empty PHP arrays in a JSON Schema must be sent as {} where an object is expected. */
	private static function objectify( $node ) {
		if ( ! is_array( $node ) ) {
			return $node;
		}
		foreach ( $node as $k => $v ) {
			if ( in_array( $k, array( 'properties', 'patternProperties', '$defs', 'definitions' ), true ) && ( is_array( $v ) || is_object( $v ) ) ) {
				$out = new stdClass();
				foreach ( (array) $v as $pk => $ps ) {
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
