jQuery(document).ready(function($) {
    'use strict';
    
    /**
     * Wishlist functionality
     */
    $('.wishlist-icon').on('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        
        var $button = $(this);
        var productId = $button.data('product-id');
        
        // Prevent multiple clicks
        if ($button.hasClass('loading')) {
            return;
        }
        
        $button.addClass('loading');
        
        $.ajax({
            url: shoptimizer_ajax.ajax_url,
            type: 'POST',
            data: {
                action: 'toggle_wishlist',
                product_id: productId,
                nonce: shoptimizer_ajax.nonce
            },
            success: function(response) {
                if (response.success) {
                    if (response.data.action === 'added') {
                        $button.addClass('active');
                        $button.find('svg').addClass('filled');
                        showNotification('Product added to wishlist', 'success');
                    } else {
                        $button.removeClass('active');
                        $button.find('svg').removeClass('filled');
                        showNotification('Product removed from wishlist', 'info');
                    }
                    
                    // Update wishlist counter if exists
                    updateWishlistCounter(response.data.count);
                } else {
                    if (response.data === 'User not logged in') {
                        showNotification('Please log in to add items to wishlist', 'error');
                        // Optionally redirect to login page
                        // window.location.href = '/my-account/';
                    } else {
                        showNotification('Error updating wishlist', 'error');
                    }
                }
            },
            error: function() {
                showNotification('Network error. Please try again.', 'error');
            },
            complete: function() {
                $button.removeClass('loading');
            }
        });
    });
    
    /**
     * Enhanced Add to Cart functionality
     */
    $(document).on('click', '.add_to_cart_button', function(e) {
        var $button = $(this);
        
        // Add loading state
        $button.addClass('loading');
        $button.text('Adding...');
        
        // Reset button after animation
        setTimeout(function() {
            if (!$button.hasClass('added')) {
                $button.removeClass('loading');
                $button.text($button.data('original-text') || 'Add to Cart');
            }
        }, 2000);
    });
    
    /**
     * Product card hover effects
     */
    $('.woocommerce ul.products li.product').hover(
        function() {
            $(this).addClass('hover-effect');
        },
        function() {
            $(this).removeClass('hover-effect');
        }
    );
    
    /**
     * Lazy loading for product images
     */
    if ('IntersectionObserver' in window) {
        var imageObserver = new IntersectionObserver(function(entries, observer) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    var img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        document.querySelectorAll('img[data-src]').forEach(function(img) {
            imageObserver.observe(img);
        });
    }
    
    /**
     * Smooth scroll to top when clicking pagination
     */
    $('.woocommerce-pagination a').on('click', function() {
        $('html, body').animate({
            scrollTop: $('.woocommerce-products-header').offset().top - 100
        }, 500);
    });
    
    /**
     * Product quick view functionality (optional)
     */
    $('.product-quick-view').on('click', function(e) {
        e.preventDefault();
        var productId = $(this).data('product-id');
        openQuickView(productId);
    });
    
    /**
     * Helper Functions
     */
    
    function showNotification(message, type) {
        var notificationClass = 'notification-' + type;
        var $notification = $('<div class="custom-notification ' + notificationClass + '">' + message + '</div>');
        
        $('body').append($notification);
        
        // Animate in
        setTimeout(function() {
            $notification.addClass('show');
        }, 100);
        
        // Remove after 3 seconds
        setTimeout(function() {
            $notification.removeClass('show');
            setTimeout(function() {
                $notification.remove();
            }, 300);
        }, 3000);
    }
    
    function updateWishlistCounter(count) {
        $('.wishlist-counter').text(count);
        if (count > 0) {
            $('.wishlist-counter').show();
        } else {
            $('.wishlist-counter').hide();
        }
    }
    
    function openQuickView(productId) {
        // Quick view modal implementation
        var $modal = $('#quick-view-modal');
        if ($modal.length === 0) {
            $modal = $('<div id="quick-view-modal" class="quick-view-modal"><div class="modal-content"><span class="close">&times;</span><div class="modal-body"></div></div></div>');
            $('body').append($modal);
        }
        
        $.ajax({
            url: shoptimizer_ajax.ajax_url,
            type: 'POST',
            data: {
                action: 'get_quick_view',
                product_id: productId,
                nonce: shoptimizer_ajax.nonce
            },
            success: function(response) {
                if (response.success) {
                    $modal.find('.modal-body').html(response.data.html);
                    $modal.addClass('show');
                }
            }
        });
        
        // Close modal
        $modal.on('click', '.close, .quick-view-modal', function(e) {
            if (e.target === this) {
                $modal.removeClass('show');
            }
        });
    }
    
    /**
     * Product sorting animations
     */
    $('.orderby').on('change', function() {
        $('.woocommerce ul.products').addClass('sorting');
        setTimeout(function() {
            $('.woocommerce ul.products').removeClass('sorting');
        }, 500);
    });
    
    /**
     * Mobile optimization
     */
    function handleMobileLayout() {
        if ($(window).width() < 768) {
            // Mobile specific optimizations
            $('.product-details').each(function() {
                var $details = $(this);
                var $description = $details.find('.product-description');
                if ($description.length && $description.text().length > 50) {
                    $description.text($description.text().substring(0, 50) + '...');
                }
            });
        }
    }
    
    // Initialize mobile layout
    handleMobileLayout();
    $(window).on('resize', handleMobileLayout);
    
    /**
     * Product image zoom on hover (desktop only)
     */
    if ($(window).width() > 768) {
        $('.product-image-wrapper').on('mouseenter', function() {
            $(this).find('img').addClass('zoom-effect');
        }).on('mouseleave', function() {
            $(this).find('img').removeClass('zoom-effect');
        });
    }
    
    /**
     * Infinite scroll (optional)
     */
    if ($('.woocommerce-pagination').length) {
        var page = 2;
        var loading = false;
        
        $(window).scroll(function() {
            if (loading) return;
            
            var scrollTop = $(window).scrollTop();
            var windowHeight = $(window).height();
            var documentHeight = $(document).height();
            
            if (scrollTop + windowHeight >= documentHeight - 1000) {
                loading = true;
                loadMoreProducts(page);
                page++;
            }
        });
    }
    
    function loadMoreProducts(page) {
        var currentUrl = window.location.href;
        var separator = currentUrl.includes('?') ? '&' : '?';
        var loadUrl = currentUrl + separator + 'paged=' + page;
        
        $.get(loadUrl, function(data) {
            var $newProducts = $(data).find('.woocommerce ul.products li.product');
            if ($newProducts.length) {
                $('.woocommerce ul.products').append($newProducts);
                loading = false;
            } else {
                // No more products
                $(window).off('scroll');
            }
        });
    }
});