(function($) {
    function toggleFields() {
        const productType = $('#id_product_type').val();
        const simpleFields = ['.form-row.field-regular_price', '.form-row.field-sale_price', '.form-row.field-sku', '.form-row.field-stock_quantity', '.form-row.field-stock_status'];

        if (productType === 'simple') {
            $(simpleFields.join(',')).show();
        } else {
            $(simpleFields.join(',')).hide();
        }
    }

    $(document).ready(function() {
        toggleFields();
        $('#id_product_type').change(toggleFields);
    });
})(django.jQuery);