<?php
defined( 'ABSPATH' ) || exit;

/**
 * [youtube_messages] — grid/list of imported messages. Each card opens the video on YouTube.
 */
class YTM_Shortcode {

	private static $instance = 0;

	public static function init() {
		add_shortcode( 'youtube_messages', array( __CLASS__, 'render' ) );
		add_action( 'wp_enqueue_scripts', array( __CLASS__, 'register_assets' ) );
	}

	public static function register_assets() {
		wp_register_style( 'youtube-messages', YTM_URL . 'assets/youtube-messages.css', array(), YTM_VERSION );
	}

	private static function yes( $value ) {
		return in_array( strtolower( (string) $value ), array( '1', 'yes', 'true', 'on' ), true );
	}

	public static function render( $atts ) {
		$a = shortcode_atts( array(
			'per_page'      => 12,
			'columns'       => 3,
			'layout'        => 'grid',
			'featured'      => 'no',
			'filters'       => 'yes',
			'pagination'    => 'yes',
			'series'        => '',
			'type'          => '',
			'show_date'     => 'yes',
			'show_type'     => 'yes',
			'show_series'   => 'no',
			'show_duration' => 'yes',
			'show_excerpt'  => 'no',
			'date_format'   => '',
		), $atts, 'youtube_messages' );

		++self::$instance;
		wp_enqueue_style( 'youtube-messages' );
		wp_add_inline_style( 'youtube-messages', '.ytm{--ytm-accent:' . ( YTM_Settings::get( 'accent_color' ) ?: '#A51C30' ) . '}' );

		// Filter/page values come from the URL. Only the first list on a page reads them unless
		// the others have filters on, so a "latest message" box elsewhere on the page stays put.
		$reads_url = self::yes( $a['filters'] ) || self::yes( $a['pagination'] );
		// phpcs:disable WordPress.Security.NonceVerification.Recommended -- public, read-only filters.
		$search = $reads_url && isset( $_GET['ytm_s'] ) ? sanitize_text_field( wp_unslash( $_GET['ytm_s'] ) ) : '';
		$series = $a['series'] ? sanitize_title( $a['series'] ) : ( $reads_url && isset( $_GET['ytm_series'] ) ? sanitize_title( wp_unslash( $_GET['ytm_series'] ) ) : '' );
		$type   = $a['type'] ? sanitize_title( $a['type'] ) : ( $reads_url && isset( $_GET['ytm_type'] ) ? sanitize_title( wp_unslash( $_GET['ytm_type'] ) ) : '' );
		$paged  = self::yes( $a['pagination'] ) && isset( $_GET['ytm_pg'] ) ? max( 1, absint( $_GET['ytm_pg'] ) ) : 1;
		// phpcs:enable

		$per_page = max( 1, min( 100, (int) $a['per_page'] ) );
		$columns  = max( 1, min( 4, (int) $a['columns'] ) );

		$query_args = array(
			'post_type'      => YTM_Post_Type::POST_TYPE,
			'post_status'    => 'publish',
			'posts_per_page' => $per_page,
			'paged'          => $paged,
			'orderby'        => 'date',
			'order'          => 'DESC',
			'no_found_rows'  => ! self::yes( $a['pagination'] ),
		);
		if ( '' !== $search ) {
			$query_args['s'] = $search;
		}
		$tax = array();
		if ( $series ) {
			$tax[] = array( 'taxonomy' => YTM_Post_Type::SERIES, 'field' => 'slug', 'terms' => $series );
		}
		if ( $type ) {
			$tax[] = array( 'taxonomy' => YTM_Post_Type::TYPE, 'field' => 'slug', 'terms' => $type );
		}
		if ( $tax ) {
			$query_args['tax_query'] = $tax; // phpcs:ignore WordPress.DB.SlowDBQuery
		}
		$q = new WP_Query( $query_args );

		$classes = array( 'ytm', 'ytm--' . ( 'list' === $a['layout'] ? 'list' : 'grid' ), 'ytm--cols-' . $columns );
		ob_start();
		echo '<div class="' . esc_attr( implode( ' ', $classes ) ) . '" id="ytm-' . (int) self::$instance . '">';

		if ( self::yes( $a['filters'] ) ) {
			self::filters( $search, $a['series'] ? '' : $series, $a['type'] ? '' : $type, ! $a['series'], ! $a['type'] );
		}

		if ( $q->have_posts() ) {
			$i = 0;
			echo '<div class="ytm-items">';
			while ( $q->have_posts() ) {
				$q->the_post();
				$featured = self::yes( $a['featured'] ) && 0 === $i && 1 === $paged && '' === $search;
				self::card( get_post(), $a, $featured );
				++$i;
			}
			echo '</div>';
			wp_reset_postdata();
		} else {
			echo '<p class="ytm-empty">' . esc_html( ( $search || $series || $type ) ? __( 'No messages match your search.', 'youtube-messages' ) : __( 'New messages will appear here soon.', 'youtube-messages' ) ) . '</p>';
		}

		if ( self::yes( $a['pagination'] ) && $q->max_num_pages > 1 ) {
			self::pagination( $paged, (int) $q->max_num_pages );
		}

		echo '</div>';
		return ob_get_clean();
	}

	private static function card( WP_Post $post, array $a, $featured ) {
		$video = get_post_meta( $post->ID, '_ytm_video_id', true );
		if ( ! $video ) {
			return;
		}
		$url      = YTM_Post_Type::watch_url( $video );
		$new_tab  = YTM_Settings::get( 'new_tab' );
		$thumb    = YTM_Post_Type::thumbnail_url( $post->ID );
		$duration = self::yes( $a['show_duration'] ) ? YTM_Post_Type::format_duration( get_post_meta( $post->ID, '_ytm_duration', true ) ) : '';
		$live     = 'live' === get_post_meta( $post->ID, '_ytm_live', true );
		$title    = get_the_title( $post );

		$meta = array();
		if ( self::yes( $a['show_date'] ) ) {
			$meta[] = '<time datetime="' . esc_attr( get_the_date( 'c', $post ) ) . '">' . esc_html( get_the_date( $a['date_format'], $post ) ) . '</time>';
		}
		foreach ( array( 'show_type' => YTM_Post_Type::TYPE, 'show_series' => YTM_Post_Type::SERIES ) as $flag => $taxonomy ) {
			if ( self::yes( $a[ $flag ] ) ) {
				$terms = get_the_terms( $post, $taxonomy );
				if ( $terms && ! is_wp_error( $terms ) ) {
					$meta[] = '<span>' . esc_html( implode( ', ', wp_list_pluck( $terms, 'name' ) ) ) . '</span>';
				}
			}
		}
		?>
		<article class="ytm-card<?php echo $featured ? ' ytm-card--featured' : ''; ?>">
			<a class="ytm-card__link" href="<?php echo esc_url( $url ); ?>"<?php echo $new_tab ? ' target="_blank" rel="noopener"' : ''; ?>>
				<span class="ytm-card__media">
					<img src="<?php echo esc_url( $thumb ); ?>" alt="" loading="lazy" decoding="async" width="640" height="360">
					<span class="ytm-card__play" aria-hidden="true"><svg viewBox="0 0 24 24" width="24" height="24"><path d="M8 5.5v13l11-6.5z" fill="currentColor"/></svg></span>
					<?php if ( $live ) : ?>
						<span class="ytm-card__badge ytm-card__badge--live"><?php esc_html_e( 'Live', 'youtube-messages' ); ?></span>
					<?php elseif ( $duration ) : ?>
						<span class="ytm-card__badge"><?php echo esc_html( $duration ); ?></span>
					<?php endif; ?>
				</span>
				<span class="ytm-card__body">
					<?php if ( $meta ) : ?>
						<span class="ytm-card__meta"><?php echo implode( '<span class="ytm-card__sep" aria-hidden="true">&middot;</span>', $meta ); // phpcs:ignore WordPress.Security.EscapeOutput -- escaped above. ?></span>
					<?php endif; ?>
					<span class="ytm-card__title"><?php echo esc_html( $title ); ?></span>
					<?php if ( self::yes( $a['show_excerpt'] ) && '' !== trim( $post->post_content ) ) : ?>
						<span class="ytm-card__excerpt"><?php echo esc_html( wp_trim_words( wp_strip_all_tags( $post->post_content ), 22 ) ); ?></span>
					<?php endif; ?>
					<span class="ytm-card__cta"><?php esc_html_e( 'Watch on YouTube', 'youtube-messages' ); ?><?php if ( $new_tab ) : ?><span class="screen-reader-text"> <?php esc_html_e( '(opens in a new tab)', 'youtube-messages' ); ?></span><?php endif; ?></span>
				</span>
			</a>
		</article>
		<?php
	}

	private static function filters( $search, $series, $type, $show_series, $show_type ) {
		$action = remove_query_arg( array( 'ytm_s', 'ytm_series', 'ytm_type', 'ytm_pg' ) );
		$id     = 'ytm-' . (int) self::$instance;
		?>
		<form class="ytm-filters" method="get" action="<?php echo esc_url( $action . '#' . $id ); ?>" role="search">
			<?php
			// Keep any other query args (e.g. ?page_id=) when the form submits.
			$query = wp_parse_url( $action, PHP_URL_QUERY );
			if ( $query ) {
				parse_str( $query, $keep );
				foreach ( $keep as $k => $v ) {
					if ( is_scalar( $v ) ) {
						printf( '<input type="hidden" name="%s" value="%s">', esc_attr( $k ), esc_attr( $v ) );
					}
				}
			}
			?>
			<label class="screen-reader-text" for="<?php echo esc_attr( $id ); ?>-s"><?php esc_html_e( 'Search messages', 'youtube-messages' ); ?></label>
			<input class="ytm-filters__search" type="search" id="<?php echo esc_attr( $id ); ?>-s" name="ytm_s" value="<?php echo esc_attr( $search ); ?>" placeholder="<?php esc_attr_e( 'Search messages…', 'youtube-messages' ); ?>">
			<?php
			if ( $show_series ) {
				self::term_select( YTM_Post_Type::SERIES, 'ytm_series', $series, __( 'All series', 'youtube-messages' ), $id );
			}
			if ( $show_type ) {
				self::term_select( YTM_Post_Type::TYPE, 'ytm_type', $type, __( 'All service types', 'youtube-messages' ), $id );
			}
			?>
			<button type="submit" class="ytm-filters__button"><?php esc_html_e( 'Filter', 'youtube-messages' ); ?></button>
			<?php if ( $search || $series || $type ) : ?>
				<a class="ytm-filters__reset" href="<?php echo esc_url( $action . '#' . $id ); ?>"><?php esc_html_e( 'Clear', 'youtube-messages' ); ?></a>
			<?php endif; ?>
		</form>
		<?php
	}

	private static function term_select( $taxonomy, $name, $current, $all_label, $id ) {
		$terms = get_terms( array( 'taxonomy' => $taxonomy, 'hide_empty' => true ) );
		if ( is_wp_error( $terms ) || ! $terms ) {
			return;
		}
		printf( '<label class="screen-reader-text" for="%1$s-%2$s">%3$s</label><select class="ytm-filters__select" id="%1$s-%2$s" name="%2$s" onchange="this.form.submit()">', esc_attr( $id ), esc_attr( $name ), esc_html( $all_label ) );
		printf( '<option value="">%s</option>', esc_html( $all_label ) );
		foreach ( $terms as $term ) {
			printf( '<option value="%s" %s>%s</option>', esc_attr( $term->slug ), selected( $current, $term->slug, false ), esc_html( $term->name ) );
		}
		echo '</select>';
	}

	private static function pagination( $paged, $max ) {
		$id    = 'ytm-' . (int) self::$instance;
		$links = paginate_links( array(
			'base'      => esc_url_raw( add_query_arg( 'ytm_pg', '%#%' ) ) . '#' . $id,
			'format'    => '',
			'current'   => $paged,
			'total'     => $max,
			'mid_size'  => 1,
			'prev_text' => '&larr; ' . __( 'Newer', 'youtube-messages' ),
			'next_text' => __( 'Older', 'youtube-messages' ) . ' &rarr;',
			'type'      => 'plain',
		) );
		if ( $links ) {
			echo '<nav class="ytm-pagination" aria-label="' . esc_attr__( 'Messages pages', 'youtube-messages' ) . '">' . $links . '</nav>'; // phpcs:ignore WordPress.Security.EscapeOutput
		}
	}
}
