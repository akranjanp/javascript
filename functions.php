<?php
/**
 * Shoptimizer Child Theme Functions
 */

// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

/**
 * Enqueue child theme styles
 */
function shoptimizer_child_enqueue_styles() {
    wp_enqueue_style('shoptimizer-parent-style', get_template_directory_uri() . '/style.css');
    wp_enqueue_style('shoptimizer-child-style', get_stylesheet_directory_uri() . '/style.css', array('shoptimizer-parent-style'), wp_get_theme()->get('Version'));
    
    // Enqueue custom JavaScript
    wp_enqueue_script('shoptimizer-child-custom', get_stylesheet_directory_uri() . '/assets/js/custom.js', array('jquery'), '1.0.0', true);
    
    // Localize script for AJAX
    wp_localize_script('shoptimizer-child-custom', 'shoptimizer_ajax', array(
        'ajax_url' => admin_url('admin-ajax.php'),
        'nonce' => wp_create_nonce('shoptimizer_nonce')
    ));
}
add_action('wp_enqueue_scripts', 'shoptimizer_child_enqueue_styles');

/**
 * Override WooCommerce product loop template
 */
function shoptimizer_child_woocommerce_product_loop_start() {
    echo '<ul class="products columns-' . esc_attr(wc_get_loop_prop('columns')) . '">';
}

function shoptimizer_child_woocommerce_product_loop_end() {
    echo '</ul>';
}

// Remove default WooCommerce loop hooks
remove_action('woocommerce_shop_loop_item_title', 'woocommerce_template_loop_product_title', 10);
remove_action('woocommerce_after_shop_loop_item_title', 'woocommerce_template_loop_rating', 5);
remove_action('woocommerce_after_shop_loop_item_title', 'woocommerce_template_loop_price', 10);
remove_action('woocommerce_after_shop_loop_item', 'woocommerce_template_loop_add_to_cart', 10);

// Add custom product loop content
add_action('woocommerce_before_shop_loop_item', 'shoptimizer_child_product_wrapper_start', 5);
add_action('woocommerce_before_shop_loop_item_title', 'shoptimizer_child_product_image_wrapper_start', 5);
add_action('woocommerce_before_shop_loop_item_title', 'shoptimizer_child_add_wishlist_icon', 15);
add_action('woocommerce_before_shop_loop_item_title', 'shoptimizer_child_product_image_wrapper_end', 25);
add_action('woocommerce_before_shop_loop_item_title', 'shoptimizer_child_product_details_start', 30);
add_action('woocommerce_shop_loop_item_title', 'shoptimizer_child_product_title', 10);
add_action('woocommerce_after_shop_loop_item_title', 'shoptimizer_child_product_description', 5);
add_action('woocommerce_after_shop_loop_item_title', 'woocommerce_template_loop_price', 10);
add_action('woocommerce_after_shop_loop_item', 'shoptimizer_child_add_to_cart_button', 10);
add_action('woocommerce_after_shop_loop_item', 'shoptimizer_child_product_details_end', 15);
add_action('woocommerce_after_shop_loop_item', 'shoptimizer_child_product_wrapper_end', 25);

/**
 * Custom product loop functions
 */
function shoptimizer_child_product_wrapper_start() {
    echo '<div class="product-card">';
}

function shoptimizer_child_product_wrapper_end() {
    echo '</div>';
}

function shoptimizer_child_product_image_wrapper_start() {
    echo '<div class="product-image-wrapper">';
}

function shoptimizer_child_product_image_wrapper_end() {
    echo '</div>';
}

function shoptimizer_child_product_details_start() {
    echo '<div class="product-details">';
}

function shoptimizer_child_product_details_end() {
    echo '</div>';
}

function shoptimizer_child_add_wishlist_icon() {
    global $product;
    $product_id = $product->get_id();
    
    echo '<button class="wishlist-icon" data-product-id="' . esc_attr($product_id) . '" title="' . esc_attr__('Add to Wishlist', 'shoptimizer-child') . '">';
    echo '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">';
    echo '<path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>';
    echo '</svg>';
    echo '</button>';
}

function shoptimizer_child_product_title() {
    global $product;
    echo '<h2 class="woocommerce-loop-product__title"><a href="' . esc_url(get_permalink()) . '">' . esc_html(get_the_title()) . '</a></h2>';
}

function shoptimizer_child_product_description() {
    global $product;
    
    // Get product short description or excerpt
    $short_description = $product->get_short_description();
    if (empty($short_description)) {
        $short_description = wp_trim_words(get_the_excerpt(), 15, '...');
    }
    
    if (!empty($short_description)) {
        echo '<div class="product-description">' . wp_kses_post($short_description) . '</div>';
    }
}

function shoptimizer_child_add_to_cart_button() {
    global $product;
    
    if (!$product->is_purchasable() || !$product->is_in_stock()) {
        return;
    }
    
    $button_text = $product->is_type('simple') ? esc_html__('Сагсанд хийх', 'shoptimizer-child') : esc_html__('Сонгох', 'shoptimizer-child');
    
    echo sprintf(
        '<a href="%s" data-quantity="1" class="%s" data-product_id="%s" data-product_sku="%s" rel="nofollow">%s</a>',
        esc_url($product->add_to_cart_url()),
        esc_attr(implode(' ', array_filter(array(
            'button',
            'product_type_' . $product->get_type(),
            $product->is_purchasable() && $product->is_in_stock() ? 'add_to_cart_button' : '',
            $product->supports('ajax_add_to_cart') && $product->is_purchasable() && $product->is_in_stock() ? 'ajax_add_to_cart' : '',
        )))),
        esc_attr($product->get_id()),
        esc_attr($product->get_sku()),
        esc_html($button_text)
    );
}

/**
 * AJAX handler for wishlist functionality
 */
function shoptimizer_child_toggle_wishlist() {
    check_ajax_referer('shoptimizer_nonce', 'nonce');
    
    $product_id = intval($_POST['product_id']);
    $user_id = get_current_user_id();
    
    if (!$user_id) {
        wp_send_json_error('User not logged in');
        return;
    }
    
    $wishlist = get_user_meta($user_id, 'shoptimizer_wishlist', true);
    if (!is_array($wishlist)) {
        $wishlist = array();
    }
    
    $is_in_wishlist = in_array($product_id, $wishlist);
    
    if ($is_in_wishlist) {
        $wishlist = array_diff($wishlist, array($product_id));
        $action = 'removed';
    } else {
        $wishlist[] = $product_id;
        $action = 'added';
    }
    
    update_user_meta($user_id, 'shoptimizer_wishlist', $wishlist);
    
    wp_send_json_success(array(
        'action' => $action,
        'product_id' => $product_id,
        'count' => count($wishlist)
    ));
}
add_action('wp_ajax_toggle_wishlist', 'shoptimizer_child_toggle_wishlist');
add_action('wp_ajax_nopriv_toggle_wishlist', 'shoptimizer_child_toggle_wishlist');

/**
 * Add wishlist page shortcode
 */
function shoptimizer_child_wishlist_shortcode() {
    if (!is_user_logged_in()) {
        return '<p>' . esc_html__('Please log in to view your wishlist.', 'shoptimizer-child') . '</p>';
    }
    
    $user_id = get_current_user_id();
    $wishlist = get_user_meta($user_id, 'shoptimizer_wishlist', true);
    
    if (empty($wishlist) || !is_array($wishlist)) {
        return '<p>' . esc_html__('Your wishlist is empty.', 'shoptimizer-child') . '</p>';
    }
    
    ob_start();
    
    echo '<div class="wishlist-products">';
    echo '<ul class="products">';
    
    foreach ($wishlist as $product_id) {
        $product = wc_get_product($product_id);
        if (!$product) continue;
        
        wc_get_template_part('content', 'product');
    }
    
    echo '</ul>';
    echo '</div>';
    
    return ob_get_clean();
}
add_shortcode('shoptimizer_wishlist', 'shoptimizer_child_wishlist_shortcode');

/**
 * Customize WooCommerce columns
 */
function shoptimizer_child_loop_columns() {
    return 4; // Number of columns
}
add_filter('loop_shop_columns', 'shoptimizer_child_loop_columns', 999);

/**
 * Add body class for archive pages
 */
function shoptimizer_child_body_classes($classes) {
    if (is_shop() || is_product_category() || is_product_tag()) {
        $classes[] = 'shoptimizer-child-archive';
    }
    return $classes;
}
add_filter('body_class', 'shoptimizer_child_body_classes');

/**
 * Include installation helper
 */
require_once get_stylesheet_directory() . '/install.php';