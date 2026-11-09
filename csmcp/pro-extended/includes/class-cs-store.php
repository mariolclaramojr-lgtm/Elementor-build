<?php
/**
 * Read/write layer for Cornerstone page data.
 *
 * Cornerstone keeps a page's builder document in post meta (`_cornerstone_data`,
 * a JSON element tree, plus `_cornerstone_settings` etc.). The exact element
 * schema varies between Cornerstone/Pro versions, so this class never assumes a
 * schema beyond "elements have a `_type` and children live in `_modules`" —
 * everything else is learned from the live site via the catalog tools.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

class Pro_Extended_CS_Store {

	const DATA_KEY     = '_cornerstone_data';
	const SETTINGS_KEY = '_cornerstone_settings';
	const BACKUP_KEY   = '_pro_extended_backups';
	const MAX_BACKUPS  = 10;

	/** Keys that may hold child elements, in order of preference. */
	const CHILD_KEYS = array( '_modules', 'elements', 'children' );

	/** Meta keys considered part of a page's Cornerstone state. */
	public static function is_cs_meta_key( $key ) {
		return (bool) preg_match( '/^_(cornerstone|cs_|x_|pro_)/', $key ) && self::BACKUP_KEY !== $key;
	}

	/** All Cornerstone-related meta for a post, JSON-decoded where possible. */
	public static function get_cs_meta( $post_id ) {
		$out = array();
		foreach ( get_post_meta( $post_id ) as $key => $values ) {
			if ( ! self::is_cs_meta_key( $key ) ) {
				continue;
			}
			$out[ $key ] = self::decode( maybe_unserialize( $values[0] ) );
		}
		ksort( $out );
		return $out;
	}

	public static function decode( $value ) {
		if ( is_string( $value ) && '' !== $value && ( '{' === $value[0] || '[' === $value[0] ) ) {
			$decoded = json_decode( $value, true );
			if ( JSON_ERROR_NONE === json_last_error() ) {
				return $decoded;
			}
		}
		return $value;
	}

	/** The element tree, or null when the post has never been built with Cornerstone. */
	public static function get_tree( $post_id ) {
		$raw = get_post_meta( $post_id, self::DATA_KEY, true );
		if ( '' === $raw || null === $raw ) {
			return null;
		}
		$tree = self::decode( $raw );
		return is_array( $tree ) ? $tree : null;
	}

	/** True when the stored data is a JSON string (vs. a PHP-serialized array). */
	private static function stored_as_json( $post_id ) {
		$raw = get_post_meta( $post_id, self::DATA_KEY, true );
		return '' === $raw || is_string( $raw );
	}

	/**
	 * Write a meta value. JSON strings must be wp_slash()ed, because
	 * update_post_meta() unslashes its input and would otherwise strip the
	 * backslashes out of escaped quotes/newlines and corrupt the JSON.
	 */
	public static function put_meta( $post_id, $key, $value, $as_json = true ) {
		if ( is_array( $value ) && $as_json ) {
			$value = wp_json_encode( $value, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE );
		}
		update_post_meta( $post_id, $key, wp_slash( $value ) );
	}

	/**
	 * Save an element tree. Prefers Cornerstone's own document pipeline
	 * (Content::update + save), which also rebuilds the shortcode copy in
	 * post_content, clears the compiled CSS (_cs_generated_tss) and fires
	 * cs_save_document — exactly what the builder's Save button does.
	 * Falls back to a raw meta write for non-content documents.
	 *
	 * @return string|WP_Error 'cornerstone' or 'raw'.
	 */
	public static function save_tree( $post_id, array $tree ) {
		$elements = isset( $tree['_type'] ) ? self::roots( $tree ) : array_values( $tree );
		$via      = self::save_via_cornerstone( $post_id, array( 'elements' => $elements ) );
		if ( is_wp_error( $via ) || true === $via ) {
			return is_wp_error( $via ) ? $via : 'cornerstone';
		}
		self::put_meta( $post_id, self::DATA_KEY, $tree, self::stored_as_json( $post_id ) );
		delete_post_meta( $post_id, '_cs_generated_tss' );
		return 'raw';
	}

	/**
	 * Run an update through Cornerstone's Content document. Returns true on
	 * success, false when the pipeline isn't available for this post, or a
	 * WP_Error when Cornerstone rejected the save.
	 */
	public static function save_via_cornerstone( $post_id, array $update ) {
		$document = 'Themeco\\Cornerstone\\Documents\\Document';
		$content  = 'Themeco\\Cornerstone\\Documents\\Content';
		if ( ! class_exists( $document ) || ! class_exists( $content ) ) {
			return false;
		}
		try {
			$doc = $document::locate( (int) $post_id );
			if ( ! $doc || ! ( $doc instanceof $content ) ) {
				return false; // Headers, footers, layouts, components: different document classes.
			}
			// Content::save() reads elements from data['elements']['data'], which only update()
			// sets — so elements must always be passed or the page would be emptied.
			if ( ! isset( $update['elements'] ) ) {
				$update['elements'] = self::roots_of( self::get_tree( $post_id ) );
			}
			$updated = $doc->update( $update ); // The builder uses the returned object; some updates swap it.
			$doc     = is_object( $updated ) ? $updated : $doc;
			$res = $doc->save();
			return is_wp_error( $res ) ? $res : true;
		} catch ( Throwable $e ) {
			return new WP_Error( 'cornerstone_save_failed', 'Cornerstone save failed: ' . $e->getMessage() );
		}
	}

	/**
	 * Create or update a Pro layout document (header/footer/layout) through
	 * Cornerstone's Layout document: update() then save(), exactly like the
	 * builder. Layouts keep their data as JSON in post_content
	 * ({settings, regions}) with post_status "tco-data".
	 *
	 * @param int|null $id      Existing document ID, or null to create.
	 * @param string   $doctype 'layout:header' | 'layout:footer' (used when creating).
	 * @param array    $update  ['title' => ..., 'settings' => [...], 'elements' => [region => [...]]]
	 * @return array|WP_Error   Cornerstone's serialized document (has 'id').
	 */
	public static function save_layout( $id, $doctype, array $update ) {
		$document = 'Themeco\\Cornerstone\\Documents\\Document';
		$layout   = 'Themeco\\Cornerstone\\Documents\\Layout';
		if ( ! class_exists( $document ) ) {
			return new WP_Error( 'no_cornerstone', 'Cornerstone document classes not available.' );
		}
		try {
			$doc = $id ? $document::locate( (int) $id ) : $document::create( $doctype );
			if ( ! $doc || ! ( $doc instanceof $layout ) ) {
				return new WP_Error( 'not_layout', 'Post ' . $id . ' is not a Cornerstone header/footer/layout.' );
			}
			$updated = $doc->update( $update ); // The builder uses the returned object; some updates swap it.
			$doc     = is_object( $updated ) ? $updated : $doc;
			$res = $doc->save();
			return is_wp_error( $res ) ? $res : $res;
		} catch ( Throwable $e ) {
			return new WP_Error( 'cornerstone_save_failed', 'Cornerstone save failed: ' . $e->getMessage() );
		}
	}

	/**
	 * Create or update a Cornerstone Component (post type cs_global_block,
	 * status tco-data) through its Component document, like the builder.
	 * Components keep elements FLAT: {e0: root, e1: content region, eN: ...}
	 * with `_modules` = child ids and `_parent` = parent id. $roots is the
	 * usual nested tree (list of top-level elements with nested _modules).
	 *
	 * @return array|WP_Error Cornerstone's serialized document (has 'id').
	 */
	public static function save_component( $id, $title, array $roots, $settings = null ) {
		$document  = 'Themeco\\Cornerstone\\Documents\\Document';
		$component = 'Themeco\\Cornerstone\\Documents\\Component';
		if ( ! class_exists( $document ) || ! class_exists( $component ) ) {
			return new WP_Error( 'no_cornerstone', 'Cornerstone component documents not available.' );
		}
		$flat = array(
			'e0' => array( '_type' => 'root', '_modules' => array( 'e1' ) ),
			'e1' => array( '_type' => 'region', '_region' => 'content', '_modules' => array(), '_parent' => 'e0' ),
		);
		$n    = 1;
		$walk = function ( $el, $parent ) use ( &$walk, &$flat, &$n ) {
			$eid      = 'e' . ( ++$n );
			$children = isset( $el['_modules'] ) && is_array( $el['_modules'] ) ? $el['_modules'] : array();
			unset( $el['_id'] );
			$el['_modules'] = array();
			$el['_parent']  = $parent;
			$el['_region']  = 'content';
			$flat[ $eid ]   = $el;
			foreach ( $children as $child ) {
				$flat[ $eid ]['_modules'][] = $walk( $child, $eid );
			}
			return $eid;
		};
		foreach ( array_values( $roots ) as $root ) {
			$flat['e1']['_modules'][] = $walk( $root, 'e1' );
		}
		try {
			$doc = $id ? $document::locate( (int) $id ) : $document::create( 'custom:component' );
			if ( ! $doc || ! ( $doc instanceof $component ) ) {
				return new WP_Error( 'not_component', 'Post ' . $id . ' is not a Cornerstone component.' );
			}
			$update = array( 'elements' => $flat );
			if ( $title ) {
				$update['title'] = $title;
			}
			if ( is_array( $settings ) ) {
				$update['settings'] = $settings;
			}
			$updated = $doc->update( $update );
			$doc     = is_object( $updated ) ? $updated : $doc;
			$res     = $doc->save();
			if ( ! is_wp_error( $res ) ) {
				delete_post_meta( isset( $res['id'] ) ? (int) $res['id'] : (int) $id, '_cs_component_map' );
				delete_option( 'cs_component_cache' );
			}
			return $res;
		} catch ( Throwable $e ) {
			return new WP_Error( 'cornerstone_save_failed', 'Cornerstone save failed: ' . $e->getMessage() );
		}
	}

	/** Top-level element list of a tree (or empty). */
	public static function roots_of( $tree ) {
		if ( ! is_array( $tree ) ) {
			return array();
		}
		return isset( $tree['_type'] ) ? self::roots( $tree ) : array_values( $tree );
	}

	/* ---------------------------------------------------------------- backups */

	/** Snapshot all Cornerstone meta + post_content before a write. */
	public static function backup( $post_id, $reason ) {
		$post = get_post( $post_id );
		$raw  = array();
		foreach ( get_post_meta( $post_id ) as $key => $values ) {
			if ( self::is_cs_meta_key( $key ) ) {
				$raw[ $key ] = $values[0]; // Stored form, exactly as in the DB.
			}
		}
		$backups = get_post_meta( $post_id, self::BACKUP_KEY, true );
		$backups = is_array( $backups ) ? $backups : array();
		array_unshift(
			$backups,
			array(
				'time'         => gmdate( 'c' ),
				'reason'       => $reason,
				'user'         => get_current_user_id(),
				'post_content' => $post ? $post->post_content : '',
				'meta'         => $raw,
			)
		);
		update_post_meta( $post_id, self::BACKUP_KEY, wp_slash( array_slice( $backups, 0, self::MAX_BACKUPS ) ) );
	}

	public static function list_backups( $post_id ) {
		$backups = get_post_meta( $post_id, self::BACKUP_KEY, true );
		$out     = array();
		foreach ( is_array( $backups ) ? $backups : array() as $i => $b ) {
			$out[] = array(
				'index'     => $i,
				'time'      => $b['time'],
				'reason'    => $b['reason'],
				'meta_keys' => array_keys( $b['meta'] ),
			);
		}
		return $out;
	}

	public static function restore( $post_id, $index ) {
		$backups = get_post_meta( $post_id, self::BACKUP_KEY, true );
		if ( ! is_array( $backups ) || ! isset( $backups[ $index ] ) ) {
			return new WP_Error( 'no_backup', 'No backup at index ' . $index );
		}
		$b = $backups[ $index ];
		self::backup( $post_id, 'before restore of backup from ' . $b['time'] );
		foreach ( get_post_meta( $post_id ) as $key => $values ) {
			if ( self::is_cs_meta_key( $key ) && ! isset( $b['meta'][ $key ] ) ) {
				delete_post_meta( $post_id, $key );
			}
		}
		foreach ( $b['meta'] as $key => $value ) {
			update_post_meta( $post_id, $key, wp_slash( maybe_unserialize( $value ) ) );
		}
		wp_update_post(
			wp_slash(
				array(
					'ID'           => $post_id,
					'post_content' => $b['post_content'],
				)
			)
		);
		return true;
	}

	/* ------------------------------------------------------------ tree utils */

	public static function child_key( array $el ) {
		foreach ( self::CHILD_KEYS as $k ) {
			if ( isset( $el[ $k ] ) && is_array( $el[ $k ] ) ) {
				return $k;
			}
		}
		return null;
	}

	/** The list of top-level elements, whatever the root shape is. */
	public static function &roots( array &$tree ) {
		if ( isset( $tree['_type'] ) ) {
			$k = self::child_key( $tree );
			if ( null === $k ) {
				$tree['_modules'] = array();
				$k                = '_modules';
			}
			return $tree[ $k ];
		}
		return $tree; // Plain list of elements.
	}

	/** Visit every element depth-first. $fn( array $el, int $depth, string $path ). */
	public static function walk( $nodes, callable $fn, $depth = 0, $path = '' ) {
		if ( isset( $nodes['_type'] ) ) {
			$nodes = array( $nodes );
		}
		foreach ( (array) $nodes as $i => $el ) {
			if ( ! is_array( $el ) ) {
				continue;
			}
			$p = '' === $path ? (string) $i : $path . '.' . $i;
			$fn( $el, $depth, $p );
			$k = self::child_key( $el );
			if ( $k ) {
				self::walk( $el[ $k ], $fn, $depth + 1, $p );
			}
		}
	}

	/** Compact human-readable outline of a tree. */
	public static function outline( $tree ) {
		$lines = array();
		self::walk(
			$tree,
			function ( $el, $depth, $path ) use ( &$lines ) {
				$type    = isset( $el['_type'] ) ? $el['_type'] : '?';
				$label   = isset( $el['_label'] ) ? ' "' . $el['_label'] . '"' : '';
				$id      = isset( $el['_id'] ) ? ' #' . $el['_id'] : '';
				$preview = self::text_preview( $el );
				$lines[] = str_repeat( '  ', $depth ) . "[$path] $type$id$label" . ( $preview ? " — $preview" : '' );
			}
		);
		return implode( "\n", $lines );
	}

	private static function text_preview( array $el ) {
		foreach ( $el as $k => $v ) {
			if ( is_string( $v ) && '' !== trim( $v ) && preg_match( '/(content|text|title)$/', $k ) ) {
				$t = trim( preg_replace( '/\s+/', ' ', wp_strip_all_tags( $v ) ) );
				if ( '' !== $t ) {
					return mb_strimwidth( $t, 0, 60, '…' );
				}
			}
		}
		return '';
	}

	/** Deep copy with long strings shortened and children replaced by a count. */
	public static function summarize_element( array $el, $max_len = 300 ) {
		$k = self::child_key( $el );
		if ( $k ) {
			$el[ $k ] = '(' . count( $el[ $k ] ) . ' children)';
		}
		array_walk_recursive(
			$el,
			function ( &$v ) use ( $max_len ) {
				if ( is_string( $v ) && strlen( $v ) > $max_len ) {
					$v = substr( $v, 0, $max_len ) . '…';
				}
			}
		);
		return $el;
	}

	/** Largest numeric `_id` in a tree (0 if none / non-numeric). */
	public static function max_numeric_id( $tree ) {
		$max = 0;
		self::walk(
			$tree,
			function ( $el ) use ( &$max ) {
				if ( isset( $el['_id'] ) && is_numeric( $el['_id'] ) ) {
					$max = max( $max, (int) $el['_id'] );
				}
			}
		);
		return $max;
	}

	/**
	 * Give every element in $nodes a fresh `_id` so cloned elements don't
	 * collide with existing ones. Numeric ids continue from $next; string ids
	 * get a unique suffix.
	 */
	public static function reassign_ids( array $nodes, &$next ) {
		foreach ( $nodes as &$el ) {
			if ( ! is_array( $el ) ) {
				continue;
			}
			if ( isset( $el['_id'] ) ) {
				$el['_id'] = is_numeric( $el['_id'] ) ? (string) ( $next++ ) : preg_replace( '/-px\w+$/', '', $el['_id'] ) . '-px' . wp_generate_password( 5, false );
			}
			$k = self::child_key( $el );
			if ( $k ) {
				$el[ $k ] = self::reassign_ids( $el[ $k ], $next );
			}
		}
		return $nodes;
	}
}
