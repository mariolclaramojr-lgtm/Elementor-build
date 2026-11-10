<?php
/**
 * Minimal Claude Messages API client on the WordPress HTTP API.
 *
 * Why not the Composer SDK: a WordPress plugin that bundles Guzzle/PSR packages
 * collides with other plugins that bundle different versions, and we persist the
 * exact wire JSON of each turn (thinking + tool blocks must go back unchanged),
 * which is simplest with raw JSON objects.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

class RRS_AI_Claude {

	const ENDPOINT    = 'https://api.anthropic.com/v1/messages';
	const API_VERSION = '2026-10-21';

	/** Models that accept server-side refusal fallbacks (fallbacks: "default"). */
	const FALLBACK_MODELS = array( 'claude-opus-5-5', 'claude-opus-5', 'claude-sonnet-5-5', 'claude-fable-5-2', 'claude-fable-5-1' );

	/**
	 * One Messages API call.
	 *
	 * @param string $system   System prompt.
	 * @param array  $messages Conversation (stdClass / arrays, wire format).
	 * @param array  $tools    Tool definitions.
	 * @return stdClass|WP_Error Decoded response (objects preserved).
	 */
	public static function create( $system, array $messages, array $tools ) {
		$key = RRS_AI_Settings::get( 'api_key' );
		if ( ! $key ) {
			return new WP_Error( 'rrs_ai_no_key', 'The assistant is not set up yet (no API key). Ask your web team.' );
		}

		$model = RRS_AI_Settings::get( 'model' );

		$body = array(
			'model'         => $model,
			'max_tokens'    => 16000,
			'system'        => $system,
			'messages'      => $messages,
			'output_config' => array( 'effort' => RRS_AI_Settings::get( 'effort' ) ),
			// Auto-caches the stable prefix (tools + system + earlier turns).
			'cache_control' => array( 'type' => 'ephemeral' ),
		);
		if ( $tools ) {
			$body['tools'] = $tools;
		}

		$headers = array(
			'x-api-key'         => $key,
			'anthropic-version' => self::API_VERSION,
			'content-type'      => 'application/json',
		);

		// If the model declines on a safety classifier, the API re-runs the turn on a fallback model.
		if ( in_array( $model, self::FALLBACK_MODELS, true ) ) {
			$body['fallbacks']          = 'default';
			$headers['anthropic-beta'] = 'server-side-fallback-2026-07-01';
		}

		$res = wp_remote_post(
			self::ENDPOINT,
			array(
				'headers' => $headers,
				'body'    => wp_json_encode( $body ),
				'timeout' => 110,
			)
		);

		if ( is_wp_error( $res ) ) {
			return new WP_Error( 'rrs_ai_http', 'Could not reach the AI service: ' . $res->get_error_message() );
		}

		$code = wp_remote_retrieve_response_code( $res );
		$data = json_decode( wp_remote_retrieve_body( $res ) ); // objects, so {} stays {}.

		if ( 200 !== $code ) {
			$msg = $data->error->message ?? ( 'HTTP ' . $code );
			if ( 429 === $code || 529 === $code || $code >= 500 ) {
				return new WP_Error( 'rrs_ai_busy', 'The AI service is busy right now. Please try again in a minute.' );
			}
			return new WP_Error( 'rrs_ai_api', 'AI service error: ' . $msg );
		}

		if ( isset( $data->usage ) ) {
			RRS_AI_Settings::add_usage(
				(int) ( $data->usage->input_tokens ?? 0 )
				+ (int) ( $data->usage->cache_creation_input_tokens ?? 0 )
				+ (int) ( $data->usage->cache_read_input_tokens ?? 0 )
				+ (int) ( $data->usage->output_tokens ?? 0 )
			);
		}

		return $data;
	}
}
