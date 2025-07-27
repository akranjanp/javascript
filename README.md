# Shoptimizer Child Theme - Custom Product Archive Design

This child theme provides a complete redesign of the WooCommerce product archive page to match your desired design with modern card layouts, wishlist functionality, and enhanced user experience.

## Features

- ✨ Modern card-based product layout
- ❤️ Wishlist functionality with heart icon
- 🛒 Custom "Add to Cart" button styling
- 📱 Fully responsive design
- 🔍 Product image hover effects
- 🎨 Clean, modern UI matching the screenshot
- ⚡ Performance optimized
- 🌐 Multi-language support (includes Mongolian text)

## Installation Instructions

### 1. Upload the Child Theme

1. **Via WordPress Admin (Recommended):**
   - Zip all the files in this folder
   - Go to `Appearance > Themes` in WordPress admin
   - Click "Add New" then "Upload Theme"
   - Upload the zip file and activate

2. **Via FTP:**
   - Upload this entire folder to `/wp-content/themes/`
   - Go to `Appearance > Themes` and activate "Shoptimizer Child"

### 2. Required Plugin Compatibility

This theme works with:
- ✅ WooCommerce (required)
- ✅ Shoptimizer theme (parent theme)
- ✅ Any standard wishlist plugin (optional, has built-in functionality)

### 3. File Structure

```
shoptimizer-child/
├── style.css                 # Main stylesheet
├── functions.php            # Theme functions
├── assets/
│   └── js/
│       └── custom.js       # JavaScript functionality
├── woocommerce/
│   └── content-product.php # Product loop template
└── README.md               # This file
```

## Customization Options

### 1. Colors

Edit `style.css` to change colors:

```css
/* Primary accent color (buttons, wishlist) */
.add_to_cart_button {
    background: #e74c3c !important; /* Change this color */
}

.wishlist-icon:hover svg {
    stroke: #e74c3c; /* Change this color */
}
```

### 2. Grid Layout

Modify the number of columns in `functions.php`:

```php
function shoptimizer_child_loop_columns() {
    return 4; // Change to 3, 4, or 5 columns
}
```

### 3. Card Spacing

Adjust spacing in `style.css`:

```css
.woocommerce ul.products {
    gap: 20px; /* Change gap between cards */
}
```

## Features Breakdown

### Wishlist Functionality

- **Heart Icon**: Appears on product cards
- **AJAX Integration**: No page reload required
- **User Authentication**: Works with logged-in users
- **Visual Feedback**: Heart fills when item is added
- **Shortcode**: Use `[shoptimizer_wishlist]` to display wishlist page

### Product Cards

- **Hover Effects**: Cards lift slightly on hover
- **Image Zoom**: Product images scale on hover
- **Clean Layout**: Title, description, price, and button
- **Sale Badges**: Automatically displays sale labels
- **Out of Stock**: Visual indicators for unavailable products

### JavaScript Features

- **Smooth Animations**: All interactions are animated
- **Mobile Optimized**: Touch-friendly on mobile devices
- **Loading States**: Visual feedback during actions
- **Notifications**: Toast notifications for user actions
- **Infinite Scroll**: Optional infinite loading (commented out)

## Browser Support

- ✅ Chrome (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Edge (latest)
- ✅ Mobile browsers

## Performance

- **CSS Grid**: Modern layout system
- **Optimized Images**: Proper sizing and object-fit
- **Minimal JavaScript**: Only essential functionality
- **Lazy Loading**: Built-in image lazy loading support
- **Caching Friendly**: Works with WordPress caching plugins

## Troubleshooting

### Cards Not Displaying Correctly

1. Clear any caching plugins
2. Check if WooCommerce is active
3. Ensure Shoptimizer parent theme is installed

### Wishlist Not Working

1. Check if users are logged in
2. Verify AJAX is enabled
3. Check browser console for JavaScript errors

### Styling Issues

1. Clear browser cache
2. Check if parent theme styles are loading
3. Verify CSS file permissions

## Customization Services

Need additional customizations? The design can be extended with:

- **Quick View Modals**: Product preview without leaving page
- **Advanced Filtering**: Category and attribute filters
- **Comparison Feature**: Compare multiple products
- **Review Integration**: Display ratings on cards
- **Custom Fields**: Additional product information

## Version History

- **v1.0.0**: Initial release with core functionality
  - Product card layout
  - Wishlist functionality
  - Responsive design
  - Basic animations

## Support

For customization support or issues:

1. Check WordPress debug logs
2. Verify plugin compatibility
3. Test with default WooCommerce theme
4. Contact theme developer

## License

This child theme inherits the license from the parent Shoptimizer theme. Please ensure compliance with all licensing requirements.

---

**Note**: This child theme requires the Shoptimizer parent theme to be installed and WooCommerce to be active. The design matches the provided screenshot with modern e-commerce best practices.