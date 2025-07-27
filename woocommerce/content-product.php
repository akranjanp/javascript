<?php
/**
 * The template for displaying product content within loops
 *
 * This template can be overridden by copying it to yourtheme/woocommerce/content-product.php.
 *
 * @see     https://docs.woocommerce.com/document/template-structure/
 * @package WooCommerce\Templates
 * @version 3.6.0
 */

defined( 'ABSPATH' ) || exit;

global $product;

// Ensure visibility.
if ( empty( $product ) || ! $product->is_visible() ) {
	return;
}

// Get wishlist status
$user_id = get_current_user_id();
$wishlist = get_user_meta($user_id, 'shoptimizer_wishlist', true);
$is_in_wishlist = is_array($wishlist) && in_array($product->get_id(), $wishlist);
?>
<li <?php wc_product_class( '', $product ); ?>>
	<div class="product-card">
		<?php
		/**
		 * Hook: woocommerce_before_shop_loop_item.
		 *
		 * @hooked woocommerce_template_loop_product_link_open - 10
		 */
		do_action( 'woocommerce_before_shop_loop_item' );
		?>
		
		<div class="product-image-wrapper">
			<?php
			/**
			 * Hook: woocommerce_before_shop_loop_item_title.
			 *
			 * @hooked woocommerce_show_product_loop_sale_flash - 10
			 * @hooked woocommerce_template_loop_product_thumbnail - 10
			 */
			do_action( 'woocommerce_before_shop_loop_item_title' );
			?>
			
			<!-- Wishlist Icon -->
			<button class="wishlist-icon <?php echo $is_in_wishlist ? 'active' : ''; ?>" 
					data-product-id="<?php echo esc_attr( $product->get_id() ); ?>" 
					title="<?php esc_attr_e( 'Add to Wishlist', 'shoptimizer-child' ); ?>">
				<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" <?php echo $is_in_wishlist ? 'class="filled"' : ''; ?>>
					<path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
				</svg>
			</button>
		</div>
		
		<div class="product-details">
			<?php
			/**
			 * Hook: woocommerce_shop_loop_item_title.
			 *
			 * @hooked woocommerce_template_loop_product_title - 10
			 */
			do_action( 'woocommerce_shop_loop_item_title' );
			?>
			
			<!-- Custom Product Description -->
			<?php
			$short_description = $product->get_short_description();
			if ( empty( $short_description ) ) {
				$short_description = wp_trim_words( get_the_excerpt(), 15, '...' );
			}
			
			if ( ! empty( $short_description ) ) {
				echo '<div class="product-description">' . wp_kses_post( $short_description ) . '</div>';
			}
			?>

			<?php
			/**
			 * Hook: woocommerce_after_shop_loop_item_title.
			 *
			 * @hooked woocommerce_template_loop_rating - 5
			 * @hooked woocommerce_template_loop_price - 10
			 */
			do_action( 'woocommerce_after_shop_loop_item_title' );
			?>

			<?php
			/**
			 * Hook: woocommerce_after_shop_loop_item.
			 *
			 * @hooked woocommerce_template_loop_product_link_close - 5
			 * @hooked woocommerce_template_loop_add_to_cart - 10
			 */
			do_action( 'woocommerce_after_shop_loop_item' );
			?>
		</div>
	</div>
</li>