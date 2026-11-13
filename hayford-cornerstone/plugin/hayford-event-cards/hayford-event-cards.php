<?php
/**
 * Plugin Name:       Hayford Event Cards
 * Description:       [hf_event_cards] shortcode — upcoming Modern Events Calendar events as a responsive card grid in the Hayford design (3 columns desktop, 2 tablet, 1 mobile).
 * Version:           1.0.0
 * Requires at least: 6.0
 * Requires PHP:      7.4
 * Author:            Reach Right
 * License:           GPL-2.0-or-later
 * Text Domain:       hayford-event-cards
 *
 * Usage:
 *   [hf_event_cards]                                   6 upcoming events, 3 columns
 *   [hf_event_cards count="3"]                         only the next 3
 *   [hf_event_cards category="worship,students"]       mec_category slugs, names or ids
 *   [hf_event_cards columns="2" excerpt="0"]           2 columns, no excerpt
 *   [hf_event_cards group="no"]                        every occurrence (repeating events can fill several cards)
 *
 * Dates come from MEC's own occurrence table ({prefix}mec_dates), so events are ordered by their NEXT occurrence and a
 * repeating event (e.g. Sunday Service) shows once, with its next date and an "Every Sunday" label.
 * Colours / fonts / radii use the site's global tokens (var(--hf-…) from Theme Options › CSS), with fallbacks.
 */

defined( 'ABSPATH' ) || exit;

define( 'HF_EC_VERSION', '1.0.0' );
define( 'HF_EC_FILE', __FILE__ );

add_action( 'init', 'hf_ec_init' );
add_action( 'wp_enqueue_scripts', 'hf_ec_assets' );

function hf_ec_init() {
	add_shortcode( 'hf_event_cards', 'hf_ec_shortcode' );
}

/** Register the stylesheet; enqueue it in <head> when the current page's content contains the shortcode. */
function hf_ec_assets() {
	wp_register_style( 'hf-event-cards', plugins_url( 'assets/event-cards.css', HF_EC_FILE ), array(), HF_EC_VERSION );
	$post = is_singular() ? get_post() : null;
	if ( $post && has_shortcode( (string) $post->post_content, 'hf_event_cards' ) ) {
		wp_enqueue_style( 'hf-event-cards' );
	}
}

/* ------------------------------------------------------------------ shortcode */

function hf_ec_shortcode( $atts ) {
	$a = shortcode_atts(
		array(
			'count'    => 6,
			'category' => '',
			'columns'  => 3,
			'excerpt'  => 22,     // words; 0 hides the excerpt
			'group'    => 'yes',  // one card per event (next occurrence); "no" = every occurrence
			'image'    => 'yes',
			'heading'  => 'h3',
			'empty'    => __( 'There are no upcoming events right now — check back soon.', 'hayford-event-cards' ),
			'class'    => '',
		),
		$atts,
		'hf_event_cards'
	);

	$a['count']   = max( 1, min( 24, (int) $a['count'] ) );
	$a['columns'] = max( 1, min( 4, (int) $a['columns'] ) );
	$a['excerpt'] = max( 0, (int) $a['excerpt'] );
	$a['group']   = ! in_array( strtolower( (string) $a['group'] ), array( 'no', '0', 'false' ), true );
	$a['image']   = ! in_array( strtolower( (string) $a['image'] ), array( 'no', '0', 'false' ), true );
	$a['heading'] = in_array( $a['heading'], array( 'h2', 'h3', 'h4' ), true ) ? $a['heading'] : 'h3';

	$events = array();
	foreach ( hf_ec_upcoming( $a ) as $row ) {
		$e = hf_ec_event( (int) $row['post_id'], (int) $row['tstart'], (int) $row['tend'], $a );
		if ( $e ) {
			$events[] = $e;
		}
	}

	// Print the stylesheet right here if the page did not load it in <head> (e.g. shortcode inside a Global Block).
	$css = '';
	if ( ! wp_style_is( 'hf-event-cards', 'done' ) && ! wp_style_is( 'hf-event-cards', 'enqueued' ) ) {
		if ( ! wp_style_is( 'hf-event-cards', 'registered' ) ) {
			wp_register_style( 'hf-event-cards', plugins_url( 'assets/event-cards.css', HF_EC_FILE ), array(), HF_EC_VERSION );
		}
		ob_start();
		wp_print_styles( 'hf-event-cards' );
		$css = ob_get_clean();
	}

	return $css . hf_ec_render( $events, $a );
}

/* ------------------------------------------------------------------ data */

/**
 * Upcoming occurrences: rows of post_id / tstart / tend (MEC stores local wall-clock times as timestamps).
 * Uses MEC's occurrence table; falls back to the mec_start_date meta if that table is missing.
 */
function hf_ec_upcoming( array $a ) {
	global $wpdb;

	$ids = null;
	if ( '' !== trim( (string) $a['category'] ) ) {
		$ids = hf_ec_category_post_ids( $a['category'] );
		if ( ! $ids ) {
			return array();
		}
	}

	$now   = (int) current_time( 'timestamp' ); // phpcs:ignore WordPress.DateTime.CurrentTimeTimestamp.Requested -- MEC compares local wall-clock timestamps
	$table = $wpdb->prefix . 'mec_dates';

	if ( hf_ec_has_table( $table ) ) {
		$where  = "p.post_type = 'mec-events' AND p.post_status = 'publish' AND d.tend >= %d";
		$params = array( $now );
		if ( hf_ec_has_column( $table, 'public' ) ) {
			$where .= ' AND d.public = 1';
		}
		if ( null !== $ids ) {
			$where .= ' AND d.post_id IN (' . implode( ',', array_fill( 0, count( $ids ), '%d' ) ) . ')';
			$params = array_merge( $params, $ids );
		}
		$params[] = (int) $a['count'];
		if ( $a['group'] ) {
			// Occurrences of one event never overlap, so the earliest future start and end belong to the same occurrence.
			$sql = "SELECT d.post_id, MIN(d.tstart) AS tstart, MIN(d.tend) AS tend FROM {$table} d
			        INNER JOIN {$wpdb->posts} p ON p.ID = d.post_id WHERE {$where}
			        GROUP BY d.post_id ORDER BY tstart ASC, d.post_id ASC LIMIT %d";
		} else {
			$sql = "SELECT d.post_id, d.tstart, d.tend FROM {$table} d
			        INNER JOIN {$wpdb->posts} p ON p.ID = d.post_id WHERE {$where}
			        ORDER BY d.tstart ASC, d.post_id ASC LIMIT %d";
		}
		return (array) $wpdb->get_results( $wpdb->prepare( $sql, $params ), ARRAY_A ); // phpcs:ignore WordPress.DB.PreparedSQL.InterpolatedNotPrepared
	}

	// Fallback: first occurrence only (no repeat expansion).
	$q    = array(
		'post_type'      => 'mec-events',
		'post_status'    => 'publish',
		'posts_per_page' => (int) $a['count'],
		'fields'         => 'ids',
		'meta_key'       => 'mec_start_date', // phpcs:ignore WordPress.DB.SlowDBQuery
		'orderby'        => 'meta_value',
		'order'          => 'ASC',
		'meta_query'     => array( array( 'key' => 'mec_start_date', 'value' => wp_date( 'Y-m-d' ), 'compare' => '>=', 'type' => 'DATE' ) ), // phpcs:ignore WordPress.DB.SlowDBQuery
	);
	if ( null !== $ids ) {
		$q['post__in'] = $ids;
	}
	$rows = array();
	foreach ( get_posts( $q ) as $id ) {
		$sd    = (string) get_post_meta( $id, 'mec_start_date', true );
		$ed    = (string) get_post_meta( $id, 'mec_end_date', true );
		$st    = (int) get_post_meta( $id, 'mec_start_day_seconds', true );
		$et    = (int) get_post_meta( $id, 'mec_end_day_seconds', true );
		$start = strtotime( $sd . ' UTC' ) + $st;
		$rows[] = array( 'post_id' => $id, 'tstart' => $start, 'tend' => $ed ? strtotime( $ed . ' UTC' ) + $et : $start );
	}
	return $rows;
}

function hf_ec_category_post_ids( $list ) {
	$terms = array();
	foreach ( array_filter( array_map( 'trim', explode( ',', (string) $list ) ) ) as $t ) {
		$term = is_numeric( $t ) ? get_term( (int) $t, 'mec_category' ) : get_term_by( 'slug', sanitize_title( $t ), 'mec_category' );
		if ( ! $term || is_wp_error( $term ) ) {
			$term = get_term_by( 'name', $t, 'mec_category' );
		}
		if ( $term && ! is_wp_error( $term ) ) {
			$terms[] = (int) $term->term_id;
		}
	}
	if ( ! $terms ) {
		return array();
	}
	return array_map(
		'intval',
		get_posts(
			array(
				'post_type'      => 'mec-events',
				'post_status'    => 'publish',
				'posts_per_page' => -1,
				'fields'         => 'ids',
				'tax_query'      => array( array( 'taxonomy' => 'mec_category', 'terms' => $terms ) ), // phpcs:ignore WordPress.DB.SlowDBQuery
			)
		)
	);
}

function hf_ec_has_table( $table ) {
	global $wpdb;
	static $cache = array();
	if ( ! isset( $cache[ $table ] ) ) {
		$cache[ $table ] = ( $wpdb->get_var( $wpdb->prepare( 'SHOW TABLES LIKE %s', $wpdb->esc_like( $table ) ) ) === $table );
	}
	return $cache[ $table ];
}

function hf_ec_has_column( $table, $column ) {
	global $wpdb;
	static $cache = array();
	$k = $table . '.' . $column;
	if ( ! isset( $cache[ $k ] ) ) {
		$cache[ $k ] = (bool) $wpdb->get_var( $wpdb->prepare( "SHOW COLUMNS FROM {$table} LIKE %s", $column ) ); // phpcs:ignore WordPress.DB.PreparedSQL.InterpolatedNotPrepared
	}
	return $cache[ $k ];
}

/** One event occurrence → plain array for the template. */
function hf_ec_event( $id, $tstart, $tend, array $a ) {
	$post = get_post( $id );
	if ( ! $post ) {
		return null;
	}

	$repeat = '';
	if ( get_post_meta( $id, 'mec_repeat_status', true ) ) {
		$repeat = hf_ec_repeat_label( (string) get_post_meta( $id, 'mec_repeat_type', true ), (int) get_post_meta( $id, 'mec_repeat_interval', true ), $tstart );
	}

	$url = get_permalink( $id );
	if ( $repeat ) {
		$url = add_query_arg( 'occurrence', gmdate( 'Y-m-d', $tstart ), $url ); // MEC shows this occurrence's date on the single page
	}

	$image = null;
	$thumb = $a['image'] ? get_post_thumbnail_id( $id ) : 0;
	if ( $thumb ) {
		$src = wp_get_attachment_image_src( $thumb, 'medium_large' );
		if ( $src ) {
			$image = array(
				'src'    => $src[0],
				'width'  => (int) $src[1],
				'height' => (int) $src[2],
				'srcset' => (string) wp_get_attachment_image_srcset( $thumb, 'medium_large' ),
				'alt'    => (string) get_post_meta( $thumb, '_wp_attachment_image_alt', true ),
			);
		}
	}

	$category = '';
	$cats     = get_the_terms( $id, 'mec_category' );
	if ( $cats && ! is_wp_error( $cats ) ) {
		$category = $cats[0]->name;
	}

	$location = '';
	$loc_id   = (int) get_post_meta( $id, 'mec_location_id', true );
	if ( $loc_id > 1 ) { // MEC uses 1 for "no location"
		$loc = get_term( $loc_id, 'mec_location' );
		if ( $loc && ! is_wp_error( $loc ) ) {
			$location = $loc->name;
		}
	}

	$excerpt = '';
	if ( $a['excerpt'] ) {
		$raw     = has_excerpt( $id ) ? $post->post_excerpt : strip_shortcodes( $post->post_content );
		$excerpt = wp_trim_words( wp_strip_all_tags( $raw ), $a['excerpt'], '…' );
	}

	return hf_ec_format(
		array(
			'id'        => $id,
			'title'     => get_the_title( $id ),
			'url'       => $url,
			'image'     => $image,
			'start'     => $tstart,
			'end'       => $tend,
			'allday'    => (bool) get_post_meta( $id, 'mec_allday', true ),
			'hide_time' => (bool) get_post_meta( $id, 'mec_hide_time', true ),
			'hide_end'  => (bool) get_post_meta( $id, 'mec_hide_end_time', true ),
			'category'  => $category,
			'location'  => $location,
			'excerpt'   => $excerpt,
			'repeat'    => $repeat,
		)
	);
}

function hf_ec_repeat_label( $type, $interval, $tstart ) {
	$day = date_i18n( 'l', $tstart );
	switch ( $type ) {
		case 'daily':
			return $interval > 1 ? sprintf( __( 'Every %d days', 'hayford-event-cards' ), $interval ) : __( 'Every day', 'hayford-event-cards' );
		case 'weekly':
			/* translators: %s: weekday */
			return 14 === $interval ? sprintf( __( 'Every other %s', 'hayford-event-cards' ), $day ) : sprintf( __( 'Every %s', 'hayford-event-cards' ), $day );
		case 'weekday':
			return __( 'Weekdays', 'hayford-event-cards' );
		case 'weekend':
			return __( 'Weekends', 'hayford-event-cards' );
		case 'certain_weekdays':
			return __( 'Weekly', 'hayford-event-cards' );
		case 'monthly':
			return __( 'Monthly', 'hayford-event-cards' );
		case 'yearly':
			return __( 'Yearly', 'hayford-event-cards' );
		default:
			return __( 'Repeats', 'hayford-event-cards' );
	}
}

/** Adds the display strings (badge month/day, date + time line, ISO datetime). Times are local wall-clock timestamps. */
function hf_ec_format( array $e ) {
	$tf       = get_option( 'time_format' ) ? get_option( 'time_format' ) : 'g:i a';
	$same_day = gmdate( 'Ymd', $e['start'] ) === gmdate( 'Ymd', $e['end'] );

	$e['month'] = date_i18n( 'M', $e['start'] );
	$e['day']   = date_i18n( 'j', $e['start'] );
	$e['iso']   = gmdate( 'Y-m-d\TH:i', $e['start'] );

	$date = date_i18n( 'D, M j', $e['start'] );
	if ( ! $same_day ) {
		$date .= ' – ' . date_i18n( 'D, M j', $e['end'] );
	}
	if ( $e['allday'] ) {
		$time = __( 'All day', 'hayford-event-cards' );
	} elseif ( $e['hide_time'] ) {
		$time = '';
	} else {
		$time = date_i18n( $tf, $e['start'] );
		if ( ! $e['hide_end'] && $same_day && $e['end'] > $e['start'] ) {
			$time .= ' – ' . date_i18n( $tf, $e['end'] );
		}
	}
	$e['when'] = $time ? $date . ' · ' . $time : $date;
	return $e;
}

/* ------------------------------------------------------------------ template */

function hf_ec_icon( $name ) {
	$paths = array(
		'clock'  => '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
		'pin'    => '<path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
		'repeat' => '<path d="M17 2l3 3-3 3"/><path d="M4 11V9a4 4 0 0 1 4-4h12"/><path d="M7 22l-3-3 3-3"/><path d="M20 13v2a4 4 0 0 1-4 4H4"/>',
		'arrow'  => '<path d="M5 12h14"/><path d="M13 6l6 6-6 6"/>',
	);
	return '<svg class="hf-ec-icon" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">' . $paths[ $name ] . '</svg>';
}

function hf_ec_render( array $events, array $a ) {
	$class = trim( 'hf-ec ' . preg_replace( '/[^A-Za-z0-9_ -]/', '', (string) $a['class'] ) );
	$style = '--hf-ec-cols:' . (int) $a['columns'];

	if ( ! $events ) {
		return '<div class="' . esc_attr( $class ) . '" style="' . esc_attr( $style ) . '"><p class="hf-ec-empty">' . esc_html( $a['empty'] ) . '</p></div>';
	}

	$h   = $a['heading'];
	$out = '<div class="' . esc_attr( $class ) . '" style="' . esc_attr( $style ) . '"><ul class="hf-ec-grid" role="list">';
	foreach ( $events as $e ) {
		$out .= '<li class="hf-ec-item"><article class="hf-ec-card' . ( $e['image'] ? '' : ' hf-ec-card--noimg' ) . '">';

		// Date badge: on the photo, or at the top of the card when there is no photo.
		$badge = '<div class="hf-ec-badge" aria-hidden="true"><span class="hf-ec-badge-m">' . esc_html( $e['month'] ) . '</span><span class="hf-ec-badge-d">' . esc_html( $e['day'] ) . '</span></div>';
		if ( $e['image'] ) {
			$img  = $e['image'];
			$out .= '<div class="hf-ec-media"><img src="' . esc_url( $img['src'] ) . '"'
				. ( $img['srcset'] ? ' srcset="' . esc_attr( $img['srcset'] ) . '" sizes="(max-width: 767px) 92vw, (max-width: 978px) 46vw, 400px"' : '' )
				. ' width="' . (int) $img['width'] . '" height="' . (int) $img['height'] . '" alt="' . esc_attr( $img['alt'] ) . '" loading="lazy" decoding="async">'
				. $badge . '</div>';
		}

		$out .= '<div class="hf-ec-body">';
		if ( ! $e['image'] ) {
			$out .= $badge;
		}
		if ( $e['category'] || $e['repeat'] ) {
			$out .= '<div class="hf-ec-top">';
			$out .= $e['category'] ? '<span class="hf-ec-cat">' . esc_html( $e['category'] ) . '</span>' : '';
			$out .= $e['repeat'] ? '<span class="hf-ec-repeat">' . hf_ec_icon( 'repeat' ) . esc_html( $e['repeat'] ) . '</span>' : '';
			$out .= '</div>';
		}
		$out .= '<' . $h . ' class="hf-ec-title"><a href="' . esc_url( $e['url'] ) . '">' . esc_html( $e['title'] ) . '</a></' . $h . '>';
		$out .= '<ul class="hf-ec-meta" role="list">';
		$out .= '<li>' . hf_ec_icon( 'clock' ) . '<time datetime="' . esc_attr( $e['iso'] ) . '">' . esc_html( $e['when'] ) . '</time></li>';
		if ( $e['location'] ) {
			$out .= '<li>' . hf_ec_icon( 'pin' ) . '<span>' . esc_html( $e['location'] ) . '</span></li>';
		}
		$out .= '</ul>';
		if ( $e['excerpt'] ) {
			$out .= '<p class="hf-ec-excerpt">' . esc_html( $e['excerpt'] ) . '</p>';
		}
		$out .= '<div class="hf-ec-foot"><span class="hf-ec-more">' . esc_html__( 'Event details', 'hayford-event-cards' ) . '<span class="hf-ec-chip">' . hf_ec_icon( 'arrow' ) . '</span></span></div>';
		$out .= '</div></article></li>';
	}
	return $out . '</ul></div>';
}
