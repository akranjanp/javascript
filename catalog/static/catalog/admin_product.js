/* Simple conditional UI behavior for WooCommerce-like admin */
(function() {
  function toggleSimpleFields() {
    var typeSelect = document.getElementById('id_product_type');
    if (!typeSelect) return;
    var isSimple = typeSelect.value === 'simple';
    var simpleSections = document.querySelectorAll('.simple-only');
    simpleSections.forEach(function(section) {
      if (isSimple) {
        section.classList.remove('collapsed');
        section.style.display = '';
      } else {
        section.style.display = 'none';
      }
    });
    // Toggle variations inline group
    var varInline = document.getElementById('productvariation_set-group');
    if (varInline) {
      varInline.style.display = isSimple ? 'none' : '';
    }
  }

  function attachLivePreviewToInput(input) {
    if (!input) return;
    input.addEventListener('change', function() {
      var file = input.files && input.files[0];
      if (!file) return;
      var reader = new FileReader();
      reader.onload = function(e) {
        var container = input.closest('div.form-row') || input.parentElement;
        var img = container && container.querySelector('img.inline-live-preview');
        if (!img) {
          img = document.createElement('img');
          img.className = 'inline-live-preview';
          img.style.maxHeight = '120px';
          container && container.appendChild(img);
        }
        img.src = e.target.result;
      };
      reader.readAsDataURL(file);
    });
  }

  function wireUpInlinePreviews(context) {
    var root = context || document;
    // Featured image
    var featured = root.getElementById && root.getElementById('id_featured_image');
    if (featured) attachLivePreviewToInput(featured);
    // Any inline file input whose id ends with '-image'
    var inputs = root.querySelectorAll("input[type='file'][id$='-image']");
    inputs.forEach(attachLivePreviewToInput);
  }

  document.addEventListener('DOMContentLoaded', function() {
    toggleSimpleFields();
    var typeSelect = document.getElementById('id_product_type');
    if (typeSelect) {
      typeSelect.addEventListener('change', toggleSimpleFields);
    }
    wireUpInlinePreviews(document);

    // Handle dynamically added inlines (Django admin adds events on formset)
    document.body.addEventListener('formset:added', function(event) {
      wireUpInlinePreviews(event.target);
    });
  });
})();

