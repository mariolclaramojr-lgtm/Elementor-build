<?php
/**
 * MCP tool definitions and handlers.
 *
 * Every tool is declared once in self::registry(): name, description, input
 * schema, whether it writes, and its handler. The admin screen reads the same
 * registry for the per-tool on/off switches.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

class Pro_Extended_Tools {

	const OPTION_SETTINGS = 'pro_extended_settings';
	const OPTION_LOG      = 'pro_extended_log';
	const LOG_MAX         = 200;

	/** Option name prefixes the option tools may touch. */
	const OPTION_PREFIXES = array( 'cs_', 'cornerstone', 'x_', 'pro_', 'tco_', 'themeco' );

	private static $registry = null;

	public static function instructions() {
		return implode(
			"\n",
			array(
				'Tools for Themeco Pro / Cornerstone pages. Cornerstone stores each page as a JSON element tree (post meta _cornerstone_data); elements have a `_type` and children in `_modules`.',
				'The element schema differs between Cornerstone versions, so LEARN IT FROM THE SITE before writing: call cs_environment, then cs_element_catalog to see every element type in use with a real example, then cs_get_element_tree on a hand-built reference page.',
				'To build pages, copy the shape of real examples (same keys, same value formats) rather than inventing keys.',
				'HTML designs: cs_import_html wraps HTML+CSS in the site\'s own Raw Content/Code element (pixel-accurate, not visually editable). For editable pages, convert to native elements modelled on catalog examples and save with cs_save_element_tree.',
				'Every write backs up the page first (cs_list_backups / cs_restore_backup). New pages default to draft. After writes, call cs_purge_cache and check the page in the browser and in the Cornerstone editor.',
			)
		);
	}

	/* ============================================================ registry */

	private static function registry() {
		if ( null !== self::$registry ) {
			return self::$registry;
		}
		$id     = array(
			'type'        => 'integer',
			'description' => 'Post/page ID.',
		);
		$object = array( 'type' => 'object' );

		self::$registry = array(
			'cs_environment'       => array(
				'description' => 'Report WordPress, theme and Cornerstone/Pro versions, related constants, Cornerstone hooks and functions. Call first on a new site.',
				'write'       => false,
				'props'       => (object) array(),
				'required'    => array(),
				'handler'     => 'environment',
			),
			'cs_list_pages'        => array(
				'description' => 'List posts of a type (default page) with a flag for whether each was built with Cornerstone.',
				'write'       => false,
				'props'       => array(
					'post_type'         => array(
						'type'    => 'string',
						'default' => 'page',
					),
					'search'            => array( 'type' => 'string' ),
					'status'            => array(
						'type'        => 'string',
						'description' => 'publish, draft, any …',
						'default'     => 'any',
					),
					'cornerstone_only'  => array(
						'type'    => 'boolean',
						'default' => false,
					),
					'per_page'          => array(
						'type'    => 'integer',
						'default' => 50,
					),
					'page'              => array(
						'type'    => 'integer',
						'default' => 1,
					),
				),
				'required'    => array(),
				'handler'     => 'list_pages',
			),
			'cs_get_page'          => array(
				'description' => 'Get a post with ALL its Cornerstone-related meta (decoded) and optionally post_content. Use on a hand-built page to learn how this site stores data.',
				'write'       => false,
				'props'       => array(
					'id'              => $id,
					'include_content' => array(
						'type'    => 'boolean',
						'default' => true,
					),
					'include_tree'    => array(
						'type'        => 'boolean',
						'description' => 'Include the full _cornerstone_data tree (can be large).',
						'default'     => false,
					),
				),
				'required'    => array( 'id' ),
				'handler'     => 'get_page',
			),
			'cs_get_element_tree'  => array(
				'description' => 'Get a page\'s element tree. format=outline gives an indented list with [paths] usable by cs_update_element; format=full gives the raw JSON.',
				'write'       => false,
				'props'       => array(
					'id'     => $id,
					'format' => array(
						'type'    => 'string',
						'enum'    => array( 'outline', 'full', 'both' ),
						'default' => 'both',
					),
					'path'   => array(
						'type'        => 'string',
						'description' => 'Optional element path (e.g. "0.1") to return only that subtree.',
					),
				),
				'required'    => array( 'id' ),
				'handler'     => 'get_element_tree',
			),
			'cs_element_catalog'   => array(
				'description' => 'Scan every Cornerstone document on the site (pages, headers, footers, layouts, global blocks) and report each element `_type` in use: count, all keys seen, and one real example. The schema reference for building elements.',
				'write'       => false,
				'props'       => array(
					'type'  => array(
						'type'        => 'string',
						'description' => 'Only this element type (returns up to 3 examples).',
					),
					'limit' => array(
						'type'        => 'integer',
						'description' => 'Max documents to scan.',
						'default'     => 300,
					),
				),
				'required'    => array(),
				'handler'     => 'element_catalog',
			),
			'cs_create_page'       => array(
				'description' => 'Create a page (draft by default). clone_from copies a Cornerstone page\'s whole builder state; otherwise the page starts empty but flagged as a Cornerstone page using flags copied from an existing one.',
				'write'       => true,
				'props'       => array(
					'title'      => array( 'type' => 'string' ),
					'status'     => array(
						'type'    => 'string',
						'enum'    => array( 'draft', 'publish', 'private', 'pending' ),
						'default' => 'draft',
					),
					'slug'       => array( 'type' => 'string' ),
					'parent'     => array( 'type' => 'integer' ),
					'post_type'  => array(
						'type'    => 'string',
						'default' => 'page',
					),
					'template'   => array(
						'type'        => 'string',
						'description' => 'Page template file, if any.',
					),
					'clone_from' => array(
						'type'        => 'integer',
						'description' => 'ID of a Cornerstone page to duplicate.',
					),
					'elements'   => array(
						'type'        => 'array',
						'description' => 'Optional initial top-level elements.',
						'items'       => $object,
					),
				),
				'required'    => array( 'title' ),
				'handler'     => 'create_page',
			),
			'cs_save_element_tree' => array(
				'description' => 'Replace a page\'s whole element tree. Pass `tree` as either the root object or a list of top-level elements, in the same shape cs_get_element_tree returns. Backs up first.',
				'write'       => true,
				'props'       => array(
					'id'           => $id,
					'tree'         => array(
						'description' => 'Root object or array of top-level elements.',
					),
					'post_content' => array(
						'type'        => 'string',
						'description' => 'Optional: also set post_content (some Cornerstone versions keep a rendered copy there).',
					),
				),
				'required'    => array( 'id', 'tree' ),
				'handler'     => 'save_element_tree',
			),
			'cs_update_element'    => array(
				'description' => 'Edit one element by path (from the outline): merge `set` properties, remove `unset` keys, delete it (`remove`), or insert `insert` elements before/after/inside it.',
				'write'       => true,
				'props'       => array(
					'id'       => $id,
					'path'     => array(
						'type'        => 'string',
						'description' => 'e.g. "0.1.2"',
					),
					'set'      => $object,
					'unset'    => array(
						'type'  => 'array',
						'items' => array( 'type' => 'string' ),
					),
					'remove'   => array( 'type' => 'boolean' ),
					'insert'   => array(
						'type'  => 'array',
						'items' => $object,
					),
					'position' => array(
						'type'    => 'string',
						'enum'    => array( 'before', 'after', 'inside' ),
						'default' => 'after',
					),
				),
				'required'    => array( 'id', 'path' ),
				'handler'     => 'update_element',
			),
			'cs_import_html'       => array(
				'description' => 'Import an HTML design into a page as the site\'s own Raw Content/Code element(s), wrapped in section/row/column cloned from real examples. Pixel-accurate; not visually editable. Use `sections: true` to split each top-level <section>/<header>/<footer> into its own Cornerstone section.',
				'write'       => true,
				'props'       => array(
					'id'            => array(
						'type'        => 'integer',
						'description' => 'Target page. Omit to create a new draft with `title`.',
					),
					'title'         => array( 'type' => 'string' ),
					'html'          => array(
						'type'        => 'string',
						'description' => 'Body HTML (a full document is fine; <body> is extracted).',
					),
					'css'           => array(
						'type'        => 'string',
						'description' => 'CSS for the design.',
					),
					'css_target'    => array(
						'type'        => 'string',
						'enum'        => array( 'inline', 'page_settings' ),
						'default'     => 'inline',
						'description' => 'inline = <style> inside the first raw element (always works). page_settings = the page\'s Cornerstone custom CSS setting (key auto-detected).',
					),
					'sections'      => array(
						'type'    => 'boolean',
						'default' => true,
					),
					'mode'          => array(
						'type'    => 'string',
						'enum'    => array( 'replace', 'append' ),
						'default' => 'replace',
					),
					'raw_type'      => array(
						'type'        => 'string',
						'description' => 'Override the element _type used for raw HTML (auto-detected from the catalog).',
					),
					'wrapper_types' => array(
						'type'        => 'array',
						'items'       => array( 'type' => 'string' ),
						'description' => 'Override wrapper chain, outermost first, e.g. ["section","layout-row","layout-column"].',
					),
				),
				'required'    => array( 'html' ),
				'handler'     => 'import_html',
			),
			'cs_update_settings'   => array(
				'description' => 'Merge keys into a page\'s _cornerstone_settings (e.g. custom CSS/JS — inspect a page with cs_get_page first to see key names). null deletes a key.',
				'write'       => true,
				'props'       => array(
					'id'       => $id,
					'settings' => $object,
				),
				'required'    => array( 'id', 'settings' ),
				'handler'     => 'update_settings',
			),
			'cs_list_options'      => array(
				'description' => 'List site options belonging to Cornerstone/Pro/X (names + sizes). Global CSS, fonts and colors live here.',
				'write'       => false,
				'props'       => (object) array(),
				'required'    => array(),
				'handler'     => 'list_options',
			),
			'cs_get_option'        => array(
				'description' => 'Read one Cornerstone/Pro option (decoded).',
				'write'       => false,
				'props'       => array( 'name' => array( 'type' => 'string' ) ),
				'required'    => array( 'name' ),
				'handler'     => 'get_option',
			),
			'cs_update_option'     => array(
				'description' => 'Write one Cornerstone/Pro option (e.g. global CSS). Admins only. The previous value is returned so it can be restored.',
				'write'       => true,
				'props'       => array(
					'name'    => array( 'type' => 'string' ),
					'value'   => array( 'description' => 'New value. Arrays/objects are stored in the same form (JSON string vs array) as the current value.' ),
				),
				'required'    => array( 'name', 'value' ),
				'handler'     => 'update_option',
			),
			'cs_upload_media'      => array(
				'description' => 'Add an image/file to the Media Library from a public URL or base64 data. Returns attachment id and URL.',
				'write'       => true,
				'props'       => array(
					'url'      => array( 'type' => 'string' ),
					'base64'   => array( 'type' => 'string' ),
					'filename' => array(
						'type'        => 'string',
						'description' => 'Required with base64.',
					),
					'title'    => array( 'type' => 'string' ),
					'alt'      => array( 'type' => 'string' ),
				),
				'required'    => array(),
				'handler'     => 'upload_media',
			),
			'cs_list_media'        => array(
				'description' => 'List Media Library items (id, url, filename, alt).',
				'write'       => false,
				'props'       => array(
					'search'   => array( 'type' => 'string' ),
					'per_page' => array(
						'type'    => 'integer',
						'default' => 50,
					),
					'page'     => array(
						'type'    => 'integer',
						'default' => 1,
					),
				),
				'required'    => array(),
				'handler'     => 'list_media',
			),
			'cs_list_backups'      => array(
				'description' => 'List automatic backups taken before each write to a page.',
				'write'       => false,
				'props'       => array( 'id' => $id ),
				'required'    => array( 'id' ),
				'handler'     => 'list_backups',
			),
			'cs_restore_backup'    => array(
				'description' => 'Restore a page\'s Cornerstone data and post_content from a backup (index from cs_list_backups; 0 = most recent). The current state is backed up first.',
				'write'       => true,
				'props'       => array(
					'id'    => $id,
					'index' => array(
						'type'    => 'integer',
						'default' => 0,
					),
				),
				'required'    => array( 'id' ),
				'handler'     => 'restore_backup',
			),
			'cs_dev_source'        => array(
				'description' => 'Developer: read-only access to the active parent theme\'s source (Pro/X includes Cornerstone). List a directory, read a file (optionally a line range), or grep a directory recursively with a regex. Admins only. Use it to learn how Cornerstone saves documents.',
				'write'       => false,
				'props'       => array(
					'root'  => array(
						'type'        => 'string',
						'enum'        => array( 'theme', 'plugins' ),
						'default'     => 'theme',
						'description' => 'theme = active parent theme (Pro/X, includes Cornerstone); plugins = wp-content/plugins.',
					),
					'path'  => array(
						'type'        => 'string',
						'description' => 'Path relative to the root, e.g. "cornerstone/includes/classes" or "modern-events-calendar/app". Empty = root.',
					),
					'grep'  => array(
						'type'        => 'string',
						'description' => 'PCRE pattern without delimiters; searches *.php under path.',
					),
					'start' => array( 'type' => 'integer' ),
					'end'   => array( 'type' => 'integer' ),
				),
				'required'    => array(),
				'handler'     => 'dev_source',
			),
			'cs_get_layout'        => array(
				'description' => 'Get a Pro header/footer/layout document (post types cs_header, cs_footer, cs_layout*): settings (incl. assignments) and regions element tree with an outline. List them with cs_list_pages post_type=cs_header|cs_footer, status=tco-data.',
				'write'       => false,
				'props'       => array( 'id' => $id ),
				'required'    => array( 'id' ),
				'handler'     => 'get_layout',
			),
			'cs_save_layout'       => array(
				'description' => 'Create or update a Pro header or footer through Cornerstone. Regions: header uses "top" (also right/bottom/left with multi_region), footer uses "footer". Each region is a list of `bar` elements -> `container` elements -> any elements; every element needs `_region` set to its region (added automatically). settings: customCSS, customJS, assignments ([{group:true, condition:"site:entire-site"|"single:specific-post-of-type|page", value:<post id or "">}]), assignment_priority (lowest wins). Omit id to create. Backs up existing documents first.',
				'write'       => true,
				'props'       => array(
					'id'       => array(
						'type'        => 'integer',
						'description' => 'Existing header/footer ID. Omit to create.',
					),
					'type'     => array(
						'type' => 'string',
						'enum' => array( 'header', 'footer' ),
					),
					'title'    => array( 'type' => 'string' ),
					'regions'  => array(
						'type'        => 'object',
						'description' => 'region name => list of bar elements.',
					),
					'settings' => $object,
				),
				'required'    => array(),
				'handler'     => 'save_layout',
			),
			'cs_save_component'    => array(
				'description' => 'Create or update a reusable Cornerstone Component (shown in Cornerstone under Components) through Cornerstone\'s Component document. `elements` is the usual nested tree (list of top-level elements, children in _modules). Place it on pages with an element {"_type":"global-block","global_block_id":"<id>"}; editing the component then updates every page using it. Omit id to create. Backs up existing components first.',
				'write'       => true,
				'props'       => array(
					'id'       => array(
						'type'        => 'integer',
						'description' => 'Existing component ID. Omit to create.',
					),
					'title'    => array( 'type' => 'string' ),
					'elements' => array(
						'type'  => 'array',
						'items' => $object,
					),
					'settings' => $object,
				),
				'required'    => array( 'elements' ),
				'handler'     => 'save_component',
			),
			'gf_list_forms'        => array(
				'description' => 'Gravity Forms: list forms (id, title, active, entry count). Use the id in [gravityform id="…"].',
				'write'       => false,
				'props'       => (object) array(),
				'required'    => array(),
				'handler'     => 'gf_list_forms',
			),
			'gf_save_form'         => array(
				'description' => 'Gravity Forms: create (omit id) or update a form through GFAPI. `form` is a Gravity Forms form object: title, description, labelPlacement, button {type:"text", text}, fields [{type:"name"|"email"|"textarea"|"text"|"phone"|..., id, label, isRequired, ...}], confirmations, notifications. Updating replaces the whole form object. Admins only.',
				'write'       => true,
				'props'       => array(
					'id'   => array( 'type' => 'integer' ),
					'form' => $object,
				),
				'required'    => array( 'form' ),
				'handler'     => 'gf_save_form',
			),
			'cs_list_menus'        => array(
				'description' => 'List WordPress navigation menus (id, name, item count). Cornerstone nav elements reference them as "menu:<id>".',
				'write'       => false,
				'props'       => (object) array(),
				'required'    => array(),
				'handler'     => 'list_menus',
			),
			'cs_save_menu'         => array(
				'description' => 'Create a WordPress menu, or replace all items of an existing one (by name). items: [{title, url, children?: [...] }]. Returns the menu id for nav elements ("menu:<id>").',
				'write'       => true,
				'props'       => array(
					'name'  => array( 'type' => 'string' ),
					'items' => array(
						'type'  => 'array',
						'items' => $object,
					),
				),
				'required'    => array( 'name', 'items' ),
				'handler'     => 'save_menu',
			),
			'cs_get_post_meta'     => array(
				'description' => 'Developer: read all post meta of any post (decoded). Optional key prefix filter. Admins only. Useful to learn how a plugin (e.g. Modern Events Calendar) stores its data.',
				'write'       => false,
				'props'       => array(
					'id'     => $id,
					'prefix' => array( 'type' => 'string' ),
				),
				'required'    => array( 'id' ),
				'handler'     => 'get_post_meta_all',
			),
			'cs_save_post'         => array(
				'description' => 'Admin: create or update a post of ANY post type (e.g. mec_calendars = MEC shortcodes, wpfc_sermon = sermons) with title, status, content, excerpt, parent and post meta (arrays stored natively). Pass id to update; meta keys set to null are deleted. Backs up existing posts first.',
				'write'       => true,
				'props'       => array(
					'id'        => array( 'type' => 'integer' ),
					'post_type' => array( 'type' => 'string' ),
					'title'     => array( 'type' => 'string' ),
					'status'    => array(
						'type'    => 'string',
						'default' => 'publish',
					),
					'content'   => array( 'type' => 'string' ),
					'excerpt'   => array( 'type' => 'string' ),
					'slug'      => array( 'type' => 'string' ),
					'date'      => array(
						'type'        => 'string',
						'description' => 'Post date Y-m-d H:i:s (optional).',
					),
					'meta'      => $object,
					'terms'     => array(
						'type'        => 'object',
						'description' => 'taxonomy => list of term names (created if missing).',
					),
					'featured_image' => array( 'type' => 'integer' ),
				),
				'required'    => array(),
				'handler'     => 'save_post_generic',
			),
			'mec_save_event'       => array(
				'description' => 'Create or update a Modern Events Calendar event through MEC\'s own save routine (MEC_main::save_event), so its date/occurrence tables are filled correctly. `event` is passed straight through (keys per MEC source: title, content, status, start, start_time_hour, start_time_minutes, start_time_ampm, end, end_time_hour, end_time_minutes, end_time_ampm, allday, repeat_status, repeat_type, interval, finish, location_id, organizer_id, meta, …). Pass post_id to update. Returns the post id, its dates and meta. Optional featured_image (attachment id) and categories (term names in mec_category).',
				'write'       => true,
				'props'       => array(
					'event'          => $object,
					'post_id'        => array( 'type' => 'integer' ),
					'featured_image' => array( 'type' => 'integer' ),
					'categories'     => array(
						'type'  => 'array',
						'items' => array( 'type' => 'string' ),
					),
				),
				'required'    => array( 'event' ),
				'handler'     => 'mec_save_event',
			),
			'cs_preview_link'      => array(
				'description' => 'Create an expiring public link to view a draft/private page without logging in (for screenshots or client review). Generating a new link invalidates the previous one.',
				'write'       => true,
				'props'       => array(
					'id'    => $id,
					'hours' => array(
						'type'    => 'integer',
						'default' => 48,
					),
				),
				'required'    => array( 'id' ),
				'handler'     => 'preview_link',
			),
			'cs_purge_cache'       => array(
				'description' => 'Best-effort cache clear after writes: Cornerstone generated styles for the page, WordPress object cache, and host page caches (WP Engine) when present.',
				'write'       => true,
				'props'       => array(
					'id'  => $id,
					'all' => array(
						'type'        => 'boolean',
						'description' => 'Also clear compiled Cornerstone CSS for every page (after global CSS/colors/fonts changes).',
					),
				),
				'required'    => array(),
				'handler'     => 'purge_cache',
			),
		);
		return self::$registry;
	}

	/* ====================================================== public surface */

	public static function settings() {
		$s = get_option( self::OPTION_SETTINGS, array() );
		return wp_parse_args(
			is_array( $s ) ? $s : array(),
			array(
				'read_only'      => false,
				'disabled_tools' => array(),
			)
		);
	}

	/** name => [description, write] for the admin screen. */
	public static function catalog_for_admin() {
		$out = array();
		foreach ( self::registry() as $name => $t ) {
			$out[ $name ] = array(
				'description' => $t['description'],
				'write'       => $t['write'],
			);
		}
		return $out;
	}

	private static function enabled( $name, $t ) {
		$s = self::settings();
		if ( $t['write'] && $s['read_only'] ) {
			return false;
		}
		return ! in_array( $name, (array) $s['disabled_tools'], true );
	}

	public static function exists( $name ) {
		$r = self::registry();
		return isset( $r[ $name ] ) && self::enabled( $name, $r[ $name ] );
	}

	public static function definitions() {
		$defs = array();
		foreach ( self::registry() as $name => $t ) {
			if ( ! self::enabled( $name, $t ) ) {
				continue;
			}
			$schema = array(
				'type'       => 'object',
				'properties' => $t['props'],
			);
			if ( $t['required'] ) {
				$schema['required'] = $t['required'];
			}
			$defs[] = array(
				'name'        => $name,
				'description' => $t['description'],
				'inputSchema' => $schema,
				'annotations' => array(
					'readOnlyHint'    => ! $t['write'],
					'destructiveHint' => $t['write'],
				),
			);
		}
		return $defs;
	}

	public static function call( $name, array $args ) {
		$t = self::registry()[ $name ];
		if ( isset( $args['id'] ) ) {
			$args['id'] = (int) $args['id'];
			if ( $args['id'] && ! get_post( $args['id'] ) ) {
				return new WP_Error( 'not_found', 'No post with id ' . $args['id'] );
			}
			$cap = $t['write'] ? 'edit_post' : 'read_post';
			if ( $args['id'] && ! current_user_can( $cap, $args['id'] ) ) {
				return new WP_Error( 'forbidden', 'You cannot access post ' . $args['id'] );
			}
		}
		$result = call_user_func( array( __CLASS__, $t['handler'] ), $args );
		if ( $t['write'] && ! is_wp_error( $result ) ) {
			self::log( $name, $args, $result );
		}
		return $result;
	}

	/* ================================================================= log */

	private static function log( $tool, $args, $result ) {
		$post_id = 0;
		if ( ! empty( $args['id'] ) ) {
			$post_id = (int) $args['id'];
		} elseif ( is_array( $result ) && ! empty( $result['id'] ) ) {
			$post_id = (int) $result['id'];
		}
		$log = get_option( self::OPTION_LOG, array() );
		$log = is_array( $log ) ? $log : array();
		array_unshift(
			$log,
			array(
				'time'    => gmdate( 'c' ),
				'user'    => get_current_user_id(),
				'tool'    => $tool,
				'post_id' => $post_id,
				'summary' => is_array( $result ) && isset( $result['summary'] ) ? $result['summary'] : '',
			)
		);
		update_option( self::OPTION_LOG, array_slice( $log, 0, self::LOG_MAX ), false );
	}

	public static function get_log() {
		$log = get_option( self::OPTION_LOG, array() );
		return is_array( $log ) ? $log : array();
	}

	/* ============================================================ handlers */

	private static function environment( $args ) {
		global $wp_filter;
		$theme  = wp_get_theme();
		$parent = $theme->parent();

		$constants = array();
		$user_constants = get_defined_constants( true );
		foreach ( isset( $user_constants['user'] ) ? $user_constants['user'] : array() as $k => $v ) {
			if ( preg_match( '/^(CS_|X_|PRO_|CORNERSTONE|TCO_|THEMECO)/', $k ) && is_scalar( $v ) ) {
				$constants[ $k ] = $v;
			}
		}

		$functions = array_values(
			array_filter(
				get_defined_functions()['user'],
				function ( $f ) {
					return (bool) preg_match( '/^(cornerstone|cs_|x_|tco_)/', $f );
				}
			)
		);
		sort( $functions );

		$classes = array_values(
			array_filter(
				get_declared_classes(),
				function ( $c ) {
					return (bool) preg_match( '/cornerstone|themeco|^tco_|^cs_/i', $c );
				}
			)
		);

		$hooks = array();
		foreach ( array_keys( (array) $wp_filter ) as $h ) {
			if ( preg_match( '/^(cs_|cornerstone|x_|tco_)/', $h ) ) {
				$hooks[] = $h;
			}
		}
		sort( $hooks );

		if ( ! function_exists( 'get_plugins' ) ) {
			require_once ABSPATH . 'wp-admin/includes/plugin.php';
		}
		$plugins = array();
		foreach ( get_plugins() as $file => $p ) {
			if ( preg_match( '/cornerstone|themeco|pro|x-/i', $file . ' ' . $p['Name'] . ' ' . $p['Author'] ) ) {
				$plugins[ $file ] = array(
					'name'    => $p['Name'],
					'version' => $p['Version'],
					'active'  => is_plugin_active( $file ),
				);
			}
		}

		$cs_post_types = array_values(
			array_filter(
				get_post_types(),
				function ( $pt ) {
					return (bool) preg_match( '/^(cs_|x-|tco|pro)/', $pt );
				}
			)
		);

		return array(
			'site'                  => home_url(),
			'wordpress'             => get_bloginfo( 'version' ),
			'php'                   => PHP_VERSION,
			'theme'                 => $theme->get( 'Name' ) . ' ' . $theme->get( 'Version' ),
			'parent_theme'          => $parent ? $parent->get( 'Name' ) . ' ' . $parent->get( 'Version' ) : null,
			'cornerstone_detected'  => (bool) ( $constants || $classes || function_exists( 'cornerstone' ) ),
			'plugins'               => $plugins,
			'constants'             => $constants,
			'cornerstone_post_types' => $cs_post_types,
			'functions'             => array_slice( $functions, 0, 400 ),
			'classes'               => array_slice( $classes, 0, 200 ),
			'hooks'                 => array_slice( $hooks, 0, 400 ),
			'pro_extended'          => PRO_EXTENDED_VERSION,
		);
	}

	private static function list_pages( $args ) {
		$q = array(
			'post_type'      => isset( $args['post_type'] ) ? sanitize_key( $args['post_type'] ) : 'page',
			'post_status'    => isset( $args['status'] ) ? $args['status'] : 'any',
			's'              => isset( $args['search'] ) ? $args['search'] : '',
			'posts_per_page' => min( 200, max( 1, isset( $args['per_page'] ) ? (int) $args['per_page'] : 50 ) ),
			'paged'          => max( 1, isset( $args['page'] ) ? (int) $args['page'] : 1 ),
			'orderby'        => 'modified',
			'order'          => 'DESC',
		);
		if ( ! empty( $args['cornerstone_only'] ) ) {
			$q['meta_key'] = Pro_Extended_CS_Store::DATA_KEY; // phpcs:ignore WordPress.DB.SlowDBQuery
		}
		$query = new WP_Query( $q );
		$items = array();
		foreach ( $query->posts as $p ) {
			$items[] = array(
				'id'          => $p->ID,
				'title'       => $p->post_title,
				'status'      => $p->post_status,
				'slug'        => $p->post_name,
				'parent'      => $p->post_parent,
				'link'        => get_permalink( $p ),
				'modified'    => $p->post_modified_gmt,
				'cornerstone' => '' !== get_post_meta( $p->ID, Pro_Extended_CS_Store::DATA_KEY, true ),
			);
		}
		return array(
			'total' => (int) $query->found_posts,
			'pages' => (int) $query->max_num_pages,
			'items' => $items,
		);
	}

	private static function get_page( $args ) {
		$p    = get_post( $args['id'] );
		$meta = Pro_Extended_CS_Store::get_cs_meta( $p->ID );
		if ( empty( $args['include_tree'] ) && isset( $meta[ Pro_Extended_CS_Store::DATA_KEY ] ) ) {
			$meta[ Pro_Extended_CS_Store::DATA_KEY ] = '(omitted — use include_tree or cs_get_element_tree)';
		}
		$out = array(
			'id'        => $p->ID,
			'title'     => $p->post_title,
			'status'    => $p->post_status,
			'post_type' => $p->post_type,
			'slug'      => $p->post_name,
			'link'      => get_permalink( $p ),
			'template'  => get_page_template_slug( $p ),
			'meta'      => $meta,
		);
		if ( ! isset( $args['include_content'] ) || $args['include_content'] ) {
			$out['post_content'] = $p->post_content;
		}
		return $out;
	}

	private static function get_element_tree( $args ) {
		$tree = Pro_Extended_CS_Store::get_tree( $args['id'] );
		if ( null === $tree ) {
			return new WP_Error( 'no_tree', 'This post has no Cornerstone data.' );
		}
		if ( ! empty( $args['path'] ) ) {
			$node = self::node_at( $tree, $args['path'] );
			if ( is_wp_error( $node ) ) {
				return $node;
			}
			$tree = $node;
		}
		$format = isset( $args['format'] ) ? $args['format'] : 'both';
		$out    = array( 'id' => $args['id'] );
		if ( 'full' !== $format ) {
			$out['outline'] = Pro_Extended_CS_Store::outline( $tree );
		}
		if ( 'outline' !== $format ) {
			$out['tree'] = $tree;
		}
		return $out;
	}

	/** Shared by the catalog tool and the HTML importer. */
	private static function scan_catalog( $limit = 300, $only_type = null ) {
		$posts = get_posts(
			array(
				'post_type'      => array_values( array_diff( get_post_types(), array( 'revision', 'attachment', 'nav_menu_item' ) ) ),
				'post_status'    => 'any',
				'meta_key'       => Pro_Extended_CS_Store::DATA_KEY, // phpcs:ignore WordPress.DB.SlowDBQuery
				'posts_per_page' => max( 1, (int) $limit ),
				'orderby'        => 'modified',
				'order'          => 'DESC',
				'fields'         => 'ids',
			)
		);
		$types = array();
		foreach ( $posts as $pid ) {
			$tree = Pro_Extended_CS_Store::get_tree( $pid );
			if ( null === $tree ) {
				continue;
			}
			Pro_Extended_CS_Store::walk(
				$tree,
				function ( $el, $depth ) use ( &$types, $pid, $only_type ) {
					if ( ! isset( $el['_type'] ) || ( $only_type && $el['_type'] !== $only_type ) ) {
						return;
					}
					$t = $el['_type'];
					if ( ! isset( $types[ $t ] ) ) {
						$types[ $t ] = array(
							'count'     => 0,
							'depths'    => array(),
							'keys'      => array(),
							'posts'     => array(),
							'examples'  => array(),
						);
					}
					$types[ $t ]['count']++;
					$types[ $t ]['depths'][ $depth ] = true;
					$types[ $t ]['posts'][ $pid ]    = true;
					foreach ( array_keys( $el ) as $k ) {
						$types[ $t ]['keys'][ $k ] = true;
					}
					if ( count( $types[ $t ]['examples'] ) < ( $only_type ? 3 : 1 ) ) {
						$types[ $t ]['examples'][] = array(
							'post_id' => $pid,
							'element' => $el,
						);
					}
				}
			);
		}
		return array(
			'documents' => count( $posts ),
			'types'     => $types,
		);
	}

	private static function element_catalog( $args ) {
		$only = ! empty( $args['type'] ) ? $args['type'] : null;
		$scan = self::scan_catalog( isset( $args['limit'] ) ? $args['limit'] : 300, $only );
		$out  = array();
		foreach ( $scan['types'] as $t => $info ) {
			$out[ $t ] = array(
				'count'    => $info['count'],
				'depths'   => array_keys( $info['depths'] ),
				'in_posts' => array_slice( array_keys( $info['posts'] ), 0, 10 ),
				'keys'     => array_keys( $info['keys'] ),
				'examples' => array_map(
					function ( $ex ) {
						return array(
							'post_id' => $ex['post_id'],
							'element' => Pro_Extended_CS_Store::summarize_element( $ex['element'] ),
						);
					},
					$info['examples']
				),
			);
		}
		ksort( $out );
		return array(
			'documents_scanned' => $scan['documents'],
			'element_types'     => $out,
			'note'              => $scan['documents'] ? null : 'No Cornerstone documents found. Build a reference page by hand in Cornerstone first.',
		);
	}

	private static function create_page( $args ) {
		$post_type = isset( $args['post_type'] ) ? sanitize_key( $args['post_type'] ) : 'page';
		$pto       = get_post_type_object( $post_type );
		if ( ! $pto || ! current_user_can( $pto->cap->create_posts ) ) {
			return new WP_Error( 'forbidden', 'Cannot create ' . $post_type );
		}
		$status = isset( $args['status'] ) ? $args['status'] : 'draft';
		if ( 'publish' === $status && ! current_user_can( $pto->cap->publish_posts ) ) {
			$status = 'pending';
		}

		$source = ! empty( $args['clone_from'] ) ? get_post( (int) $args['clone_from'] ) : null;
		if ( ! empty( $args['clone_from'] ) && ( ! $source || ! current_user_can( 'read_post', $source->ID ) ) ) {
			return new WP_Error( 'not_found', 'Cannot read clone_from post' );
		}

		$postarr = array(
			'post_title'   => $args['title'],
			'post_status'  => $status,
			'post_type'    => $post_type,
			'post_content' => $source ? $source->post_content : '',
		);
		if ( ! empty( $args['slug'] ) ) {
			$postarr['post_name'] = sanitize_title( $args['slug'] );
		}
		if ( ! empty( $args['parent'] ) ) {
			$postarr['post_parent'] = (int) $args['parent'];
		}
		$new_id = wp_insert_post( wp_slash( $postarr ), true );
		if ( is_wp_error( $new_id ) ) {
			return $new_id;
		}

		$template_src = $source ? $source->ID : ( class_exists( 'Themeco\\Cornerstone\\Documents\\Content' ) ? 0 : self::latest_cornerstone_post( $post_type ) );
		$copied       = array();
		if ( $template_src ) {
			foreach ( get_post_meta( $template_src ) as $key => $values ) {
				if ( ! Pro_Extended_CS_Store::is_cs_meta_key( $key ) ) {
					continue;
				}
				// Without clone_from, copy only small flag/version keys, not content or generated styles.
				if ( ! $source && ( Pro_Extended_CS_Store::DATA_KEY === $key || Pro_Extended_CS_Store::SETTINGS_KEY === $key || preg_match( '/style|css|cache|generated|data/i', $key ) || strlen( $values[0] ) > 200 ) ) {
					continue;
				}
				update_post_meta( $new_id, $key, wp_slash( maybe_unserialize( $values[0] ) ) );
				$copied[] = $key;
			}
		}
		if ( $source ) {
			$tpl = get_page_template_slug( $source );
			if ( $tpl ) {
				update_post_meta( $new_id, '_wp_page_template', $tpl );
			}
		}
		if ( ! empty( $args['template'] ) ) {
			update_post_meta( $new_id, '_wp_page_template', sanitize_text_field( $args['template'] ) );
		}

		$saved_via = null;
		if ( ! empty( $args['elements'] ) ) {
			$saved_via = Pro_Extended_CS_Store::save_tree( $new_id, array_values( $args['elements'] ) );
		} elseif ( ! $source ) {
			// An empty Cornerstone save marks the page as Cornerstone content (settings + data meta).
			$saved_via = Pro_Extended_CS_Store::save_tree( $new_id, self::empty_tree_like( $template_src ) );
		}
		if ( is_wp_error( $saved_via ) ) {
			return $saved_via;
		}

		return array(
			'id'          => $new_id,
			'status'      => $status,
			'edit_link'   => get_edit_post_link( $new_id, 'raw' ),
			'preview'     => get_preview_post_link( $new_id ),
			'copied_meta' => $copied,
			'flags_from'  => $template_src ?: null,
			'saved_via'   => $saved_via,
			'summary'     => sprintf( 'Created %s "%s"%s', $post_type, $args['title'], $source ? ' (clone of #' . $source->ID . ')' : '' ),
		);
	}

	/** An empty document with the same root shape as an existing one (object root vs. plain list). */
	private static function empty_tree_like( $post_id ) {
		$tree = $post_id ? Pro_Extended_CS_Store::get_tree( $post_id ) : null;
		if ( is_array( $tree ) && isset( $tree['_type'] ) ) {
			$k          = Pro_Extended_CS_Store::child_key( $tree );
			$tree[ $k ? $k : '_modules' ] = array();
			unset( $tree['_id'] );
			return $tree;
		}
		return array();
	}

	private static function latest_cornerstone_post( $post_type ) {
		$ids = get_posts(
			array(
				'post_type'      => $post_type,
				'post_status'    => 'any',
				'meta_key'       => Pro_Extended_CS_Store::DATA_KEY, // phpcs:ignore WordPress.DB.SlowDBQuery
				'posts_per_page' => 1,
				'orderby'        => 'modified',
				'order'          => 'DESC',
				'fields'         => 'ids',
			)
		);
		return $ids ? (int) $ids[0] : 0;
	}

	private static function normalize_tree_arg( $tree ) {
		if ( is_string( $tree ) ) {
			$tree = json_decode( $tree, true );
		}
		return is_array( $tree ) ? $tree : new WP_Error( 'bad_tree', '`tree` must be a JSON object or array.' );
	}

	private static function save_element_tree( $args ) {
		$tree = self::normalize_tree_arg( $args['tree'] );
		if ( is_wp_error( $tree ) ) {
			return $tree;
		}
		$existing = Pro_Extended_CS_Store::get_tree( $args['id'] );
		// Caller passed a list of elements but the stored root is an object: keep the root, swap its children.
		if ( is_array( $existing ) && isset( $existing['_type'] ) && ! isset( $tree['_type'] ) ) {
			$list = &Pro_Extended_CS_Store::roots( $existing );
			$list = array_values( $tree );
			unset( $list );
			$tree = $existing;
		}
		Pro_Extended_CS_Store::backup( $args['id'], 'cs_save_element_tree' );
		$via = Pro_Extended_CS_Store::save_tree( $args['id'], $tree );
		if ( is_wp_error( $via ) ) {
			return $via;
		}
		if ( isset( $args['post_content'] ) && 'raw' === $via ) {
			wp_update_post(
				wp_slash(
					array(
						'ID'           => $args['id'],
						'post_content' => $args['post_content'],
					)
				)
			);
		}
		$count = 0;
		Pro_Extended_CS_Store::walk(
			$tree,
			function () use ( &$count ) {
				$count++;
			}
		);
		return array(
			'id'       => $args['id'],
			'elements' => $count,
			'saved_via' => $via,
			'outline'  => Pro_Extended_CS_Store::outline( $tree ),
			'summary'  => "Saved element tree ($count elements) via $via",
		);
	}

	/** Reference to the element at a dotted path within the tree. */
	private static function &node_ref( array &$tree, $path ) {
		$err   = null;
		$parts = array_map( 'intval', explode( '.', (string) $path ) );
		$list  = &Pro_Extended_CS_Store::roots( $tree );
		$node  = null;
		foreach ( $parts as $n => $i ) {
			if ( ! isset( $list[ $i ] ) || ! is_array( $list[ $i ] ) ) {
				$err = new WP_Error( 'bad_path', 'No element at path ' . $path );
				return $err;
			}
			$node = &$list[ $i ];
			if ( $n < count( $parts ) - 1 ) {
				$k = Pro_Extended_CS_Store::child_key( $node );
				if ( null === $k ) {
					$err = new WP_Error( 'bad_path', 'Element at ' . implode( '.', array_slice( $parts, 0, $n + 1 ) ) . ' has no children' );
					return $err;
				}
				unset( $list );
				$list = &$node[ $k ];
				unset( $node );
			}
		}
		return $node;
	}

	private static function node_at( array $tree, $path ) {
		$ref = &self::node_ref( $tree, $path );
		return $ref;
	}

	private static function update_element( $args ) {
		$tree = Pro_Extended_CS_Store::get_tree( $args['id'] );
		if ( null === $tree ) {
			return new WP_Error( 'no_tree', 'This post has no Cornerstone data.' );
		}
		$path   = (string) $args['path'];
		$parts  = explode( '.', $path );
		$index  = (int) array_pop( $parts );
		$check  = self::node_at( $tree, $path );
		if ( is_wp_error( $check ) ) {
			return $check;
		}

		Pro_Extended_CS_Store::backup( $args['id'], 'cs_update_element ' . $path );
		$done = array();

		// Sibling list that contains the target.
		if ( $parts ) {
			$parent = &self::node_ref( $tree, implode( '.', $parts ) );
			$list   = &$parent[ Pro_Extended_CS_Store::child_key( $parent ) ];
		} else {
			$list = &Pro_Extended_CS_Store::roots( $tree );
		}
		$next = Pro_Extended_CS_Store::max_numeric_id( $tree ) + 1;

		if ( ! empty( $args['set'] ) && is_array( $args['set'] ) ) {
			$list[ $index ] = array_replace_recursive( $list[ $index ], $args['set'] );
			$done[]         = 'set ' . implode( ', ', array_keys( $args['set'] ) );
		}
		if ( ! empty( $args['unset'] ) ) {
			foreach ( (array) $args['unset'] as $k ) {
				unset( $list[ $index ][ $k ] );
			}
			$done[] = 'unset ' . implode( ', ', (array) $args['unset'] );
		}
		if ( ! empty( $args['insert'] ) && is_array( $args['insert'] ) ) {
			$new = Pro_Extended_CS_Store::reassign_ids( array_values( $args['insert'] ), $next );
			$pos = isset( $args['position'] ) ? $args['position'] : 'after';
			if ( 'inside' === $pos ) {
				$k = Pro_Extended_CS_Store::child_key( $list[ $index ] );
				$k = $k ? $k : '_modules';
				$list[ $index ][ $k ] = array_merge( isset( $list[ $index ][ $k ] ) ? $list[ $index ][ $k ] : array(), $new );
			} else {
				array_splice( $list, 'before' === $pos ? $index : $index + 1, 0, $new );
				if ( 'before' === $pos ) {
					$index += count( $new ); // Target moved down.
				}
			}
			$done[] = 'inserted ' . count( $new ) . ' ' . $pos;
		}
		if ( ! empty( $args['remove'] ) ) {
			array_splice( $list, $index, 1 );
			$done[] = 'removed';
		}
		unset( $list, $parent );

		$via = Pro_Extended_CS_Store::save_tree( $args['id'], $tree );
		if ( is_wp_error( $via ) ) {
			return $via;
		}
		return array(
			'id'        => $args['id'],
			'saved_via' => $via,
			'outline'   => Pro_Extended_CS_Store::outline( $tree ),
			'summary' => "Element $path: " . ( $done ? implode( '; ', $done ) : 'no changes' ),
		);
	}

	/* --------------------------------------------------------- HTML import */

	private static function pick_type( array $types, array $patterns ) {
		foreach ( $patterns as $re ) {
			$best = null;
			foreach ( $types as $t => $info ) {
				if ( preg_match( $re, $t ) && ( null === $best || $info['count'] > $types[ $best ]['count'] ) ) {
					$best = $t;
				}
			}
			if ( $best ) {
				return $best;
			}
		}
		return null;
	}

	/**
	 * Wrapper settings that make section/row/column invisible around imported
	 * HTML: no padding, no gaps, full width (the HTML brings its own container).
	 * Key names from cornerstone/includes/elements/definitions/*.php (CS 7.5).
	 */
	const NEUTRAL_WRAPPERS = array(
		'section'       => array( 'section_padding' => '0px 0px 0px 0px' ),
		'layout-row'    => array(
			'layout_row_global_container' => false,
			'layout_row_gap_column'       => '0px',
			'layout_row_gap_row'          => '0px',
			'layout_row_padding'          => '0px 0px 0px 0px',
		),
		'layout-column' => array( 'layout_column_padding' => '0px 0px 0px 0px' ),
	);

	/**
	 * A clean element of a type, built from a real example: only its internal
	 * `_` keys (version/breakpoint markers) are kept, so none of the example's
	 * styling (backgrounds, padding, labels) leaks into the new element.
	 */
	private static function blank_from_example( array $types, $type ) {
		if ( ! isset( $types[ $type ] ) ) {
			return null;
		}
		$el = array();
		foreach ( $types[ $type ]['examples'][0]['element'] as $k => $v ) {
			if ( '_' === $k[0] && ! in_array( $k, array( '_label', '_id' ), true ) ) {
				$el[ $k ] = $v;
			}
		}
		if ( isset( self::NEUTRAL_WRAPPERS[ $type ] ) ) {
			$el = array_merge( $el, self::NEUTRAL_WRAPPERS[ $type ] );
		}
		$el['_modules'] = array();
		return $el;
	}

	/** The key in a raw-content example that holds its HTML. */
	private static function content_key( array $el ) {
		foreach ( array( 'raw_content', 'content', 'code' ) as $k ) {
			if ( array_key_exists( $k, $el ) ) {
				return $k;
			}
		}
		foreach ( $el as $k => $v ) {
			if ( is_string( $v ) && preg_match( '/content$/', $k ) ) {
				return $k;
			}
		}
		return null;
	}

	/** Split body HTML into top-level chunks at <section>/<header>/<footer>/<main>/<nav> boundaries. */
	private static function split_sections( $html ) {
		if ( ! class_exists( 'DOMDocument' ) ) {
			return array( $html );
		}
		$doc  = new DOMDocument();
		$prev = libxml_use_internal_errors( true );
		$doc->loadHTML( '<?xml encoding="utf-8"?><div id="pxroot">' . $html . '</div>', LIBXML_HTML_NOIMPLIED | LIBXML_HTML_NODEFDTD );
		libxml_clear_errors();
		libxml_use_internal_errors( $prev );
		$root = $doc->getElementById( 'pxroot' );
		if ( ! $root ) {
			return array( $html );
		}
		// Descend through a single wrapper (e.g. <div class="page"><section>…) to reach the real sections.
		while ( 1 === self::element_children_count( $root ) && ! preg_match( '/^(section|header|footer|main|nav)$/i', self::first_element( $root )->nodeName ) ) {
			$root = self::first_element( $root );
		}
		$chunks = array();
		$buffer = '';
		foreach ( iterator_to_array( $root->childNodes ) as $node ) {
			$out = $doc->saveHTML( $node );
			if ( XML_ELEMENT_NODE === $node->nodeType && preg_match( '/^(section|header|footer|main|nav|article|aside)$/i', $node->nodeName ) ) {
				if ( '' !== trim( $buffer ) ) {
					$chunks[] = $buffer;
				}
				$chunks[] = $out;
				$buffer   = '';
			} else {
				$buffer .= $out;
			}
		}
		if ( '' !== trim( $buffer ) ) {
			$chunks[] = $buffer;
		}
		return $chunks ? $chunks : array( $html );
	}

	private static function element_children_count( DOMNode $n ) {
		$c = 0;
		foreach ( $n->childNodes as $ch ) {
			if ( XML_ELEMENT_NODE === $ch->nodeType ) {
				$c++;
			} elseif ( XML_TEXT_NODE === $ch->nodeType && '' !== trim( $ch->textContent ) ) {
				return 99;
			}
		}
		return $c;
	}

	private static function first_element( DOMNode $n ) {
		foreach ( $n->childNodes as $ch ) {
			if ( XML_ELEMENT_NODE === $ch->nodeType ) {
				return $ch;
			}
		}
		return null;
	}

	private static function import_html( $args ) {
		$html = (string) $args['html'];
		$css  = isset( $args['css'] ) ? (string) $args['css'] : '';

		// Accept full documents: pull inline <style> into $css and keep only the body.
		if ( preg_match_all( '#<style[^>]*>(.*?)</style>#is', $html, $m ) && preg_match( '#<head#i', $html ) ) {
			$css .= "\n" . implode( "\n", $m[1] );
		}
		if ( preg_match( '#<body[^>]*>(.*)</body>#is', $html, $m ) ) {
			$html = $m[1];
		}

		$scan  = self::scan_catalog( 300 );
		$types = $scan['types'];

		$raw_type = ! empty( $args['raw_type'] ) ? $args['raw_type'] : self::pick_type( $types, array( '/^raw-content$/', '/raw/', '/^code$/', '/code/' ) );
		if ( ! $raw_type || ! isset( $types[ $raw_type ] ) ) {
			return new WP_Error(
				'no_raw_example',
				'Could not find a Raw Content / Code element on this site to copy. In Cornerstone, add one "Raw Content" (or Code) element to any page and save it once, then retry. Found types: ' . implode( ', ', array_keys( $types ) )
			);
		}
		$raw_blank = self::blank_from_example( $types, $raw_type );
		$ckey      = self::content_key( $raw_blank );
		if ( ! $ckey ) {
			return new WP_Error( 'no_content_key', "Element type $raw_type has no recognisable content key. Keys: " . implode( ', ', array_keys( $raw_blank ) ) );
		}

		if ( ! empty( $args['wrapper_types'] ) ) {
			$wrapper_types = array_values( (array) $args['wrapper_types'] );
		} else {
			$wrapper_types = array_values(
				array_filter(
					array(
						self::pick_type( $types, array( '/^section$/', '/^layout-section$/', '/section/' ) ),
						self::pick_type( $types, array( '/^layout-row$/', '/^row$/', '/row/' ) ),
						self::pick_type( $types, array( '/^layout-column$/', '/^column$/', '/column|^col/' ) ),
					)
				)
			);
		}
		foreach ( $wrapper_types as $wt ) {
			if ( ! isset( $types[ $wt ] ) ) {
				return new WP_Error( 'no_wrapper_example', "No example of wrapper type $wt on this site." );
			}
		}

		// Target page.
		$created = null;
		if ( empty( $args['id'] ) ) {
			$created = self::create_page(
				array(
					'title' => ! empty( $args['title'] ) ? $args['title'] : 'Imported design ' . gmdate( 'Y-m-d H:i' ),
				)
			);
			if ( is_wp_error( $created ) ) {
				return $created;
			}
			$post_id = $created['id'];
		} else {
			$post_id = (int) $args['id'];
		}

		$chunks = ( ! isset( $args['sections'] ) || $args['sections'] ) ? self::split_sections( $html ) : array( $html );

		$css_target = isset( $args['css_target'] ) ? $args['css_target'] : 'inline';
		$css_note   = null;
		if ( '' !== trim( $css ) && 'page_settings' === $css_target ) {
			$key = self::detect_css_setting_key( $post_id );
			if ( $key ) {
				$settings         = Pro_Extended_CS_Store::decode( get_post_meta( $post_id, Pro_Extended_CS_Store::SETTINGS_KEY, true ) );
				$settings         = is_array( $settings ) ? $settings : array();
				$settings[ $key ] = $css;
				$css_note         = "CSS written to page setting `$key`";
			} else {
				$css_target = 'inline';
				$css_note   = 'No custom-CSS setting key found on any page; fell back to inline <style>.';
			}
		}
		if ( '' !== trim( $css ) && 'inline' === $css_target ) {
			$chunks[0] = "<style>\n" . trim( $css ) . "\n</style>\n" . $chunks[0];
			$css_note  = $css_note ? $css_note : 'CSS inlined as <style> in the first element';
		}

		$tree = Pro_Extended_CS_Store::get_tree( $post_id );
		$tree = null === $tree ? array() : $tree;
		$next = Pro_Extended_CS_Store::max_numeric_id( $tree ) + 1;

		$new_sections = array();
		foreach ( $chunks as $chunk ) {
			$el          = $raw_blank;
			$el[ $ckey ] = trim( $chunk );
			for ( $i = count( $wrapper_types ) - 1; $i >= 0; $i-- ) {
				$wrap = self::blank_from_example( $types, $wrapper_types[ $i ] );
				$k    = Pro_Extended_CS_Store::child_key( $wrap );
				$k    = $k ? $k : '_modules';
				$wrap[ $k ] = array( $el );
				$el         = $wrap;
			}
			$new_sections[] = $el;
		}
		$new_sections = Pro_Extended_CS_Store::reassign_ids( $new_sections, $next );

		Pro_Extended_CS_Store::backup( $post_id, 'cs_import_html' );
		$list = &Pro_Extended_CS_Store::roots( $tree );
		$list = ( isset( $args['mode'] ) && 'append' === $args['mode'] ) ? array_merge( $list, $new_sections ) : $new_sections;
		unset( $list );

		$update = array( 'elements' => Pro_Extended_CS_Store::roots_of( $tree ) );
		if ( isset( $settings ) ) {
			$update['settings'] = $settings;
		}
		$via = Pro_Extended_CS_Store::save_via_cornerstone( $post_id, $update );
		if ( is_wp_error( $via ) ) {
			return $via;
		}
		if ( true === $via ) {
			$via = 'cornerstone';
		} else {
			Pro_Extended_CS_Store::save_tree( $post_id, $tree );
			if ( isset( $settings ) ) {
				Pro_Extended_CS_Store::put_meta( $post_id, Pro_Extended_CS_Store::SETTINGS_KEY, $settings );
			}
			$via = 'raw';
		}

		self::purge_cache( array( 'id' => $post_id ) );

		return array(
			'id'            => $post_id,
			'created'       => (bool) $created,
			'preview'       => get_preview_post_link( $post_id ),
			'raw_type'      => $raw_type,
			'content_key'   => $ckey,
			'wrapper_types' => $wrapper_types,
			'sections'      => count( $new_sections ),
			'css'           => $css_note,
			'saved_via'     => $via,
			'outline'       => Pro_Extended_CS_Store::outline( $tree ),
			'summary'       => sprintf( 'Imported HTML as %d %s section(s)', count( $new_sections ), $raw_type ),
		);
	}

	/** Find the _cornerstone_settings key used for page custom CSS, from this or any other page. */
	private static function detect_css_setting_key( $post_id ) {
		$candidates = array_merge( array( $post_id ), get_posts(
			array(
				'post_type'      => array_values( get_post_types() ),
				'post_status'    => 'any',
				'meta_key'       => Pro_Extended_CS_Store::SETTINGS_KEY, // phpcs:ignore WordPress.DB.SlowDBQuery
				'posts_per_page' => 50,
				'fields'         => 'ids',
			)
		) );
		foreach ( $candidates as $pid ) {
			$s = Pro_Extended_CS_Store::decode( get_post_meta( $pid, Pro_Extended_CS_Store::SETTINGS_KEY, true ) );
			if ( is_array( $s ) ) {
				foreach ( array_keys( $s ) as $k ) {
					if ( preg_match( '/css$/i', $k ) ) {
						return $k;
					}
				}
			}
		}
		return null;
	}

	private static function update_settings( $args ) {
		$current = Pro_Extended_CS_Store::decode( get_post_meta( $args['id'], Pro_Extended_CS_Store::SETTINGS_KEY, true ) );
		$current = is_array( $current ) ? $current : array();
		Pro_Extended_CS_Store::backup( $args['id'], 'cs_update_settings' );
		foreach ( (array) $args['settings'] as $k => $v ) {
			if ( null === $v ) {
				unset( $current[ $k ] );
			} else {
				$current[ $k ] = $v;
			}
		}
		$raw     = get_post_meta( $args['id'], Pro_Extended_CS_Store::SETTINGS_KEY, true );
		$as_json = '' === $raw || is_string( $raw );
		Pro_Extended_CS_Store::put_meta( $args['id'], Pro_Extended_CS_Store::SETTINGS_KEY, $current, $as_json );
		delete_post_meta( $args['id'], '_cs_generated_tss' );
		return array(
			'id'       => $args['id'],
			'settings' => $current,
			'summary'  => 'Updated settings: ' . implode( ', ', array_keys( (array) $args['settings'] ) ),
		);
	}

	/* ------------------------------------------------------------- options */

	private static function option_allowed( $name ) {
		foreach ( self::OPTION_PREFIXES as $p ) {
			if ( 0 === strpos( $name, $p ) ) {
				return true;
			}
		}
		return false;
	}

	private static function list_options( $args ) {
		global $wpdb;
		$where = array();
		foreach ( self::OPTION_PREFIXES as $p ) {
			$where[] = $wpdb->prepare( 'option_name LIKE %s', $wpdb->esc_like( $p ) . '%' );
		}
		// phpcs:ignore WordPress.DB.PreparedSQL.NotPrepared, WordPress.DB.DirectDatabaseQuery
		$rows = $wpdb->get_results( "SELECT option_name, LENGTH(option_value) AS size FROM {$wpdb->options} WHERE (" . implode( ' OR ', $where ) . ') ORDER BY option_name' );
		$out  = array();
		foreach ( $rows as $r ) {
			if ( false === strpos( $r->option_name, 'pro_extended' ) ) {
				$out[ $r->option_name ] = (int) $r->size;
			}
		}
		return array( 'options' => $out );
	}

	private static function get_option( $args ) {
		if ( ! self::option_allowed( $args['name'] ) || false !== strpos( $args['name'], 'pro_extended' ) ) {
			return new WP_Error( 'forbidden', 'Only Cornerstone/Pro options can be read.' );
		}
		if ( preg_match( '/licen[cs]e|key|token|secret|password/i', $args['name'] ) ) {
			return new WP_Error( 'forbidden', 'License/credential options are not exposed.' );
		}
		return array(
			'name'  => $args['name'],
			'value' => Pro_Extended_CS_Store::decode( get_option( $args['name'] ) ),
		);
	}

	private static function update_option( $args ) {
		if ( ! current_user_can( 'manage_options' ) ) {
			return new WP_Error( 'forbidden', 'Only administrators can change site options.' );
		}
		if ( ! self::option_allowed( $args['name'] ) || preg_match( '/licen[cs]e|key|token|secret|password|pro_extended/i', $args['name'] ) ) {
			return new WP_Error( 'forbidden', 'This option cannot be changed via MCP.' );
		}
		$old   = get_option( $args['name'] );
		$value = $args['value'];
		if ( is_array( $value ) && is_string( $old ) && '' !== $old && in_array( $old[0], array( '{', '[' ), true ) ) {
			$value = wp_json_encode( $value, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE );
		}
		update_option( $args['name'], $value );
		return array(
			'name'     => $args['name'],
			'previous' => Pro_Extended_CS_Store::decode( $old ),
			'summary'  => 'Updated option ' . $args['name'],
		);
	}

	/* --------------------------------------------------------------- media */

	private static function upload_media( $args ) {
		if ( ! current_user_can( 'upload_files' ) ) {
			return new WP_Error( 'forbidden', 'This user cannot upload files.' );
		}
		require_once ABSPATH . 'wp-admin/includes/file.php';
		require_once ABSPATH . 'wp-admin/includes/media.php';
		require_once ABSPATH . 'wp-admin/includes/image.php';

		$title = isset( $args['title'] ) ? $args['title'] : null;
		if ( ! empty( $args['url'] ) ) {
			$url = esc_url_raw( $args['url'] );
			$tmp = download_url( $url, 60 );
			if ( is_wp_error( $tmp ) ) {
				return $tmp;
			}
			$name = ! empty( $args['filename'] ) ? $args['filename'] : basename( wp_parse_url( $url, PHP_URL_PATH ) );
		} elseif ( ! empty( $args['base64'] ) && ! empty( $args['filename'] ) ) {
			$data = base64_decode( preg_replace( '#^data:[^,]+,#', '', $args['base64'] ), true );
			if ( false === $data ) {
				return new WP_Error( 'bad_base64', 'Invalid base64 data.' );
			}
			$tmp = wp_tempnam( $args['filename'] );
			file_put_contents( $tmp, $data ); // phpcs:ignore WordPress.WP.AlternativeFunctions
			$name = $args['filename'];
		} else {
			return new WP_Error( 'missing', 'Provide `url`, or `base64` with `filename`.' );
		}

		$att_id = media_handle_sideload(
			array(
				'name'     => sanitize_file_name( $name ),
				'tmp_name' => $tmp,
			),
			0,
			$title
		);
		if ( is_wp_error( $att_id ) ) {
			@unlink( $tmp ); // phpcs:ignore WordPress.PHP.NoSilencedErrors
			return $att_id;
		}
		if ( isset( $args['alt'] ) ) {
			update_post_meta( $att_id, '_wp_attachment_image_alt', sanitize_text_field( $args['alt'] ) );
		}
		return array(
			'id'      => $att_id,
			'url'     => wp_get_attachment_url( $att_id ),
			'summary' => 'Uploaded ' . $name,
		);
	}

	private static function list_media( $args ) {
		$q     = new WP_Query(
			array(
				'post_type'      => 'attachment',
				'post_status'    => 'inherit',
				's'              => isset( $args['search'] ) ? $args['search'] : '',
				'posts_per_page' => min( 200, max( 1, isset( $args['per_page'] ) ? (int) $args['per_page'] : 50 ) ),
				'paged'          => max( 1, isset( $args['page'] ) ? (int) $args['page'] : 1 ),
			)
		);
		$items = array();
		foreach ( $q->posts as $a ) {
			$items[] = array(
				'id'       => $a->ID,
				'url'      => wp_get_attachment_url( $a->ID ),
				'filename' => basename( (string) get_attached_file( $a->ID ) ),
				'mime'     => $a->post_mime_type,
				'alt'      => get_post_meta( $a->ID, '_wp_attachment_image_alt', true ),
			);
		}
		return array(
			'total' => (int) $q->found_posts,
			'items' => $items,
		);
	}

	/* ------------------------------------------------------ backups, cache */

	private static function list_backups( $args ) {
		return array(
			'id'      => $args['id'],
			'backups' => Pro_Extended_CS_Store::list_backups( $args['id'] ),
		);
	}

	private static function restore_backup( $args ) {
		$index = isset( $args['index'] ) ? (int) $args['index'] : 0;
		$res   = Pro_Extended_CS_Store::restore( $args['id'], $index );
		if ( is_wp_error( $res ) ) {
			return $res;
		}
		self::purge_cache( array( 'id' => $args['id'] ) );
		return array(
			'id'      => $args['id'],
			'summary' => 'Restored backup #' . $index,
		);
	}

	private static function dev_source( $args ) {
		if ( ! current_user_can( 'manage_options' ) ) {
			return new WP_Error( 'forbidden', 'Administrators only.' );
		}
		$root = realpath( ( isset( $args['root'] ) && 'plugins' === $args['root'] ) ? WP_PLUGIN_DIR : get_template_directory() );
		$rel  = isset( $args['path'] ) ? ltrim( (string) $args['path'], '/' ) : '';
		$full = realpath( $root . '/' . $rel );
		if ( ! $full || 0 !== strpos( $full, $root ) ) {
			return new WP_Error( 'bad_path', 'Path must be inside the selected root directory.' );
		}

		if ( ! empty( $args['grep'] ) ) {
			$re = '~' . str_replace( '~', '\\~', $args['grep'] ) . '~i';
			if ( false === @preg_match( $re, '' ) ) { // phpcs:ignore WordPress.PHP.NoSilencedErrors
				return new WP_Error( 'bad_regex', 'Invalid pattern.' );
			}
			$hits  = array();
			$files = is_dir( $full ) ? new RecursiveIteratorIterator( new RecursiveDirectoryIterator( $full, FilesystemIterator::SKIP_DOTS ) ) : array( new SplFileInfo( $full ) );
			foreach ( $files as $f ) {
				if ( 'php' !== $f->getExtension() ) {
					continue;
				}
				foreach ( file( $f->getPathname() ) as $n => $line ) {
					if ( preg_match( $re, $line ) ) {
						$hits[] = substr( $f->getPathname(), strlen( $root ) + 1 ) . ':' . ( $n + 1 ) . ': ' . trim( substr( $line, 0, 240 ) );
						if ( count( $hits ) >= 300 ) {
							return array( 'hits' => $hits, 'truncated' => true );
						}
					}
				}
			}
			return array( 'hits' => $hits );
		}

		if ( is_dir( $full ) ) {
			$items = array();
			foreach ( scandir( $full ) as $f ) {
				if ( '.' !== $f[0] ) {
					$items[] = is_dir( $full . '/' . $f ) ? $f . '/' : $f;
				}
			}
			return array( 'path' => $rel, 'items' => $items );
		}

		$lines = file( $full );
		$start = max( 1, isset( $args['start'] ) ? (int) $args['start'] : 1 );
		$end   = min( count( $lines ), isset( $args['end'] ) ? (int) $args['end'] : $start + 399 );
		$out   = array();
		for ( $i = $start; $i <= $end; $i++ ) {
			$out[] = $i . "\t" . rtrim( $lines[ $i - 1 ], "\r\n" );
		}
		return array(
			'file'  => $rel,
			'lines' => count( $lines ),
			'range' => "$start-$end",
			'code'  => implode( "\n", $out ),
		);
	}

	/* ------------------------------------------------------ layouts, menus */

	private static function layout_post_types() {
		return array( 'cs_header', 'cs_footer', 'cs_layout', 'cs_layout_single', 'cs_layout_archive', 'cs_layout_single_wc', 'cs_layout_archive_wc' );
	}

	private static function get_layout( $args ) {
		$p = get_post( $args['id'] );
		if ( ! in_array( $p->post_type, self::layout_post_types(), true ) ) {
			return new WP_Error( 'not_layout', 'Not a header/footer/layout document.' );
		}
		$data    = json_decode( $p->post_content, true );
		$regions = isset( $data['regions'] ) ? $data['regions'] : array();
		$outline = array();
		foreach ( $regions as $region => $els ) {
			$outline[] = "== $region";
			$outline[] = Pro_Extended_CS_Store::outline( $els );
		}
		return array(
			'id'        => $p->ID,
			'title'     => $p->post_title,
			'post_type' => $p->post_type,
			'settings'  => isset( $data['settings'] ) ? $data['settings'] : array(),
			'outline'   => implode( "\n", $outline ),
			'regions'   => $regions,
		);
	}

	/** Stamp `_region` on every element (Cornerstone requires it in layouts). */
	private static function stamp_region( array $els, $region ) {
		foreach ( $els as &$el ) {
			if ( ! is_array( $el ) ) {
				continue;
			}
			$el['_region'] = $region;
			if ( isset( $el['_modules'] ) && is_array( $el['_modules'] ) ) {
				$el['_modules'] = self::stamp_region( $el['_modules'], $region );
			}
		}
		return $els;
	}

	private static function save_layout( $args ) {
		$id = ! empty( $args['id'] ) ? (int) $args['id'] : 0;
		if ( ! $id && empty( $args['type'] ) ) {
			return new WP_Error( 'missing', 'Give `type` (header|footer) when creating.' );
		}
		if ( ! current_user_can( 'edit_theme_options' ) && ! current_user_can( 'manage_options' ) ) {
			return new WP_Error( 'forbidden', 'Editing headers/footers requires theme-options access.' );
		}
		$update = array();
		if ( ! empty( $args['title'] ) ) {
			$update['title'] = $args['title'];
		}
		if ( isset( $args['settings'] ) && is_array( $args['settings'] ) ) {
			$update['settings'] = $args['settings'];
		}
		if ( ! $id ) {
			$update['settings'] = array_merge( array( 'layout_type' => $args['type'] ), isset( $update['settings'] ) ? $update['settings'] : array() );
		}
		if ( isset( $args['regions'] ) && is_array( $args['regions'] ) ) {
			$regions = array();
			foreach ( $args['regions'] as $region => $els ) {
				$regions[ $region ] = self::stamp_region( array_values( (array) $els ), $region );
			}
			$update['elements'] = $regions;
		}
		if ( $id ) {
			Pro_Extended_CS_Store::backup( $id, 'cs_save_layout' );
		}
		$res = Pro_Extended_CS_Store::save_layout( $id ?: null, 'footer' === ( isset( $args['type'] ) ? $args['type'] : '' ) ? 'layout:footer' : 'layout:header', $update );
		if ( is_wp_error( $res ) ) {
			return $res;
		}
		$new_id = isset( $res['id'] ) ? (int) $res['id'] : $id;
		$out    = self::get_layout( array( 'id' => $new_id ) );
		unset( $out['regions'] );
		$out['summary'] = ( $id ? 'Updated ' : 'Created ' ) . ( isset( $args['type'] ) ? $args['type'] : 'layout' ) . ' "' . get_the_title( $new_id ) . '"';
		return $out;
	}

	private static function save_component( $args ) {
		$id = ! empty( $args['id'] ) ? (int) $args['id'] : 0;
		if ( $id ) {
			Pro_Extended_CS_Store::backup( $id, 'cs_save_component' );
		}
		$res = Pro_Extended_CS_Store::save_component(
			$id ?: null,
			isset( $args['title'] ) ? $args['title'] : '',
			(array) $args['elements'],
			isset( $args['settings'] ) && is_array( $args['settings'] ) ? $args['settings'] : null
		);
		if ( is_wp_error( $res ) ) {
			return $res;
		}
		$new_id = isset( $res['id'] ) ? (int) $res['id'] : $id;
		return array(
			'id'      => $new_id,
			'title'   => get_the_title( $new_id ),
			'status'  => get_post_status( $new_id ),
			'element' => array(
				'_type'           => 'global-block',
				'global_block_id' => (string) $new_id,
			),
			'summary' => ( $id ? 'Updated' : 'Created' ) . ' component "' . get_the_title( $new_id ) . '" (' . $new_id . ')',
		);
	}

	private static function gf_ready() {
		if ( ! class_exists( 'GFAPI' ) ) {
			return new WP_Error( 'no_gravityforms', 'Gravity Forms is not active.' );
		}
		if ( ! current_user_can( 'manage_options' ) && ! current_user_can( 'gravityforms_edit_forms' ) ) {
			return new WP_Error( 'forbidden', 'Editing Gravity Forms requires an administrator.' );
		}
		return true;
	}

	private static function gf_list_forms( $args ) {
		$ok = self::gf_ready();
		if ( is_wp_error( $ok ) ) {
			return $ok;
		}
		$out = array();
		foreach ( GFAPI::get_forms( null ) as $f ) {
			$out[] = array(
				'id'      => (int) $f['id'],
				'title'   => $f['title'],
				'active'  => (bool) rgar( $f, 'is_active', true ),
				'fields'  => count( (array) rgar( $f, 'fields', array() ) ),
				'entries' => (int) GFAPI::count_entries( $f['id'] ),
			);
		}
		return array( 'forms' => $out );
	}

	private static function gf_save_form( $args ) {
		$ok = self::gf_ready();
		if ( is_wp_error( $ok ) ) {
			return $ok;
		}
		$form = (array) $args['form'];
		$id   = ! empty( $args['id'] ) ? (int) $args['id'] : 0;
		if ( $id ) {
			$form['id'] = $id;
			$res        = GFAPI::update_form( $form, $id );
			$res        = is_wp_error( $res ) ? $res : $id;
		} else {
			unset( $form['id'] );
			$res = GFAPI::add_form( $form );
		}
		if ( is_wp_error( $res ) ) {
			return $res;
		}
		$saved = GFAPI::get_form( (int) $res );
		return array(
			'id'        => (int) $res,
			'title'     => $saved['title'],
			'fields'    => array_map(
				function ( $f ) {
					return array( 'id' => $f->id, 'type' => $f->type, 'label' => $f->label );
				},
				$saved['fields']
			),
			'shortcode' => '[gravityform id="' . (int) $res . '" title="false" description="true" ajax="true"]',
			'summary'   => ( $id ? 'Updated' : 'Created' ) . ' Gravity Form "' . $saved['title'] . '" (' . (int) $res . ')',
		);
	}

	private static function list_menus( $args ) {
		$out = array();
		foreach ( wp_get_nav_menus() as $m ) {
			$out[] = array(
				'id'    => $m->term_id,
				'ref'   => 'menu:' . $m->term_id,
				'name'  => $m->name,
				'items' => (int) $m->count,
			);
		}
		return array( 'menus' => $out );
	}

	private static function save_menu( $args ) {
		if ( ! current_user_can( 'edit_theme_options' ) ) {
			return new WP_Error( 'forbidden', 'Editing menus requires edit_theme_options.' );
		}
		$menu = wp_get_nav_menu_object( $args['name'] );
		if ( $menu ) {
			$menu_id = $menu->term_id;
			foreach ( (array) wp_get_nav_menu_items( $menu_id, array( 'post_status' => 'any' ) ) as $item ) {
				wp_delete_post( $item->ID, true );
			}
		} else {
			$menu_id = wp_create_nav_menu( $args['name'] );
			if ( is_wp_error( $menu_id ) ) {
				return $menu_id;
			}
		}
		$count = 0;
		$add   = function ( $items, $parent ) use ( &$add, $menu_id, &$count ) {
			foreach ( (array) $items as $i => $it ) {
				$item_id = wp_update_nav_menu_item(
					$menu_id,
					0,
					array(
						'menu-item-title'     => isset( $it['title'] ) ? $it['title'] : '',
						'menu-item-url'       => isset( $it['url'] ) ? $it['url'] : '#',
						'menu-item-type'      => 'custom',
						'menu-item-status'    => 'publish',
						'menu-item-parent-id' => $parent,
						'menu-item-position'  => $i + 1,
						'menu-item-classes'   => isset( $it['class'] ) ? $it['class'] : '',
					)
				);
				if ( ! is_wp_error( $item_id ) ) {
					$count++;
					if ( ! empty( $it['children'] ) ) {
						$add( $it['children'], $item_id );
					}
				}
			}
		};
		$add( $args['items'], 0 );
		return array(
			'id'      => $menu_id,
			'ref'     => 'menu:' . $menu_id,
			'items'   => $count,
			'summary' => sprintf( 'Saved menu "%s" (%d items)', $args['name'], $count ),
		);
	}

	private static function get_post_meta_all( $args ) {
		if ( ! current_user_can( 'manage_options' ) ) {
			return new WP_Error( 'forbidden', 'Administrators only.' );
		}
		$out = array();
		foreach ( get_post_meta( $args['id'] ) as $k => $vals ) {
			if ( ! empty( $args['prefix'] ) && 0 !== strpos( $k, $args['prefix'] ) ) {
				continue;
			}
			if ( preg_match( '/pass|token|secret|_edit_lock/i', $k ) ) {
				continue;
			}
			$v         = maybe_unserialize( $vals[0] );
			$out[ $k ] = Pro_Extended_CS_Store::decode( $v );
		}
		ksort( $out );
		$p = get_post( $args['id'] );
		return array(
			'id'        => $args['id'],
			'post_type' => $p->post_type,
			'title'     => $p->post_title,
			'meta'      => $out,
		);
	}

	private static function save_post_generic( $args ) {
		if ( ! current_user_can( 'manage_options' ) ) {
			return new WP_Error( 'forbidden', 'Administrators only.' );
		}
		$id = ! empty( $args['id'] ) ? (int) $args['id'] : 0;
		if ( ! $id && empty( $args['post_type'] ) ) {
			return new WP_Error( 'missing', 'Give post_type when creating.' );
		}
		$postarr = array();
		$map     = array(
			'title'   => 'post_title',
			'status'  => 'post_status',
			'content' => 'post_content',
			'excerpt' => 'post_excerpt',
			'slug'    => 'post_name',
			'date'    => 'post_date',
		);
		foreach ( $map as $k => $wp ) {
			if ( isset( $args[ $k ] ) ) {
				$postarr[ $wp ] = $args[ $k ];
			}
		}
		if ( $id ) {
			Pro_Extended_CS_Store::backup( $id, 'cs_save_post' );
			$postarr['ID'] = $id;
			$res           = wp_update_post( wp_slash( $postarr ), true );
		} else {
			$postarr['post_type'] = sanitize_key( $args['post_type'] );
			if ( ! isset( $postarr['post_status'] ) ) {
				$postarr['post_status'] = 'publish';
			}
			$res = wp_insert_post( wp_slash( $postarr ), true );
		}
		if ( is_wp_error( $res ) ) {
			return $res;
		}
		$id = (int) $res;
		foreach ( (array) ( isset( $args['meta'] ) ? $args['meta'] : array() ) as $k => $v ) {
			if ( null === $v ) {
				delete_post_meta( $id, $k );
			} else {
				update_post_meta( $id, $k, wp_slash( $v ) );
			}
		}
		foreach ( (array) ( isset( $args['terms'] ) ? $args['terms'] : array() ) as $tax => $names ) {
			wp_set_object_terms( $id, array_map( 'sanitize_text_field', (array) $names ), sanitize_key( $tax ) );
		}
		if ( ! empty( $args['featured_image'] ) ) {
			set_post_thumbnail( $id, (int) $args['featured_image'] );
		}
		$p = get_post( $id );
		return array(
			'id'        => $id,
			'post_type' => $p->post_type,
			'status'    => $p->post_status,
			'link'      => get_permalink( $id ),
			'summary'   => ( empty( $args['id'] ) ? 'Created ' : 'Updated ' ) . $p->post_type . ' "' . $p->post_title . '"',
		);
	}

	private static function mec_save_event( $args ) {
		if ( ! class_exists( 'MEC' ) ) {
			return new WP_Error( 'no_mec', 'Modern Events Calendar is not active.' );
		}
		if ( ! current_user_can( 'edit_posts' ) ) {
			return new WP_Error( 'forbidden', 'Cannot edit events.' );
		}
		$main = MEC::getInstance( 'app.libraries.main' );
		if ( ! $main || ! method_exists( $main, 'save_event' ) ) {
			return new WP_Error( 'no_api', 'MEC save_event() not found in this MEC version.' );
		}
		$post_id = ! empty( $args['post_id'] ) ? (int) $args['post_id'] : null;
		if ( $post_id ) {
			Pro_Extended_CS_Store::backup( $post_id, 'mec_save_event' );
		}
		$id = $main->save_event( (array) $args['event'], $post_id );
		if ( ! $id || is_wp_error( $id ) ) {
			return is_wp_error( $id ) ? $id : new WP_Error( 'mec_failed', 'MEC did not return an event id.' );
		}
		if ( ! empty( $args['featured_image'] ) ) {
			set_post_thumbnail( $id, (int) $args['featured_image'] );
		}
		if ( ! empty( $args['categories'] ) ) {
			wp_set_object_terms( $id, array_map( 'sanitize_text_field', (array) $args['categories'] ), 'mec_category' );
		}
		global $wpdb;
		$dates = $wpdb->get_results( $wpdb->prepare( "SELECT * FROM {$wpdb->prefix}mec_dates WHERE post_id = %d ORDER BY tstart LIMIT 10", $id ), ARRAY_A ); // phpcs:ignore WordPress.DB
		return array(
			'id'      => $id,
			'link'    => get_permalink( $id ),
			'dates'   => $dates,
			'meta'    => self::get_post_meta_all( array( 'id' => $id, 'prefix' => 'mec_' ) )['meta'],
			'summary' => ( $post_id ? 'Updated' : 'Created' ) . ' MEC event "' . get_the_title( $id ) . '"',
		);
	}

	private static function preview_link( $args ) {
		$hours = isset( $args['hours'] ) ? (int) $args['hours'] : 48;
		return array(
			'id'      => $args['id'],
			'url'     => Pro_Extended_Preview::create( $args['id'], $hours ),
			'expires' => gmdate( 'c', time() + max( 1, $hours ) * HOUR_IN_SECONDS ),
			'summary' => "Preview link created ({$hours}h)",
		);
	}

	private static function purge_cache( $args ) {
		$done = array();
		if ( ! empty( $args['id'] ) ) {
			$pid = (int) $args['id'];
			foreach ( array_keys( get_post_meta( $pid ) ) as $key ) {
				if ( Pro_Extended_CS_Store::is_cs_meta_key( $key ) && preg_match( '/generated|cache|_style(s)?$/i', $key ) ) {
					delete_post_meta( $pid, $key );
					$done[] = "deleted meta $key";
				}
			}
			clean_post_cache( $pid );
			$done[] = 'clean_post_cache';
			do_action( 'cs_purge_post_cache', $pid ); // Harmless if nothing listens.
		}
		if ( function_exists( 'cornerstone_cleanup_generated_styles' ) && ! empty( $args['all'] ) ) {
			cornerstone_cleanup_generated_styles(); // Drops compiled CSS for every document.
			$done[] = 'cornerstone_cleanup_generated_styles';
		}
		// Ask Cornerstone to drop its global generated CSS, if this version exposes a hook/function for it.
		foreach ( array( 'cs_purge_tmp', 'cornerstone_purge_cache', 'cs_purge_cache' ) as $hook ) {
			if ( has_action( $hook ) ) {
				do_action( $hook );
				$done[] = "do_action $hook";
			}
		}
		wp_cache_flush();
		$done[] = 'wp_cache_flush';

		if ( class_exists( 'WpeCommon' ) ) {
			foreach ( array( 'purge_memcached', 'purge_varnish_cache', 'clear_maxcdn_cache' ) as $m ) {
				if ( method_exists( 'WpeCommon', $m ) ) {
					call_user_func( array( 'WpeCommon', $m ) );
					$done[] = "WP Engine $m";
				}
			}
		}
		return array(
			'actions' => $done,
			'summary' => 'Purged caches',
		);
	}
}
