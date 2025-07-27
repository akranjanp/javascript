<?php
/**
 * Optional Installation Helper Script
 * 
 * This script helps create the necessary pages and setup for the child theme.
 * Run this once after theme activation.
 */

// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

/**
 * Create necessary pages and setup
 */
function shoptimizer_child_setup_on_activation() {
    // Create Wishlist page if it doesn't exist
    $wishlist_page = get_page_by_title('Wishlist');
    if (!$wishlist_page) {
        $wishlist_page_id = wp_insert_post(array(
            'post_title' => 'Wishlist',
            'post_content' => '[shoptimizer_wishlist]',
            'post_status' => 'publish',
            'post_type' => 'page',
            'post_slug' => 'wishlist'
        ));
        
        if ($wishlist_page_id) {
            update_option('shoptimizer_child_wishlist_page_id', $wishlist_page_id);
        }
    }
    
    // Set default WooCommerce settings for better display
    update_option('woocommerce_shop_page_display', 'products');
    update_option('woocommerce_category_archive_display', 'products');
    update_option('woocommerce_default_catalog_orderby', 'menu_order');
    
    // Set product image sizes
    update_option('woocommerce_thumbnail_image_width', 300);
    update_option('woocommerce_thumbnail_image_height', 300);
    update_option('woocommerce_thumbnail_cropping', '1:1');
    
    // Flush rewrite rules
    flush_rewrite_rules();
}

/**
 * Run setup when theme is activated
 */
add_action('after_switch_theme', 'shoptimizer_child_setup_on_activation');

/**
 * Add admin notice with setup instructions
 */
function shoptimizer_child_admin_notice() {
    if (get_option('shoptimizer_child_setup_complete')) {
        return;
    }
    
    $class = 'notice notice-info is-dismissible';
    $message = __('Shoptimizer Child Theme activated! Your product archive pages now use the new design. <a href="' . admin_url('admin.php?page=shoptimizer-child-setup') . '">Complete setup</a>', 'shoptimizer-child');
    
    printf('<div class="%1$s"><p>%2$s</p></div>', esc_attr($class), $message);
}
add_action('admin_notices', 'shoptimizer_child_admin_notice');

/**
 * Add admin menu for theme setup
 */
function shoptimizer_child_admin_menu() {
    add_theme_page(
        'Shoptimizer Child Setup',
        'Theme Setup',
        'manage_options',
        'shoptimizer-child-setup',
        'shoptimizer_child_setup_page'
    );
}
add_action('admin_menu', 'shoptimizer_child_admin_menu');

/**
 * Setup page content
 */
function shoptimizer_child_setup_page() {
    if (isset($_POST['complete_setup'])) {
        shoptimizer_child_setup_on_activation();
        update_option('shoptimizer_child_setup_complete', true);
        echo '<div class="notice notice-success"><p>Setup completed successfully!</p></div>';
    }
    
    ?>
    <div class="wrap">
        <h1>Shoptimizer Child Theme Setup</h1>
        
        <div class="card">
            <h2>Welcome to Your New Product Archive Design!</h2>
            <p>Your theme has been activated with the following features:</p>
            
            <ul>
                <li>✅ Modern card-based product layout</li>
                <li>✅ Wishlist functionality</li>
                <li>✅ Responsive design</li>
                <li>✅ Enhanced animations</li>
            </ul>
            
            <h3>Next Steps:</h3>
            <ol>
                <li><strong>Check your shop page:</strong> <a href="<?php echo get_permalink(wc_get_page_id('shop')); ?>" target="_blank">View Shop</a></li>
                <li><strong>Customize colors:</strong> Edit style.css to match your brand</li>
                <li><strong>Add products:</strong> Make sure you have products with images and descriptions</li>
                <li><strong>Test wishlist:</strong> Create an account and test the heart icon functionality</li>
            </ol>
            
            <form method="post">
                <p>
                    <?php wp_nonce_field('shoptimizer_child_setup'); ?>
                    <input type="submit" name="complete_setup" class="button button-primary" value="Complete Setup">
                </p>
            </form>
        </div>
        
        <div class="card">
            <h3>Customization Options</h3>
            <p>You can customize your theme by:</p>
            
            <ul>
                <li><strong>Colors:</strong> Edit the CSS variables in style.css</li>
                <li><strong>Layout:</strong> Change grid columns in functions.php</li>
                <li><strong>Content:</strong> Modify product descriptions and titles</li>
                <li><strong>Features:</strong> Add or remove functionality in functions.php</li>
            </ul>
            
            <p><strong>Need help?</strong> Check the README.md file for detailed instructions.</p>
        </div>
        
        <div class="card">
            <h3>Current Status</h3>
            <table class="widefat">
                <tr>
                    <td><strong>WooCommerce Active:</strong></td>
                    <td><?php echo class_exists('WooCommerce') ? '✅ Yes' : '❌ Not installed'; ?></td>
                </tr>
                <tr>
                    <td><strong>Parent Theme:</strong></td>
                    <td><?php echo get_template() === 'shoptimizer' ? '✅ Shoptimizer' : '⚠️ ' . get_template(); ?></td>
                </tr>
                <tr>
                    <td><strong>Wishlist Page:</strong></td>
                    <td><?php echo get_page_by_title('Wishlist') ? '✅ Created' : '⚠️ Not created'; ?></td>
                </tr>
                <tr>
                    <td><strong>Products Count:</strong></td>
                    <td><?php echo wp_count_posts('product')->publish; ?> products</td>
                </tr>
            </table>
        </div>
    </div>
    <?php
}

/**
 * Dismiss setup notice
 */
function shoptimizer_child_dismiss_notice() {
    if (isset($_GET['dismiss_notice'])) {
        update_option('shoptimizer_child_setup_complete', true);
    }
}
add_action('admin_init', 'shoptimizer_child_dismiss_notice');