var confettiInterval;
const Confettiful = function (el) {
  this.el = el;
  this.containerEl = null;
  this.confettiFrequency = 3;
  this.confettiColors = ["#fce18a", "#ff726d", "#b48def", "#f4306d"];
  this.confettiAnimations = ["slow", "medium", "fast"];
  this._setupElements();
  this._renderConfetti();
};

Confettiful.prototype._setupElements = function () {
  const containerEl = this.el.querySelector(".confetti-container");
  const elPosition = this.el.style.position;

  if (elPosition !== "relative" || elPosition !== "absolute") {
    this.el.style.position = "absolute";
  }
  this.containerEl = containerEl;
};

Confettiful.prototype._renderConfetti = function () {
  confettiInterval = setInterval(() => {
    const confettiEl = document.createElement("div");
    const confettiSize = Math.floor(Math.random() * 3) + 7 + "px";
    const confettiBackground =
      this.confettiColors[
        Math.floor(Math.random() * this.confettiColors.length)
      ];
    const confettiLeft = Math.floor(Math.random() * this.el.offsetWidth) + "px";
    const confettiAnimation =
      this.confettiAnimations[
        Math.floor(Math.random() * this.confettiAnimations.length)
      ];

    confettiEl.classList.add(
      "confetti",
      "confetti--animation-" + confettiAnimation
    );
    confettiEl.style.left = confettiLeft;
    confettiEl.style.width = confettiSize;
    confettiEl.style.height = confettiSize;
    confettiEl.style.backgroundColor = confettiBackground;

    confettiEl.removeTimeout = setTimeout(function () {
      confettiEl.parentNode.removeChild(confettiEl);
    }, 3000);

    this.containerEl.appendChild(confettiEl);
  }, 25);
};

window.addEventListener("load", (event) => {
  getATCelement();
  getQuantityElement();
  getCartItemRemoveElements();
  cartGiftWrapElement();
});

function getATCelement(section = document) {
  let cartATCElement = section.querySelectorAll("[data-add-to-cart]");
  let cartDrawer = document.querySelector("#ajax-cart-drawer[data-side-drawer]");
  //let cartDrawerbackground = section.querySelector('.drawer_background');
  Array.from(cartATCElement).forEach(function (element) {
    initATC(element, cartDrawer);
  });
}

function initATC(element, cartDrawer) {
  element.addEventListener("click", function (event) {
    event.preventDefault();
    let form = element.closest("form");
    let formParent = element.closest("[data-product-wrapper]");
    if (
      element
        .closest(".shopify-section")
        .querySelector("[data-sticky-products]")
    ) {
      formParent = element.closest(".shopify-section");
    }
    if (element.closest("[data-sticky-products]")) {
      let formId = element.getAttribute("data-form");
      if (formParent.querySelector("#" + formId)) {
        form = formParent.querySelector("#" + formId);
      }
    }
    Array.from(formParent.querySelectorAll("[data-form-error]")).forEach(
      function (errorContainer) {
        errorContainer.classList.add("hidden");
        errorContainer.textContent = "";
      }
    );
    element.setAttribute("disabled", true);
    let giftCardWrapper = formParent.querySelector("[data-gift-card-box]");
    if (giftCardWrapper) {
      let errormessageWrapper = giftCardWrapper.querySelector(
        "[data-gift-card-errors]"
      );
      let errorMessage = errormessageWrapper.querySelector(".error-message");
      errormessageWrapper.classList.add("hidden");
      errorMessage.innerHTML = "";
      // giftCardErrors
    }
    if(element.classList.contains('bundle-product-button')){
      formParent = element.closest("[data-product-bundle-wrapper]");
    }
    addItemtoCart(form, formParent, element, cartDrawer);
  });
}

function addItemtoCart(form, formParent, element, cartDrawer) {
  const config = {
    method: "POST",
    headers: {
      "X-Requested-With": `XMLHttpRequest`,
      Accept: `application/javascript`,
    },
  };
  let sectionId = "ajax-cart-drawer";
  let section = "";
  var baseUrl = window.location.pathname;
  if (baseUrl.indexOf("/cart") > -1) {
    let cartSection = document.querySelector("[data-cart-wrapper]");
    section = cartSection;
    if (cartSection) {
      sectionId = cartSection.dataset.section;
    }
  }
  const formData = new FormData(form);
  formData.append("sections", [sectionId]);
  config.body = formData;
  fetch(cartAddUrl, config)
    .then((response) => {
      return response.text();
    })
    .then((responseText) => {
      const cart = JSON.parse(responseText);
      if (cart.status) {
        if (cart.errors) {
          let giftCardWrapper = formParent.querySelector(
            "[data-gift-card-box]"
          );
          if (giftCardWrapper && cart.errors["email"]) {
            let errormessageWrapper = giftCardWrapper.querySelector(
              "[data-gift-card-errors]"
            );
            let giftCardEmail = formParent.querySelector("[type=email]");
            let errorMessage =
              errormessageWrapper.querySelector(".error-message");
            errorMessage.innerHTML =
              giftCardEmail.dataset.attr + " " + cart.errors["email"];
            errormessageWrapper.classList.remove("hidden");
            //giftCardErrors
          }
        } else {
          Array.from(formParent.querySelectorAll("[data-form-error]")).forEach(
            function (errorContainer) {
              errorContainer.textContent = cart.description;
              errorContainer.classList.remove("hidden");
              // if (!isOnScreen(errorContainer)) {
              //     var scrollDiv = errorContainer.offsetTop;
              //     window.scrollTo({ top: scrollDiv, behavior: 'smooth' });
              // }
            }
          );
        }
        element.removeAttribute("disabled");
        return false;
      }
      if (carType == "page") {
        window.location.href = "/cart";
        return false;
      }
      if (shakeEffect) {
        element.classList.add("shake");
        setTimeout(() => {
          element.classList.remove("shake");
        }, 700);
      }
      if (hapticFeedbackStatus) {
        const canVibrate = window.navigator.vibrate;
        if (canVibrate) window.navigator.vibrate(500);
      }
      if (document.getElementById("cartAlert")) {
        document.getElementById("cartAlert").play();
      }
      if (baseUrl.indexOf("/cart") > -1) {
        let updatedCartHtml = new DOMParser()
          .parseFromString(cart.sections[sectionId], "text/html")
          .querySelector(".shopify-section");
        let updatedCartContent = updatedCartHtml.querySelector(
          "[data-cart-wrapper]"
        );
        let cartCount = parseInt(
          updatedCartContent.getAttribute("data-item-count")
        );
        cartCountUpdate(cartCount);
        // section.innerHTML = updatedCartHtml.innerHTML;
        section.innerHTML = updatedCartContent.innerHTML;
        element.removeAttribute("disabled");
        setTimeout(() => {
          if (cartCount > 0) {
            getQuantityElement(section);
            cartNoteUpdate(section);
            getCartItemRemoveElements(section);
            cartGiftWrapElement(section);
            cartTotalprice(section);
            shippingEstimates();
          }
        }, 500);
        var scrollDiv = section.offsetTop;
        window.scrollTo({ top: scrollDiv, behavior: "smooth" });
      } else {
        let updateCartHtml = new DOMParser()
          .parseFromString(cart.sections[sectionId], "text/html")
          .querySelector(".shopify-section");
        let updateCartContent = updateCartHtml.innerHTML;
        let cartBody = document.querySelector("[data-cart-drwaer-body]");
        let cartItemcount = 0;
        let cartItemtotalprice;
        if (updateCartHtml.querySelector("[data-cart-wrapper]")) {
          cartItemcount = parseInt(
            updateCartHtml
              .querySelector("[data-cart-wrapper]")
              .getAttribute("data-item-count")
          );
          cartItemtotalprice = updateCartHtml
            .querySelector("[data-cart-wrapper]")
            .getAttribute("data-item-total");
        }
        cartBody.innerHTML = updateCartContent;
        if (cartItemcount > 0) {
          getQuantityElement(cartBody);
        }
        cartCountUpdate(cartItemcount);
        cartNoteUpdate();
        // SidedrawerEventInit(cartDrawer);
        getCartItemRemoveElements(cartDrawer);
        cartGiftWrapElement(cartDrawer);
        cartTermhandlerClick();
        cartTermsHandler();

        setTimeout(function () {
          let Cartdrawer = document.querySelector(".cart-drawer");
          let Quickview = document.querySelector(".quickview-drawer");
          let Comparemodel = document.querySelector("[data-compare-model]");
          if (Quickview) {
            Quickview.classList.remove("sidebar-visible");
            setTimeout(function () {
              Quickview.style.display = "none";
            }, 300);
          }
          if(Comparemodel){
            if (Cartdrawer.classList.contains("sidebar-visible") && Comparemodel.querySelector(".compare-modal-content")) {
              Comparemodel.querySelector(
                ".compare-modal-content"
              ).classList.remove("popup-visible");
            }
          }
        }, 100);
        setTimeout(function () {
          if(cartDrawer){
            cartDrawer.classList.add("sidebar-visible");
          }
          setTimeout(function () {
            focusElementsRotation(cartDrawer);
            previousFocusElement = element;
          }, 500);
        }, 500);

        let recommendProducts = cartDrawer.querySelector(
          "[data-recommendation-popup]"
        );
        if (
          recommendProducts &&
          !recommendProducts.classList.contains("active")
        ) {
          setTimeout(() => {
            recommendProducts.classList.add("active");
          }, 1000);
          slideshowElements();
        }
        cartDrawer.style.display = "flex";
        document.querySelector("body").classList.add("no-scroll");
        element.removeAttribute("disabled");
      }
      if(document.querySelector('[data-cart-shipping]') && document.querySelector('[data-cart-shipping]').getAttribute('data-barwidth') == '100%'){
        if(document.querySelector('.confetti-container-wrapper') && (localStorage.confettiEffect == 'false' || localStorage.confettiEffect == undefined )){
          window.confettiful = new Confettiful(document.querySelector('.confetti-container-wrapper'));
          localStorage.confettiEffect = "true";
          setTimeout(function () {
            clearInterval(confettiInterval)
          },3000);
        }
      }
    })
    .catch(function (err) {
      element.removeAttribute("disabled");
    });
}
//Quantity change
function getQuantityElement(section = document) {
  let quantityElements = section.querySelectorAll("[data-quantity-wrapper]");
  Array.from(quantityElements).forEach(function (element) {
    initQuantityAction(element);
  });
}

function initQuantityAction(element) {
  
  let quantityInput = element.querySelector("[data-quantity-input]");
  let stickyQuantityInput;
  if(element.closest('.shopify-section') && element.closest('.shopify-section').querySelector("#sticky_quantity")){
    stickyQuantityInput = element.closest('.shopify-section').querySelector("#sticky_quantity");
  }
  let quantityIncreament = element.querySelector("[data-quantity-increment]");
  let quantityDecreament = element.querySelector("[data-quantity-decrement]");
  if (quantityInput) {
    quantityInput.onkeydown = function (e) {
      if (
        !(
          (e.keyCode > 95 && e.keyCode < 106) ||
          (e.keyCode > 47 && e.keyCode < 58) ||
          e.keyCode == 8 ||
          e.keyCode == 9 ||
          (e.keyCode > 36 && e.keyCode < 41)
        )
      ) {
        return false;
      }
    };
    quantityInput.addEventListener("input", function (event) {
      let currentValue = parseInt(quantityInput.value);
      if(isNaN(currentValue)){
        currentValue = 1;
      }
      if(stickyQuantityInput){
        stickyQuantityInput.value = currentValue;
      }
    });
    if (quantityInput.classList.contains("ajax-cart-update")) {
      quantityInput.addEventListener("change", function (event) {
        let currentValue = parseInt(quantityInput.value);
          let section = quantityInput.closest("[data-cart-wrapper]");
          let cartItem = quantityInput.closest("[data-cart-item]");
          cartItem.classList.add("disabled");
          let line = quantityInput.dataset.line;
          changeCartItem(line, currentValue, section, cartItem);
      });
    }
  }
  quantityIncreamentDecreament(
    quantityIncreament,
    quantityDecreament,
    quantityInput,
    stickyQuantityInput
  );
}

function quantityIncreamentDecreament(
  quantityIncreament,
  quantityDecreament,
  quantityInput,
  stickyQuantityInput
) {
  if (quantityIncreament) {
    
    quantityIncreament.addEventListener("click", function (event) {
      event.preventDefault();
      quantityIncreament;
      let currentValue = parseInt(quantityInput.value);
       
      updatedValue = currentValue + 1;
      if(isNaN(updatedValue)){
        updatedValue = 1;
      }
      quantityInput.value = updatedValue;
      if(stickyQuantityInput){
        stickyQuantityInput.value = updatedValue;
      }
      if (quantityIncreament.classList.contains("ajax-cart-update")) {
        quantityUpdate(quantityInput);
      }
    });
  }
  if (quantityDecreament) {
    quantityDecreament.addEventListener("click", function (event) {
      event.preventDefault();

      let currentValue = parseInt(quantityInput.value);
      updatedValue = currentValue - 1;
      if(isNaN(updatedValue)){
        updatedValue = 1;
      }
      if (updatedValue > 0) {
        quantityInput.value = updatedValue;
        if(stickyQuantityInput){
          stickyQuantityInput.value = updatedValue;
          quantityInput.value = updatedValue;
        }
      }
      if (quantityDecreament.classList.contains("ajax-cart-update")) {
        quantityInput.value = updatedValue;
        quantityUpdate(quantityInput);
      }
    });
  }
}

function getCartItemRemoveElements(section = document) {
  let cartItemRemoveElements = section.querySelectorAll("[data-item-remove]");
  Array.from(cartItemRemoveElements).forEach(function (element) {
    initCartItemRemove(element);
    if (element) {
      cartTotalprice();
    }
  });
}

function cartGiftWrapElement(section = document) {
  let cartGiftWrap = section.querySelector("[data-gift-atc]");
  if (cartGiftWrap) {
    cartGiftWrap.addEventListener("click", (event) => {
      event.preventDefault();
      let formParent = cartGiftWrap.closest("[data-gift-card]");
      let form = formParent.querySelector("form");
      addItemtoCart(form, formParent, cartGiftWrap);
    });
  }
}

function initCartItemRemove(element) {
  element.addEventListener("click", (event) => {
    event.preventDefault();
    let section = element.closest("[data-cart-wrapper]");
    element.closest("[data-cart-item]").classList.add("disabled");
    let line = element.dataset.line;
    changeCartItem(line, 0, section, element.closest("[data-cart-item]"));
  });
}

function quantityUpdate(quantityInput) {
  let section = quantityInput.closest("[data-cart-wrapper]");
  let cartItem = quantityInput.closest("[data-cart-item]");
  cartItem.classList.add("disabled");
  let quantity = parseInt(quantityInput.value);
  let line = quantityInput.dataset.line;
  changeCartItem(line, quantity, section, cartItem);
}

function cartContentUpdate(cart, sectionId) {
  let updatedCartHtml = new DOMParser()
    .parseFromString(cart.sections[sectionId], "text/html")
    .querySelector(".shopify-section");
  let cartBody = document.querySelector("[data-cart-wrapper]");
  if (sectionId == "ajax-cart-drawer") {
    cartBody = document.querySelector("[data-cart-drwaer-body]");
  }
  if (cart.item_count > 0) {
    let cartCount = 0;
    cartCount = parseInt(
      updatedCartHtml
        .querySelector("[data-cart-wrapper]")
        .getAttribute("data-item-count")
    );
    cartCountUpdate(cartCount);
    //let cartTotalprice = cartBody.querySelector('[data-cart-wrapper]').getAttribute('data-item-total');
    //  cartTotalpriceUpdate(cartTotalprice);
    if (
      cartBody.querySelector("[data-cart-form]") &&
      updatedCartHtml.querySelector("[data-cart-form]")
    ) {
      cartBody.querySelector("[data-cart-form]").innerHTML =
        updatedCartHtml.querySelector("[data-cart-form]").innerHTML;
    }
    if (
      document.querySelector("[data-cart-item-count]") &&
      updatedCartHtml.querySelector("[data-cart-item-count]")
    ) {
      document.querySelector("[data-cart-item-count]").innerHTML =
        updatedCartHtml.querySelector("[data-cart-item-count]").innerHTML;
    }
    if (
      document.querySelector("[data-cart-note-wrapper]") &&
      updatedCartHtml.querySelector("[data-cart-note-wrapper]")
    ) {
      document.querySelector("[data-cart-note-wrapper]").innerHTML =
        updatedCartHtml.querySelector("[data-cart-note-wrapper]").innerHTML;
    }
    if (
      cartBody.querySelector("[data-cart-shipping]") &&
      updatedCartHtml.querySelector("[data-cart-shipping]")
    ) {
      // cartBody.querySelector('[data-cart-shipping]').innerHTML =  updatedCartHtml.querySelector('[data-cart-shipping]').innerHTML;
      let delay = 0;
      if (
        !cartBody
          .querySelector("[data-cart-shipping-bar]")
          .classList.contains("active")
      ) {
        cartBody
          .querySelector("[data-cart-shipping-bar]")
          .classList.add("active");
        delay = 150;
      }
      cartBody.querySelector("[data-cart-shipping-text]").textContent = updatedCartHtml.querySelector("[data-cart-shipping-text]").textContent;
      setTimeout(function () {
        cartBody.querySelector("[data-cart-shipping-bar]").style.setProperty( "width",updatedCartHtml.querySelector("[data-cart-shipping]").dataset.barwidth);
        if (cartBody.querySelector("[data-cart-shipping-bar]").style.width == "100%") {
          setTimeout(function () {
            document
              .querySelector("[data-cart-shipping]")
              .classList.add("shipping-full");
            if(document.querySelector('.confetti-container-wrapper') && (localStorage.confettiEffect == 'false' || localStorage.confettiEffect == undefined )){
              window.confettiful = new Confettiful(document.querySelector('.confetti-container-wrapper'));
              localStorage.confettiEffect = "true";
            }
            setTimeout(function () {
              clearInterval(confettiInterval)
            },3000);
          }, 100);
        } else {
          document.querySelector("[data-cart-shipping]").classList.remove("shipping-full");
          localStorage.confettiEffect = "false";
          clearInterval(confettiInterval)
        }
      }, delay);
    }
    if (
      cartBody.querySelector("[data-cart-prices]") &&
      updatedCartHtml.querySelector("[data-cart-prices]")
    ) {
      cartBody.querySelector("[data-cart-prices]").innerHTML =
        updatedCartHtml.querySelector("[data-cart-prices]").innerHTML;
    }
    if (
      cartBody.querySelector("[data-gift-card]") &&
      updatedCartHtml.querySelector("[data-gift-card]")
    ) {
      cartBody.querySelector("[data-gift-card]").innerHTML =
        updatedCartHtml.querySelector("[data-gift-card]").innerHTML;
    }
    if (sectionId != "ajax-cart-drawer") {
      shippingEstimates(cartBody);
    }
    getAllDetails(cartBody);
    getQuantityElement(cartBody);
    cartNoteUpdate(cartBody);
    getCartItemRemoveElements(cartBody);
    SidedrawerEventInit(cartBody);
    cartGiftWrapElement(cartBody);
  } else {
    localStorage.confettiEffect = "false";
    clearInterval(confettiInterval)
    if (sectionId == "ajax-cart-drawer") {
      let updateCartContent = updatedCartHtml.innerHTML;
      let cartBody = document.querySelector("[data-cart-drwaer-body]");
      cartBody.innerHTML = updateCartContent;
      SidedrawerEventInit(cartBody);
    } else {
      cartBody.innerHTML = updatedCartHtml.querySelector(
        "[data-cart-wrapper]"
      ).innerHTML;
    }
    let cartpriceSelector = document.querySelector("[data-header-cart-total]");
    let cartEmptyprice = document.querySelector("[data-cart-empty]");
    if (cartEmptyprice && cartpriceSelector) {
      cartpriceSelector.textContent = "";
      cartpriceSelector.classList.add("hidden");
    }
  }
}

function cartCountUpdate(itemCount) {
  let cartCountSelectors = document.querySelectorAll("[data-header-cart-count]");
  document
    .querySelector("[data-cart-wrapper]")
    .setAttribute("data-item-count", itemCount);
  Array.from(cartCountSelectors).forEach(function (cartCountSelector) {
    if (itemCount > 0) {
      if (itemCount > 99) {
        cartCountSelector.textContent = "";
        cartCountSelector.closest(".cart.header-icons-link").classList.add("dot-icon")
      } else {
        cartCountSelector.textContent = itemCount;
        cartCountSelector.closest(".cart.header-icons-link").classList.remove("dot-icon")
      }
      cartCountSelector.classList.remove("hidden");
    } else {
      cartCountSelector.textContent = "";
      cartCountSelector.classList.add("hidden");
    }
    // if (itemCount == 1) {
    //     let itemText = cartCountSelector.getAttribute('data-item-text');
    //     document.querySelector('.cart-item-text').textContent = itemText;
    // }
    // else
    // {
    //     let itemsText = cartCountSelector.getAttribute('data-items-text');
    //     document.querySelector('.cart-item-text').textContent = itemsText;
    // }
  });
}

function cartTotalprice(section = document) {
  let cartSection = section.querySelector("[data-cart-wrapper]");
  let cartpriceSelector = document.querySelector("[data-header-cart-total]");
  if (cartSection) {
    let cartPrice = section.querySelector(
      "[data-cart-prices] [data-cart-final-price]"
    ).textContent;
    cartSection.setAttribute("data-item-total", cartPrice);
    let cartSubtotalprice = cartSection.getAttribute("data-item-total");
    let cartQuantity = cartSection.getAttribute("data-item-count");
    if (cartQuantity > 0 && cartpriceSelector) {
      cartpriceSelector.textContent = cartSubtotalprice;
      cartpriceSelector.classList.remove("hidden");
    }
  }
}

function cartNoteUpdate() {
  let cartNoteElements = document.querySelectorAll("[data-cart-note]");
  var cartNoteTyping;
  Array.from(cartNoteElements).forEach(function (element) {
    element.addEventListener("keydown", (event) => {
      clearTimeout(cartNoteTyping);
    });
    element.addEventListener("keyup", (event) => {
      clearTimeout(cartNoteTyping);
      cartNoteTyping = setTimeout(function () {
        const body = JSON.stringify({
          note: element.value,
        });
        fetch(cartUpdateUrl, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Accept: `application/json`,
          },
          body,
        }).then((response) => {
          return response.text();
        });
      }, 1000);
    });
  });
}
/* Cart change item event start */

changeCartItem = function (line, quantity, section, cartItem) {
  let sectionId = section.dataset.section;
  let allErrorSelectors = section.querySelectorAll(".cart-item-error");
  Array.from(allErrorSelectors).forEach(function (errorSelector) {
    errorSelector.querySelector("[data-error-text]").innerHTML = "";
    errorSelector.style.display = "none";
  });
  const body = JSON.stringify({
    line,
    quantity,
    sections: [sectionId],
  });
  fetch(cartChangeUrl, {
    method: "POST",
    headers: { "Content-Type": "application/json", Accept: `application/json` },
    body,
  })
    .then((response) => {
      return response.text();
    })
    .then((state) => {
      const cart = JSON.parse(state);
      if (cart.status) {
        if (cartItem.querySelector(".cart-item-error")) {
          let quantityWrappers = cartItem.querySelectorAll(".quantity-input");
          cartItem.querySelector("[data-error-text]").innerHTML = cart.message;
          cartItem.querySelector(".cart-item-error").style.display = "block";
          Array.from(quantityWrappers).forEach(function (quantity) {
            quantity.value = quantity.getAttribute("data-previous-value");
          });
          cartItem.classList.remove("disabled");
        }
        return false;
      }
      // if (cart.item_count > 0) {
      // }
      cartCountUpdate(cart.item_count);
      //  cartTotalpriceUpdate(carTotalprice);

      if (cart.sections) {
        cartContentUpdate(cart, sectionId);
      }
      // cartNoteDrawerInt(section);
    });
};
/* Cart change item event end */
if (window.location.pathname.indexOf("/cart") > -1) {
  // Shipping Estimations
  (function () {
    function shippingEstimates() {
      if (Shopify && Shopify.CountryProvinceSelector) {
        var country = document.getElementById("shippingCountry");

        if (!country) {
          return false;
        }
        var shipping = new Shopify.CountryProvinceSelector(
          "shippingCountry",
          "address_province",
          {
            hideElement: "shippingProvinceContainer",
          }
        );

        setupEventListeners();
      }
    }

    function setupEventListeners() {
      var button = document.getElementById("getShippingEstimates");
      if (button) {
        button.addEventListener("click", (e) => {
          e.preventDefault();
          $("#shipping-wrapper-response")
            .html("")
            .removeClass("success")
            .removeClass("error")
            .hide();
          var shippingAddress = {};
          shippingAddress.zip = jQuery("#address_zip").val() || "";
          shippingAddress.country = jQuery("#shippingCountry").val() || "";
          shippingAddress.province = jQuery("#address_province").val() || "";
          _getCartShippingRates(shippingAddress);
        });
      }
    }

    var _getCartShippingRates = function (shippingAddress) {
      var params = {
        type: "POST",
        url: "/cart/shipping_rates.json",
        data: jQuery.param({ shipping_address: shippingAddress }),
        success: function (data) {
          _render(data.shipping_rates);
        },
        error: _onError,
      };
      jQuery.ajax(params);
    };

    var _fullMessagesFromErrors = function (errors) {
      var fullMessages = [];
      jQuery.each(errors, function (attribute, messages) {
        jQuery.each(messages, function (index, message) {
          fullMessages.push(message);
        });
      });
      return fullMessages;
    };
    var _onError = function (XMLHttpRequest, textStatus) {
      var data = eval("(" + XMLHttpRequest.responseText + ")");
      feedback = _fullMessagesFromErrors(data).join(", ") + ".";
      $("#shipping-wrapper-response")
        .html('<p class="error-text error">' + feedback + "</p>")
        .addClass("error")
        .show();
    };
    var _render = function (response) {
      if (response && response.length > 0) {
        var html = '<p class="success-text success">';
        response.forEach(function (shipping) {
          html += `<span><strong>${
            shipping.name
          }:</strong>${Shopify.formatMoney(
            shipping.price * 100,
            moneyFormat
          )}</span>`;
        });
        html += "</p>";
        $("#shipping-wrapper-response").html(html).addClass("success").show();
      } else {
        $("#shipping-wrapper-response")
          .html('<p class="error-text error">' + notAvailableLabel + "</p>")
          .addClass("error")
          .show();
      }
    };
    setTimeout(function () {
      shippingEstimates();
    }, 500);

    window.shippingEstimates = shippingEstimates;
  })();
  document.addEventListener("shopify:section:load", shippingEstimates, false);
}

function stickyformqty() {

  let quantityChange = document.querySelector("[data-quantity-input]");
    if(quantityChange){
    quantityChange.addEventListener("change", function() {
      document.getElementById("sticky_quantity").value = this.value;
    });
    }
  let quantityInc = document.querySelector("[data-qty-increment]");
    if(quantityInc){
   quantityInc.addEventListener("click", function (event) {
        let quantityincval = document.querySelector("[data-quantity-input]");
            quantityincval = parseInt(quantityincval.value);
            quantityincval = quantityincval + 1;
        document.getElementById("sticky_quantity").value = quantityincval ;
        document.querySelector('[data-quantity-input]').value = quantityincval;
      });
    }
    
  let quantityDec = document.querySelector("[data-qty-decrement]");
     if(quantityDec){
   quantityDec.addEventListener("click", function (event) {
        let quantitydecval = document.querySelector("[data-quantity-input]");
            quantitydecval = parseInt(quantitydecval.value);
            quantitydecval = quantitydecval - 1;
     if(quantitydecval > 0){
        document.getElementById("sticky_quantity").value = quantitydecval;
        document.querySelector('[data-quantity-input]').value = quantityincval;
     }
  });
     }
  }
