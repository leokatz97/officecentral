var productMediaModel = {
    loadShopifyXR() {
      Shopify.loadFeatures([
        {
          name: 'shopify-xr',
          version: '1.0',
          onLoad: this.setupShopifyXR.bind(this),
        },
        {
          name: 'model-viewer-ui',
          version: '1.0',
          onLoad: (function(){            
            document.querySelectorAll('.sr-product-model-item').forEach((model) => {   
              let model3D = model.querySelector('model-viewer');
              model.modelViewerUI = new Shopify.ModelViewerUI(model3D);
              model3D.addEventListener('shopify_model_viewer_ui_toggle_play', function(evt) {
                model.querySelectorAll('.close-product-model').forEach(el => {
                  el.classList.remove('hidden');
                });
                let productdataMedia = model.closest('[data-slideshow]');
                if(productdataMedia){
                  let productMediaSlider = Flickity.data(productdataMedia);
                  if(productMediaSlider){
                    productMediaSlider.options.draggable = false;
                    productMediaSlider.updateDraggable();
                  }
                }
              }.bind(this));
  
              model3D.addEventListener('shopify_model_viewer_ui_toggle_pause', function(evt) {
                model.querySelectorAll('.close-product-model').forEach(el => {
                  el.classList.add('hidden');
                });
                let productdataMedia = model.closest('[data-slideshow]');
                if(productdataMedia){
                  let productMediaSlider = Flickity.data(productdataMedia);
                  if(productMediaSlider){
                    productMediaSlider.options.draggable = true;
                    productMediaSlider.updateDraggable();
                  }
                } 
              }.bind(this));
              
              model.querySelectorAll('.close-product-model').forEach(el => {
                el.addEventListener('click', function() {
                  if (model3D) {
                    model.modelViewerUI.pause();
                  }
                }.bind(this))
              });
              
            });
  
          })
        }
      ]);
    },
  
    setupShopifyXR(errors) {
      if (!errors) {
        if (!window.ShopifyXR) {
          document.addEventListener('shopify_xr_initialized', () =>
            this.setupShopifyXR()
          );
          return;
        }
        document.querySelectorAll('[id^="product3DModel-"]').forEach((model) => {
          window.ShopifyXR.addModels(JSON.parse(model.textContent));
        });
        window.ShopifyXR.setupXRElements();
      }
    },
  };
  
  window.addEventListener('DOMContentLoaded', () => {
    let productModel = document.querySelectorAll('[id^="product3DModel-"]');
    if (productMediaModel && productModel.length > 0 ){
      productMediaModel.loadShopifyXR();
    }

    /*let productTerms = document.querySelectorAll("[data-product-terms]");
    if (productTerms) {
        Array.from(productTerms).forEach(function(productTerm) {
            if(productTerm.checked){
            console.log('checked');
              productTerm.closest("[data-product-wrapper]").querySelector('[name="add"]').removeAttribute("disabled");
            }else {
              console.log('not checked');
              productTerm.closest("[data-product-wrapper]").querySelector('[name="add"]').setAttribute("disabled", true)   
            }
        });
    }*/

  });