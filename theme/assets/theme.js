function roundToTwo(num) {
    return +(Math.round(num + "e+2") + "e-2");
}
const getMousePos = (e) => {
    var pos = e.currentTarget.getBoundingClientRect();
    return {
        x: e.clientX - pos.left,
        y: e.clientY - pos.top,
    };
};

function debounce(fn, wait = 300) {
    let t;
    return (...args) => {
        clearTimeout(t);
        t = setTimeout(() => fn.apply(this, args), wait);
    };
}

Shopify.bind = function(fn, scope) {
    return function() {
        return fn.apply(scope, arguments);
    };
};

Shopify.setSelectorByValue = function(selector, value) {
    for (var i = 0, count = selector.options.length; i < count; i++) {
        var option = selector.options[i];
        if (value == option.value || value == option.innerHTML) {
            selector.selectedIndex = i;
            return i;
        }
    }
};

Shopify.addListener = function(target, eventName, callback) {
    target.addEventListener ?
        target.addEventListener(eventName, callback, false) :
        target.attachEvent("on" + eventName, callback);
};

Shopify.postLink = function(path, options) {
    options = options || {};
    var method = options["method"] || "post";
    var params = options["parameters"] || {};

    var form = document.createElement("form");
    form.setAttribute("method", method);
    form.setAttribute("action", path);

    for (var key in params) {
        var hiddenField = document.createElement("input");
        hiddenField.setAttribute("type", "hidden");
        hiddenField.setAttribute("name", key);
        hiddenField.setAttribute("value", params[key]);
        form.appendChild(hiddenField);
    }
    document.body.appendChild(form);
    form.submit();
    document.body.removeChild(form);
};

Shopify.CountryProvinceSelector = function(
    country_domid,
    province_domid,
    options
) {
    this.countryEl = document.getElementById(country_domid);
    this.provinceEl = document.getElementById(province_domid);
    this.provinceContainer = document.getElementById(
        options["hideElement"] || province_domid
    );

    Shopify.addListener(
        this.countryEl,
        "change",
        Shopify.bind(this.countryHandler, this)
    );

    this.initCountry();
    this.initProvince();
};

Shopify.CountryProvinceSelector.prototype = {
    initCountry: function() {
        var value = this.countryEl.getAttribute("data-default");
        Shopify.setSelectorByValue(this.countryEl, value);
        this.countryHandler();
    },

    initProvince: function() {
        var value = this.provinceEl.getAttribute("data-default");
        if (value && this.provinceEl.options.length > 0) {
            Shopify.setSelectorByValue(this.provinceEl, value);
        }
    },

    countryHandler: function(e) {
        var opt = this.countryEl.options[this.countryEl.selectedIndex];
        var raw = opt.getAttribute("data-provinces");
        var provinces = JSON.parse(raw);

        this.clearOptions(this.provinceEl);
        if (provinces && provinces.length == 0) {
            this.provinceContainer.style.display = "none";
        } else {
            for (var i = 0; i < provinces.length; i++) {
                var opt = document.createElement("option");
                opt.value = provinces[i][0];
                opt.innerHTML = provinces[i][1];
                this.provinceEl.appendChild(opt);
            }

            this.provinceContainer.style.display = "";
        }
    },

    clearOptions: function(selector) {
        while (selector.firstChild) {
            selector.removeChild(selector.firstChild);
        }
    },

    setOptions: function(selector, values) {
        for (var i = 0, count = values.length; i < values.length; i++) {
            var opt = document.createElement("option");
            opt.value = values[i];
            opt.innerHTML = values[i];
            selector.appendChild(opt);
        }
    },
};
const addressSelectors = {
    customerAddresses: "body",
    addressCountrySelect: "[data-address-country]",
    addressContainer: "[data-address]",
    toggleAddressButton: "button[aria-expanded]",
    cancelAddressButton: 'button[type="reset"]',
    deleteAddressButton: "button[data-confirm-message]",
};

const attributes = {
    expanded: "aria-expanded",
    confirmMessage: "data-confirm-message",
};

class CustomerAddresses {
    constructor() {
        this.elements = this._getElements();
        if (Object.keys(this.elements).length === 0) return;
        this._setupCountries();
        this._setupEventListeners();
    }

    _getElements() {
        const container = document.querySelector(
            addressSelectors.customerAddresses
        );
        return container ? {
            container,
            addressContainer: container.querySelector(
                addressSelectors.addressContainer
            ),
            toggleButtons: document.querySelectorAll(
                addressSelectors.toggleAddressButton
            ),
            deleteButtons: container.querySelectorAll(
                addressSelectors.deleteAddressButton
            ),
            countrySelects: container.querySelectorAll(
                addressSelectors.addressCountrySelect
            ),
        } : {};
    }

    _setupCountries() {
        if (Shopify && Shopify.CountryProvinceSelector) {
            // eslint-disable-next-line no-new
            new Shopify.CountryProvinceSelector(
                "AddressCountry_new",
                "AddressProvince_new", {
                    hideElement: "AddressProvinceContainer_new",
                }
            );
            this.elements.countrySelects.forEach((select) => {
                const formId = select.dataset.formId;
                // eslint-disable-next-line no-new
                new Shopify.CountryProvinceSelector(
                    `AddressCountry_${formId}`,
                    `AddressProvince_${formId}`, {
                        hideElement: `AddressProvinceContainer_${formId}`,
                    }
                );
            });
        }
    }

    _setupEventListeners() {
        this.elements.toggleButtons.forEach((element) => {
            element.addEventListener("click", this._handleAddEditButtonClick);
        });
        this.elements.deleteButtons.forEach((element) => {
            element.addEventListener("click", this._handleDeleteButtonClick);
        });
    }

    _toggleExpanded(target) {
        this.elements = this._getElements();
        this._setupCountries();
        this._setupEventListeners();
    }

    _handleAddEditButtonClick = ({ currentTarget }) => {
        this._toggleExpanded(currentTarget);
    };
    _handleDeleteButtonClick = ({ currentTarget }) => {
        // eslint-disable-next-line no-alert
        if (confirm(currentTarget.getAttribute(attributes.confirmMessage))) {
            Shopify.postLink(currentTarget.dataset.target, {
                parameters: { _method: "delete" },
            });
        }
    };
}

//  wave animation code start
class ShapeOverlays {
    constructor(elm) {
        this.elm = elm;
        this.path = elm.querySelectorAll("path");
        this.numPoints = 2;
        this.duration = 600;
        this.delayPointsArray = [];
        this.delayPointsMax = 0;
        this.delayPerPath = 200;
        this.timeStart = Date.now();
        this.isOpened = false;
        this.isAnimating = false;
    }

    toggle() {
        this.isAnimating = true;
        for (var i = 0; i < this.numPoints; i++) {
            this.delayPointsArray[i] = 0;
        }
        if (this.isOpened === false) {
            this.open();
        } else {
            this.close();
        }
    }
    open() {
        this.isOpened = true;
        this.elm.classList.add("is-opened");
        this.timeStart = Date.now();
        this.renderLoop();
    }
    close() {
        this.isOpened = false;
        this.elm.classList.remove("is-opened");
        this.timeStart = Date.now();
        this.renderLoop();
    }

    updatePath(time) {
        const points = [];

        for (var i = 0; i < this.numPoints; i++) {
            const thisEase = this.isOpened ?
                i == 1 ?
                ease.cubicOut :
                ease.cubicInOut :
                i == 1 ?
                ease.cubicInOut :
                ease.cubicOut;
            points[i] =
                thisEase(
                    Math.min(
                        Math.max(time - this.delayPointsArray[i], 0) / this.duration,
                        1
                    )
                ) * 100;
        }

        let str = "";
        str += this.isOpened ? `M 0 0 V ${points[0]} ` : `M 0 ${points[0]} `;
        for (var i = 0; i < this.numPoints - 1; i++) {
            const p = ((i + 1) / (this.numPoints - 1)) * 100;
            const cp = p - ((1 / (this.numPoints - 1)) * 100) / 2;
            str += `C ${cp} ${points[i]} ${cp} ${points[i + 1]} ${p} ${
        points[i + 1]
      } `;
        }
        str += this.isOpened ? `V 0 H 0` : `V 100 H 0`;
        return str;
    }

    render() {
        if (this.isOpened) {
            for (var i = 0; i < this.path.length; i++) {
                this.path[i].setAttribute(
                    "d",
                    this.updatePath(Date.now() - (this.timeStart + this.delayPerPath * i))
                );
            }
        } else {
            for (var i = 0; i < this.path.length; i++) {
                this.path[i].setAttribute(
                    "d",
                    this.updatePath(
                        Date.now() -
                        (this.timeStart + this.delayPerPath * (this.path.length - i - 1))
                    )
                );
            }
        }
    }
    renderLoop() {
        this.render();
        if (
            Date.now() - this.timeStart <
            this.duration +
            this.delayPerPath * (this.path.length - 1) +
            this.delayPointsMax
        ) {
            requestAnimationFrame(() => {
                this.renderLoop();
            });
        } else {
            this.isAnimating = false;
        }
    }
}

function openCloseAddressDetails(event) {
    event.preventDefault();
    let target = event.target;
    if (
        target.classList.contains("add-address") ||
        target.classList.contains("edit-text")
    ) {
        let currentActiveAddress = document.querySelector(
            ".add-address-wrapper.active"
        );
        if (currentActiveAddress) {
            currentActiveAddress.classList.add("hidden");
            currentActiveAddress.classList.remove("active");
            if (currentActiveAddress.querySelector("form")) {
                currentActiveAddress.querySelector("form").reset();
            }
        }
        let targetContent = target.getAttribute("href");
        if (document.querySelector(targetContent)) {
            document.querySelector(targetContent).classList.remove("hidden");
            document.querySelector(targetContent).classList.add("active");
            setTimeout(() => {
                document
                    .querySelector(targetContent)
                    .scrollIntoView({ behavior: "smooth" });
            }, 200);
        }
    } else {
        let targetContent = target.getAttribute("href");
        if (document.querySelector(targetContent)) {
            document
                .querySelector(targetContent)
                .scrollIntoView({ behavior: "smooth" });
            setTimeout(() => {
                target.closest(".add-address-wrapper").classList.add("hidden");
                document.querySelector(targetContent).classList.remove("active");
                if (target.closest(".add-address-wrapper").querySelector("form")) {
                    target.closest(".add-address-wrapper").querySelector("form").reset();
                }
            }, 200);
        }
    }
}
var DOMAnimations = {
    slideUp: function(element, duration = 500) {
        return new Promise(function(resolve, reject) {
            element.style.height = element.offsetHeight + "px";
            element.style.transitionProperty = `height, margin, padding`;
            element.style.transitionDuration = duration + "ms";
            element.offsetHeight;
            element.style.overflow = "hidden";
            element.style.height = 0;
            element.style.paddingTop = 0;
            element.style.paddingBottom = 0;
            element.style.marginTop = 0;
            element.style.marginBottom = 0;
            window.setTimeout(function() {
                element.style.display = "none";
                element.style.removeProperty("height");
                element.style.removeProperty("padding-top");
                element.style.removeProperty("padding-bottom");
                element.style.removeProperty("margin-top");
                element.style.removeProperty("margin-bottom");
                element.style.removeProperty("overflow");
                element.style.removeProperty("transition-duration");
                element.style.removeProperty("transition-property");
                resolve(false);
            }, duration);
        });
    },

    slideDown: function(element, duration = 500) {
        return new Promise(function(resolve, reject) {
            element.style.removeProperty("display");
            let display = window.getComputedStyle(element).display;

            if (display === "none") display = "block";

            element.style.display = display;
            let height = element.offsetHeight;
            element.style.overflow = "hidden";
            element.style.height = 0;
            element.style.paddingTop = 0;
            element.style.paddingBottom = 0;
            element.style.marginTop = 0;
            element.style.marginBottom = 0;
            element.offsetHeight;
            element.style.transitionProperty = `height, margin, padding`;
            element.style.transitionDuration = duration + "ms";
            element.style.height = height + "px";
            element.style.removeProperty("padding-top");
            element.style.removeProperty("padding-bottom");
            element.style.removeProperty("margin-top");
            element.style.removeProperty("margin-bottom");
            window.setTimeout(function() {
                element.style.removeProperty("height");
                element.style.removeProperty("overflow");
                element.style.removeProperty("transition-duration");
                element.style.removeProperty("transition-property");
            }, duration);
        });
    },

    slideToggle: function(element, duration = 500) {
        if (window.getComputedStyle(element).display === "none") {
            return this.slideDown(element, duration);
        } else {
            return this.slideUp(element, duration);
        }
    },

    classToggle: function(element, className) {
        if (element.classList.contains(className)) {
            element.classList.remove(className);
        } else {
            element.classList.add(className);
        }
    },
};

function showTab(evt, tabName) {
    var i, tabContent, tabButtons;
    tabContent = document.getElementsByClassName("tab-content");
    for (i = 0; i < tabContent.length; i++) {
        tabContent[i].style.display = "none";
    }
    tabButtons = document.getElementsByClassName("tab-button");
    for (i = 0; i < tabButtons.length; i++) {
        tabButtons[i].classList.remove("active");
    }
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.classList.add("active");
}

function setCookie(cname, cvalue, exdays) {
    const d = new Date();
    d.setTime(d.getTime() + exdays * 24 * 60 * 60 * 1000);
    let expires = "expires=" + d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(";");
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) == " ") {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

if (!Element.prototype.fadeIn) {
    Element.prototype.fadeIn = function() {
        let ms = !isNaN(arguments[0]) ? arguments[0] : 400,
            func =
            typeof arguments[0] === "function" ?
            arguments[0] :
            typeof arguments[1] === "function" ?
            arguments[1] :
            null;

        this.style.opacity = 0;
        this.style.filter = "alpha(opacity=0)";
        this.style.display = "inline-block";
        this.style.visibility = "visible";

        let $this = this,
            opacity = 0,
            timer = setInterval(function() {
                opacity += 50 / ms;
                if (opacity >= 1) {
                    clearInterval(timer);
                    opacity = 1;

                    if (func) func("done!");
                }
                $this.style.opacity = opacity;
                $this.style.filter = "alpha(opacity=" + opacity * 100 + ")";
            }, 50);
    };
}

if (!Element.prototype.fadeOut) {
    Element.prototype.fadeOut = function() {
        let ms = !isNaN(arguments[0]) ? arguments[0] : 400,
            func =
            typeof arguments[0] === "function" ?
            arguments[0] :
            typeof arguments[1] === "function" ?
            arguments[1] :
            null;

        let $this = this,
            opacity = 1,
            timer = setInterval(function() {
                opacity -= 50 / ms;
                if (opacity <= 0) {
                    clearInterval(timer);
                    opacity = 0;
                    $this.style.display = "none";
                    $this.style.visibility = "hidden";

                    if (func) func("done!");
                }
                $this.style.opacity = opacity;
                $this.style.filter = "alpha(opacity=" + opacity * 100 + ")";
            }, 50);
    };
}

function isOnScreen(elem, space) {
    if (elem) {
        if (elem.length == 0) {
            return;
        }
        var $window = $(window);
        var viewport_top = $window.scrollTop();
        var viewport_height = $window.height();
        var viewport_bottom = viewport_top + viewport_height;
        var $elem = $(elem);
        var top = $elem.offset().top;
        if (space) {
            top = top + space;
        }
        var height = $elem.height();
        var bottom = top + height;

        return (
            (top >= viewport_top && top < viewport_bottom) ||
            (bottom > viewport_top && bottom <= viewport_bottom) ||
            (height > viewport_height &&
                top <= viewport_top &&
                bottom >= viewport_bottom)
        );
    }
}

function focusableElements(wrapper) {
    if (!wrapper) return false;
    let elements = Array.from(
        wrapper.querySelectorAll(
            "summary, a[href], button:enabled, [tabindex]:not([tabindex^='-']), [draggable], area, input:not([type=hidden]):enabled, select:enabled, textarea:enabled, object, iframe"
        )
    );
    return elements;
}
const listFocusElements = {};
var previousFocusElement = "";

function focusElementsRotation(wrapper) {
    stopFocusRotation();
    let elements = focusableElements(wrapper);
    if (elements == false) return false;
    let first = elements[0];
    first.focus();
    let last = elements[elements.length - 1];
    listFocusElements.focusin = (e) => {
        if (e.target !== wrapper && e.target !== last && e.target !== first) return;

        document.addEventListener("keydown", listFocusElements.keydown);
    };

    listFocusElements.focusout = function() {
        document.removeEventListener("keydown", listFocusElements.keydown);
    };

    listFocusElements.keydown = function(e) {
        if (e.code.toUpperCase() !== "TAB") return;
        if (e.target === last && !e.shiftKey) {
            e.preventDefault();
            first.focus();
        }
        if ((e.target === wrapper[0] || e.target === first) && e.shiftKey) {
            e.preventDefault();
            last.focus();
        }
    };

    document.addEventListener("focusout", listFocusElements.focusout);
    document.addEventListener("focusin", listFocusElements.focusin);
}

function stopFocusRotation() {
    document.removeEventListener("focusin", listFocusElements.focusin);
    document.removeEventListener("focusout", listFocusElements.focusout);
    document.removeEventListener("keydown", listFocusElements.keydown);
}

document.addEventListener("keydown", function(event) {
    if (event.keyCode == 27) {
        let drawers = document.querySelectorAll("[data-side-drawer]");
    }
});

//video js
function playButtonClickEvent(playButton) {
    if(playButton.closest("[data-video-main-wrapper]")){
        let parent_wrapper = playButton.closest("[data-video-main-wrapper]");
   
        let video_style = parent_wrapper.querySelector("video");
        let iframe_style = parent_wrapper.querySelector("iframe");
        playButton.addEventListener("click", function(event) {
            event.preventDefault();
            playButton.style.display = "none";
            let videoWrapper = parent_wrapper.querySelector(".video-content-wrapper");
            let videoTitle = parent_wrapper.querySelector(".video-title");
            parent_wrapper.querySelector(".video-thumbnail").style.display = "none";
            if (videoWrapper) {
                videoWrapper.style.display = "none";
            }
            if (videoTitle) {
                videoTitle.style.display = "none";
            }
            if (video_style) {
                video_style.style.display = "block";
                video_style.play();
            } else {
                iframe_style.style.display = "block";
            }
        });

    }
   
}

function videoPlayInit() {
    if (document.querySelectorAll("[data-video-play-button]")) {
        let playButtons = document.querySelectorAll("[data-video-play-button]");
        Array.from(playButtons).forEach(function(playButton) {
            if (playButton) {
                playButtonClickEvent(playButton);
            }
        });
    }
}

function slideshowElements(section = document) {
    let sliderElements = section.querySelectorAll("[data-slideshow]");
    Array.from(sliderElements).forEach(function(slider) {
        slideshowInit(slider);
    });

    
}

//testimonial js
function slideshowInit(slider) {
    let options = JSON.parse(slider.dataset.slideshow);
    if (options) {
        let flkty = new Flickity(slider, options);
       
        if (document.querySelector('[data-nav-slideshow]')) {
            if (document.querySelector('[data-nav-slideshow]').classList.contains('slideshow-nav-images')) {
                let thumbnailItems = document.querySelectorAll('.slideshow-thumbnail');
                if (thumbnailItems) {
                    thumbnailItems.forEach(function(thumbnailItem) {
                        thumbnailItem.style.transition = '0.5s ease'; 
                    });
                }
            }
        }
        
        setTimeout(() => {
            if (flkty.selectedElements.length >= flkty.cells.length) {
                slider.classList.add("disable-arrows");
                flkty.options.draggable = false;
                flkty.updateDraggable();
            } else {
                flkty.options.draggable = true;
                flkty.updateDraggable();
                slider.classList.remove("disable-arrows");
            }
            if (
                flkty.options.wrapAround == undefined ||
                flkty.options.wrapAround == false
            ) {
                let slideSizes = flkty.slides.length - 1;
                let selectSlide = flkty.selectedIndex;
                if (selectSlide == 0) {
                    slider.classList.add("left-arrow-disabled");
                } else {
                    slider.classList.remove("left-arrow-disabled");
                }
                if (selectSlide == slideSizes) {
                    slider.classList.add("right-arrow-disabled");
                } else {
                    slider.classList.remove("right-arrow-disabled");
                }
            }
          
            flkty.resize();
        }, 500);

        if (slider.classList.contains("product-grid-wrapper")) {
            const viewport = slider.querySelector(".flickity-viewport");
            const flickitySlider = slider.querySelector(".flickity-slider");
            const sliderWrapper = document.createElement("div");
            sliderWrapper.classList.add("flickity-slider--wrapper");
            viewport.appendChild(sliderWrapper);
            sliderWrapper.appendChild(flickitySlider);
        }

        flkty.on("change", function(index) {
            if (!(
                    flkty.options.autoPlay == undefined || flkty.options.autoPlay == false
                )) {
                flkty.stopPlayer();
                flkty.playPlayer();
            }
            if (
                flkty.options.wrapAround == undefined ||
                flkty.options.wrapAround == false
            ) {
                let slideSizes = flkty.slides.length - 1;
                let selectSlide = flkty.selectedIndex;
                if (selectSlide == 0) {
                    slider.classList.add("left-arrow-disabled");
                } else {
                    slider.classList.remove("left-arrow-disabled");
                }
                if (selectSlide == slideSizes) {
                    slider.classList.add("right-arrow-disabled");
                } else {
                    slider.classList.remove("right-arrow-disabled");
                }
            }
            if (slider.hasAttribute("data-slideshow-pagination")) {
                updateSliderPagination(flkty, slider);
                let sectionParent = flkty.element.closest(".shopify-section");
                if (sectionParent) {
                    let currentActive = sectionParent.querySelector(
                        ".spotlight-product-item.active"
                    );
                    let newActive = sectionParent.querySelectorAll(
                        ".spotlight-product-item"
                    )[index];
                    if (currentActive && newActive) {
                        currentActive.classList.remove("active");
                        newActive.classList.add("active");
                    }
                }
            }

            if (slider.classList.contains('announcement-bar-wrapper')) {
                let dropdown_announcement = document.querySelectorAll(
                    ".announcement-dropdown"
                );
                let dropdown_announcement_box = document.querySelectorAll(
                    ".announcement-bar-box"
                );
                if (
                    dropdown_announcement &&
                    document.querySelector("body").classList.contains("announcement-open")
                ) {
                    document.querySelector("body").classList.remove("announcement-open");
                    document.querySelector("body").classList.remove("no-scroll");
                    Array.from(dropdown_announcement).forEach(function(
                        dropdown_announcement
                    ) {
                        dropdown_announcement.classList.remove("show");
                    });
                }
                if (dropdown_announcement_box) {
                    Array.from(dropdown_announcement_box).forEach(function(
                        dropdown_announcement_box
                    ) {
                        if (dropdown_announcement_box.querySelector(".announcement-btn")) {
                            dropdown_announcement_box
                                .querySelector(".announcement-btn")
                                .classList.remove("active");
                        }
                    });
                }
            }
            if (slider.classList.contains("product-gallery-img-slider")) {
                let modelItem = slider.querySelector(
                    ".sr-product-model-item.is-selected"
                );
                if (modelItem) {
                    setTimeout(function() {
                        let Model3D = modelItem.querySelector("model-viewer");
                        if (Model3D) {
                            if (
                                Model3D.classList.contains("shopify-model-viewer-ui__disabled")
                            ) {
                                let modelBtn = modelItem.querySelector(
                                    ".shopify-model-viewer-ui__button--poster"
                                );
                                if (modelBtn) {
                                    modelBtn.removeAttribute("hidden");
                                }
                                let modelControls = modelItem.querySelector(
                                    ".shopify-model-viewer-ui__controls-area--playing"
                                );
                                if (modelControls) {
                                    modelControls.classList.remove(
                                        "shopify-model-viewer-ui__controls-area--playing"
                                    );
                                }
                            } else {
                                flkty.options.draggable = false;
                                flkty.updateDraggable();
                            }
                        }
                    }, 500);
                }
            }
            closeVideoMedia(slider, false);

           
        });

        // flkty.on("scroll", function(index) {
        //     let progressBar = slider.nextElementSibling; // Adjust this based on your HTML structure
        //     if(progressBar){
        //         progress = Math.max(0, Math.min(1, index)); // Ensure progress is between 0 and 1
        //         progressBar.style.setProperty("--progressBarWidth", progress * 100 + "%");
        //     }
            
        // });
           
        
    }
}

function updateSliderPagination(flkty, slider) {
    let paginationWrapper = slider.querySelector(".slider-pagination");
    if (paginationWrapper) {
        let slideNumber = flkty.selectedIndex + 1;
        let slidesCount = flkty.cells.length;
        let currentSlideWrapper = slider.querySelector(".current-slide");
        if (currentSlideWrapper) {
            currentSlideWrapper.innerHTML = slideNumber;
        }
        let slidesCountWrapper = slider.querySelector(".total-slides");
        if (slidesCountWrapper) {
            slidesCountWrapper.innerHTML = slidesCount;
        }
    }
}

function customSliderArrowsEvents(section = document) {
    let paginationWrapper = section.querySelectorAll(
        "[data-slideshow-navigation-button]"
    );
    Array.from(paginationWrapper).forEach(function(arrowbuttonclick) {
        let customSlider = arrowbuttonclick.closest("[data-slideshow]");
        let parentSlider = Flickity.data(customSlider);
        if (parentSlider) {
            arrowbuttonclick.addEventListener("click", function(event) {
                event.preventDefault();
                if (arrowbuttonclick.classList.contains("previous")) {
                    parentSlider.previous();
                } else {
                    parentSlider.next();
                }
            });
        }
    });
}

// ADD / REMOVE CLASS ON MOUSE OVER
// navigation element variables
function menuDropdown() {
    let header = document.querySelector(".navbar-block");
    if (header) {
        let item_hover = header.getElementsByClassName("nav-item-on-hover");
        let item_click = header.querySelectorAll(".nav-item-on-click.dropdown");
        Array.from(item_hover).forEach(function(menuSelector) {
            menuSelector.addEventListener("mouseover", function() {
                document.querySelector("body").classList.add("scroll-none");
                let current = header.querySelector(".nav-item-on-hover.active");
                if (current) {
                    current.classList.remove("active");
                }
                menuSelector.classList.add("active");
            });
            menuSelector.addEventListener("mouseout", function() {
                document.querySelector("body").classList.remove("scroll-none");
                menuSelector.classList.remove("active");
            });
        });
        Array.from(item_click).forEach(function(menuSelector) {
            menuSelector.addEventListener("click", function(e) {
                e.preventDefault();
                document.querySelector("body").classList.add("scroll-none");
                let current = header.querySelectorAll(".nav-item-on-click.active");
                menuSelector.classList.add("active");
                Array.from(current).forEach(function(activeMenu) {
                    if (activeMenu.classList.contains("active")) {
                        activeMenu.classList.remove("active");
                    }
                });
            });
        });
    }
}

//search drawer js
var searchTyping;

function search_drawer(section = document) {
    let searchSelectors = section.querySelectorAll("[data-search-open]");
    if (searchSelectors) {
        Array.from(searchSelectors).forEach(function(searchSelector) {
            searchSelector.addEventListener("click", (e) => {
                e.preventDefault();
                var searchDrawer = document.querySelector(
                    '[data-search-drawer][data-fullwidth="true"]'
                );
                let searchParent = searchSelector.closest("[data-search-parent]");
                if (searchDrawer) {
                    if (searchDrawer.classList.contains("active")) {
                        searchDrawer.classList.add("hidden");
                        searchDrawer.classList.remove("active");
                        document
                            .querySelector("body")
                            .classList.remove("no-scroll", "search-drawer-open");
                        stopFocusRotation();
                        previousFocusElement.focus();
                        previousFocusElement = "";
                    } else {
                        searchDrawer.classList.add("active");
                        searchDrawer.classList.remove("hidden");
                        document
                            .querySelector("body")
                            .classList.add("no-scroll", "search-drawer-open");
                        previousFocusElement = searchSelector;
                        focusElementsRotation(searchDrawer);
                        setTimeout(() => {
                            searchDrawer.querySelector("[data-search-input]").focus();
                        }, 100);
                    }
                    __searchResult(
                        (searchDrawer.querySelector("[data-search-input]").value = ""),
                        searchParent
                    );
                }
            });
            searchSelector.addEventListener("keydown", (e) => {
                document.querySelector("body").classList.add("tab-focus");
            });
        });
    }
    // search input
    let searchInputElements = section.querySelectorAll("[data-search-input]");
    Array.from(searchInputElements).forEach(function(searchInput) {
        let searchParent = searchInput.closest("[data-search-parent]");
        searchInput.addEventListener("keyup", (event) => {
            event.preventDefault();
            clearTimeout(searchTyping);
            searchTyping = setTimeout(function() {
                if (searchParent) {
                    let searchTerm = searchParent.querySelector(
                        "[data-search-input]"
                    ).value;
                    __searchResult(searchTerm, searchParent);
                }
            }, 1000);
        });
        searchInput.addEventListener("click", (event) => {
            let searchDrawer = document.querySelector("[data-search-drawer]");
            if (searchDrawer) {
                let headerStyle = searchDrawer.getAttribute("data-header");
                let suggestionStatus = searchDrawer.getAttribute(
                    "data-suggestionStatus"
                );
                if (
                    headerStyle == "logo_with_search_bar" &&
                    suggestionStatus == "true"
                ) {
                    searchDrawer.classList.remove("hidden");
                }
            }
        });
        searchInput.addEventListener("search", (event) => {
            event.preventDefault();
            clearTimeout(searchTyping);
            if (searchParent) {
                __searchResult("", searchParent);
            }
        });
    });

    let searchInputResetBtns = section.querySelectorAll("[data-search-reset]");
    Array.from(searchInputResetBtns).forEach(function(searchInputResetBtn) {
        searchInputResetBtn.addEventListener("click", (event) => {
            event.preventDefault();
            clearTimeout(searchTyping);
            searchInputResetBtn
                .closest("form")
                .querySelector("[data-search-input]").value = "";
            setTimeout(function() {
                searchInputResetBtn
                    .closest("form")
                    .querySelector("[data-search-input]")
                    .focus();
                    let searchParent = searchInputResetBtn.closest("[data-search-parent]");
                    let searchTerm = searchParent.querySelector(
                        "[data-search-input]"
                    ).value;
                    __searchResult(searchTerm, searchParent);
            }, 300);
        });
    });

    let searchBySpeechs = section.querySelectorAll("[data-speech-search]");
    Array.from(searchBySpeechs).forEach(function(searchBySpeech) {
        initSpeectRecognition(searchBySpeech);
    });
}

// searchResult funtion
var __searchResult = function(searchTerm, searchparent) {
    if (searchparent) {
        let resultContainer = searchparent.querySelector("[data-result-container]");
        let suggestionContainer = searchparent.querySelector(
            "[data-suggestions-container]"
        );
        var fullwidth = document.querySelector('[data-search-drawer][data-fullwidth="true"]');
        let searchDrawer = resultContainer.closest("[data-search-drawer]");
        let headerStyle = searchDrawer.getAttribute("data-header");
        if (headerStyle == "logo_with_search_bar") {
          if(window.innerWidth >= 768){
            var style = "fullwidth"  
          }else{
            var style = "drawer";       
          }        
        }
        else{
          var style = fullwidth ? 'fullwidth' : 'drawer';          
        }
        if (resultContainer) {
            let searchDrawer = resultContainer.closest("[data-search-drawer]");
            let headerStyle = searchDrawer.getAttribute("data-header");
            let suggestionStatus = searchDrawer.getAttribute("data-suggestionStatus");
            if (searchTerm.replace(/\s/g, "").length > 0) {
                if (headerStyle == "logo_with_search_bar" && suggestionStatus == "false") {
                    searchDrawer.classList.remove("hidden");
                }
                if (suggestionContainer) {
                    
                    suggestionContainer.classList.add("hidden");
                }
                resultContainer.classList.remove("hidden");
                resultContainer.innerHTML = preLoadLoadGif;
                fetch(
                        mainSearchUrl +
                        "/suggest?section_id=predictive-search&q=" +encodeURIComponent(searchTerm) +"&resources[type]=" +predictiveSearchTypes +"&resources[limit]=10&resources[limit_scope]=each&resources[style]="+style+""
                    )
                    .then((response) => {
                        return response.text();
                    })
                    .then((responseText) => {
                        let resultsMarkup = new DOMParser().parseFromString(
                            responseText,
                            "text/html"
                        );
                        
                        if(style == 'drawer'){
                        let predictiveSearchElements = resultsMarkup.querySelectorAll(".predictive-search-tranding-products");

                      
                        predictiveSearchElements.forEach(element => {
                            element.classList.add("product-vertical");
                        });
                        }

                        resultContainer.innerHTML = resultsMarkup.querySelector(
                            "#shopify-section-predictive-search"
                        ).innerHTML;
                    });
            } else {
                if (suggestionContainer) {
                    suggestionContainer.classList.remove("hidden");
                }
                if (
                    headerStyle == "logo_with_search_bar" &&
                    suggestionStatus == "false"
                ) {
                     if(window.innerWidth >= 768){

                     searchDrawer.classList.add("hidden");

                   }
                }
                resultContainer.classList.add("hidden");
                resultContainer.innerHTML = "";
            }
        }
    }
};

function initSpeectRecognition(searchSpeech) {
    let speechRecognition = null;
    let listening = false;
    let searchInput = null;
    const userAgent = window.navigator.userAgent.toLowerCase();
    if (
        "webkitSpeechRecognition" in window &&
        userAgent.indexOf("chrome") > -1 &&
        !!window.chrome &&
        userAgent.indexOf("edg/") === -1
    ) {
        searchSpeech.classList.remove("hidden");
        speechRecognition = new window.webkitSpeechRecognition();
        speechRecognition.continuous = false;
        speechRecognition.interimResults = false;
        searchInput = searchSpeech.closest("form").querySelector("[data-search-input]");
        speechRecognition.addEventListener(
            "result",
            debounce((evt) => {
                if (evt.results) {
                    const term = evt.results[0][0].transcript;
                    searchInput.value = term;
                    searchInput.focus();
                    searchInput.dispatchEvent(new Event("input"));
                    let searchparent = searchInput.closest("[data-search-parent]");
                    __searchResult(term, searchparent);
                }
            }, 300)
        );

        speechRecognition.addEventListener("audiostart", () => {
            listening = true;
            searchSpeech.classList.add("active");
        });

        speechRecognition.addEventListener("audioend", () => {
            listening = false;
            searchSpeech.classList.remove("active");
        });

        searchSpeech.addEventListener("click", function(evt) {
            evt.preventDefault();
            if (listening) {
                speechRecognition.stop();
                listening = false;
            } else {
                speechRecognition.start();
                listening = true;
            }
        });

        searchSpeech.addEventListener("keydown", (evt) => {
            if (evt.code === "Space" || evt.code === "Enter") {
                evt.preventDefault();
                if (listening) {
                    speechRecognition.stop();
                } else {
                    speechRecognition.start();
                }
            }
        });
    }
}

function search_drawer_tab() {
    let elements = document.querySelectorAll(".predictive-tab-item");
    if (elements) {
        Array.from(elements).forEach(function(element) {
            setTimeout(function() {
                element.addEventListener("click", function(event) {
                    event.preventDefault();
                    if (element.classList.contains("is-selected")) return false;
                    let parent = element.closest(".shopify-section");
                    let currentActiveTab = parent.querySelector(
                        ".predictive-tab-item.is-selected"
                    );
                    let currentActiveProducts = parent.querySelector(".content_active");
                    let selectedTabProducts = parent.querySelector(
                        "." + element.dataset.filter
                    );
                    if (selectedTabProducts) {
                        if (currentActiveTab) {
                            currentActiveTab.classList.remove("is-selected");
                        }
                        if (currentActiveProducts) {
                            currentActiveProducts.classList.remove("content_active");
                            currentActiveProducts.style.display = "none";
                        }
                        element.classList.add("is-selected");
                        selectedTabProducts.classList.add("content_active");
                        selectedTabProducts.style.display = "block";
                    }
                });
            }, 400);
        });
    }
}

// shopify featured product variant selector
function variant_selector(section = document) {
    let elements = section.querySelectorAll("[data-product-loop-variants]");
    let selectIds = section.querySelectorAll('[name="id"]');
    Array.from(selectIds).forEach(function(selectId) {
        selectId.removeAttribute("disabled");
    });
    Array.from(elements).forEach(function(element) {
        element.addEventListener("change", function() {
            //get parent options
            let productWrapper = this.closest("[data-product-wrapper]");
            let productSection = productWrapper.closest(".shopify-section");
            let productMedia = productWrapper.querySelector("[data-product-media");
            let productOption = productWrapper.querySelector("[data-product_variant_options]");
            let colorOption = productWrapper.querySelector(".color-option");
            // create array from all options parent (ul)
            let productOptions = Array.from(
                productWrapper.querySelectorAll("[data-product-loop-variants]")
            );

            let option_type = productOption.getAttribute("data-button-type");
            // create global variable
            let options = "";
            if (productOptions) {
                if (option_type == "button") {
                    options = productOptions.map(function(option) {
                        return Array.from(option.querySelectorAll("input")).find(
                            (radio) => radio.checked
                        ).value;
                    });
                } else {
                    options = productOptions.map(function(option) {
                        return Array.from(option.querySelectorAll("[data-option]")).find(
                            (option) => option.selected
                        ).value;
                    });
                   
                }
            }
            if (option_type == "button") {
                let prevActiveOption = element.querySelector("[data-option].active");
                if (prevActiveOption) {
                    prevActiveOption.classList.remove("active");
                }
                element.querySelector("input:checked").classList.add("active");
            } else {
                let value = element.value;
                let prevActiveOption = element.querySelector("option[selected]");
                if (prevActiveOption) {
                    prevActiveOption.removeAttribute("selected");
                }

                element.querySelector('option[value="' + CSS.escape(value) + '"]').setAttribute("selected", true);
                let optionWrapper = this.closest("[data-product-wrapper]");
               // const optionValues = Array.from(productOptions.querySelector("option"));
                for (let i = 0; i < options.length; i++) {
                 
               
                    const optionValue = CSS.escape(options[i]);
                    const optionElement = optionWrapper.querySelector('option[value="' + optionValue + '"]');
                    
                    setTimeout(function(){
                        if (optionElement.classList.contains('hidden')) {
                            //console.log(optionElement.closest('select').querySelectorAll('option'));
                            optionElement.closest('select').querySelectorAll('option').forEach(opt => {
                                if (opt.classList.contains('hidden')) {
                                    opt.removeAttribute('selected');
                                }
                                if (!opt.classList.contains('hidden')) {
                                    opt.setAttribute('selected', 'selected');
                                    opt.click();
                                    return;
                                }
                            });
                                                           
                        } 
                    },200);
                 
                }
              
            }

            if (colorOption && element.classList.contains("color-swatches")) {

                let optionValue = element.querySelector("input:checked").value;
                let selectedOptionText = productOption.querySelector('[selected-option-name]')
                if (selectedOptionText) {
                    selectedOptionText.textContent = optionValue;
                }
            }
            if (productSection.querySelector("[data-sticky-products]")) {
                Array.from(
                    productSection.querySelectorAll("[data-form-error]")
                ).forEach(function(errorContainer) {
                    errorContainer.classList.add("hidden");
                    errorContainer.textContent = "";
                });
            } else {
                Array.from(productWrapper.querySelectorAll("[data-form-error]")).forEach(function(errorContainer) {
                    errorContainer.classList.add("hidden");
                    errorContainer.textContent = "";
                });
            }

            let variantData = "";
            if (
                productWrapper.querySelector(
                    '[type="application/json"][data-name="main-product"]'
                )
            ) {
                variantData = JSON.parse(
                    productWrapper.querySelector(
                        '[type="application/json"][data-name="main-product"]'
                    ).textContent
                );
            }

            // get json content

            currentVariant = getCurrentSelectedVariant(
                options,
                "options",
                productWrapper,
                variantData
            );
            let selectedElement = element.querySelector('option[selected]');
            if (option_type == "button") {
              selectedElement = element.querySelector("input:checked");
            }
            if (selectedElement && selectedElement.hasAttribute('data-product-url')) {
              
              
              let requestURL = selectedElement.dataset.productUrl;
              
              let optionValues = Array.from(
                productOption.querySelectorAll("option[selected]")
              ).map(({ dataset }) => dataset.valueProductId);
              if (option_type == "button") {
                optionValues = Array.from(
                  productOption.querySelectorAll("input:checked")
                ).map(({ dataset }) => dataset.valueProductId);
              }
              requestURL += `?option_values=${optionValues}`;
              
              Array.from(productOption.querySelectorAll("[data-product-url]")).map(({ dataset }) => dataset.valueProductId);
              const uniqueValues = Array.from(productOption.querySelectorAll("[data-product-url]")).reduce((acc, current) => {
                if (!acc.includes(current.dataset.productUrl)) {
                  acc.push(current.dataset.productUrl);
                }
                return acc;
              }, []);
              if(uniqueValues.length == 1 || productWrapper.classList.contains("quickview-drawer-content")){
                requestURL += `&section_id=${productWrapper.dataset.sectionId}`;
              }
      
              fetch(requestURL)
                .then((response) => response.text())
                .then((text) => {
                  var updatedProductHTML = new DOMParser().parseFromString(
                    text,
                    "text/html"
                  );
                  
                  if(uniqueValues.length == 1 || productWrapper.classList.contains("quickview-drawer-content")){
                  if (updatedProductHTML.querySelector("[data-product-wrapper]")) {
                      productWrapper.innerHTML =
                        updatedProductHTML.querySelector("[data-product-wrapper]").innerHTML;                
                      getATCelement(productWrapper);
                      getQuantityElement(productWrapper);
                    }
                  }else{
                    if (
                      document.querySelector("main#MainContent") &&
                      updatedProductHTML.querySelector("main#MainContent")
                    ) {
                      document.querySelector("main#MainContent").innerHTML =
                        updatedProductHTML.querySelector("main#MainContent").innerHTML;
                                  
                      getATCelement(document.querySelector("main#MainContent"));
                      getQuantityElement(document.querySelector("main#MainContent"));
                    }
                  }
                  if (productWrapper.classList.contains("main-product-section")) {
                    var _updateUrl =  selectedElement.dataset.productUrl;
                    window.history.replaceState({}, null, _updateUrl);
                  }
                  onloadEvents();
                   if (Shopify.PaymentButton) {
                    Shopify.PaymentButton.init();
                  }
                })
                .catch((e) => {});
            } else {
              if (currentVariant) {
                  let productOptionsWithValues = "";
                  if (
                      productWrapper.querySelector(
                          '[type="application/json"][data-name="main-product-options"]'
                      )
                  ) {
                      productOptionsWithValues = JSON.parse(
                          productWrapper.querySelector(
                              '[type="application/json"][data-name="main-product-options"]'
                          ).textContent
                      );
                  }
                
                  if(!productSection.querySelector('[data-combined-listing-product]')){ 
                    if (productOptionsWithValues != "" && variantData != "") {
                        updateOptionsAvailability(
                            variantData,
                            productOptionsWithValues,
                            currentVariant,
                            productOptions,
                            option_type
                        );
                    }
                  }
                  else{
              let requestURL = `${window.location.pathname}?variant=${currentVariant.id}&section_id=${productWrapper.dataset.sectionId}`;
              fetch(requestURL)
                  .then((response) => response.text())
                  .then((text) => {
                    var updatedProductHTML = new DOMParser().parseFromString(
                      text,
                      "text/html"
                    );
                    // console.log(productWrapper.querySelector("[data-product_variant_options]"),updatedProductHTML.querySelector("[data-product_variant_options]"))
                    if (productWrapper.querySelector("[data-product_variant_options]") && updatedProductHTML.querySelector("[data-product_variant_options]")) {
                        productWrapper.querySelector("[data-product_variant_options]").innerHTML = updatedProductHTML.querySelector("[data-product_variant_options]").innerHTML;
                      if(productWrapper.closest('.shopify-section')){
                        variant_selector(productWrapper.closest('.shopify-section'))
                      }
                    }  
                    if (productSection.querySelector("[data-product_variant_options-sticky]") && updatedProductHTML.querySelector("[data-product_variant_options-sticky]")) {
                        productSection.querySelector("[data-product_variant_options-sticky]").innerHTML = updatedProductHTML.querySelector("[data-product_variant_options-sticky]").innerHTML;
                        stickyProductOptions(productSection)
                    }
                    
                    
                  })
                  .catch((e) => {});
            }
                  let selectIds = productWrapper.querySelectorAll('[name="id"]');
                  Array.from(selectIds).forEach(function(selectId) {
                      selectId.value = currentVariant.id;
                      selectId.dispatchEvent(new Event("change", { bubbles: true }));
                  });
  
                  updatePrice(productWrapper, currentVariant);
                  //  ProductButtonText(cartButton, cartButtonText, currentVariant);
                  featuredImage(currentVariant, productWrapper);
                  let productdataType = productMedia.getAttribute("data-type");
                  if (productdataType == "stacked") {
                      if (currentVariant.featured_image != null) {
                          let productFeaturedmedia =
                              "#productmedia-" + currentVariant.featured_media.id;
                          let scrollMedia =
                              productWrapper.querySelector(productFeaturedmedia);
                          let showMoreButton = document.getElementById("showMoreButton");
                          if (scrollMedia) {
                              if (scrollMedia.classList.contains("hidden-media")) {
                                  showMoreButton.click();
                                  scrollMedia.scrollIntoView({
                                      behavior: "smooth",
                                  });
                              } else {
                                  scrollMedia.scrollIntoView({
                                      behavior: "smooth",
                                  });
                              }
                          }
                      }
                  }
                  thumbnailChange();
                  var baseUrl = window.location.pathname;
                  if (baseUrl.indexOf("/products/") > -1) {
                      var _updateUrl = baseUrl + "?variant=" + currentVariant.id;
                      window.history.replaceState({}, null, _updateUrl);
                  }
                  pickUpAvialabiliy(productWrapper, currentVariant);
  
                  let productvariantInventory = "";
                  let variantInventory = "";
                  if (
                      productWrapper.querySelector(
                          '[type="application/json"][data-name="main-product-inventories"]'
                      )
                  ) {
                      productvariantInventory = JSON.parse(
                          productWrapper.querySelector(
                              '[type="application/json"][data-name="main-product-inventories"]'
                          ).textContent
                      );
                      variantInventory = productvariantInventory.find((variant) => {
                          return variant.id == currentVariant.id;
                      });
                  }
                  let inventoryBar = productWrapper.querySelector(
                      "[data-product-inventory-bar-wrapper]"
                  );
                  if (
                      inventoryBar &&
                      productvariantInventory != "" &&
                      currentVariant != undefined
                  ) {
                      updateInventroyBar(
                          variantInventory.inventory_quantity,
                          variantInventory.inventory_policy,
                          variantInventory.inventory_management,
                          currentVariant
                      );
                  }
                  ProductButtonText(productWrapper, currentVariant, variantInventory);
                  // updateVariantStatus(productWrapper,variantsList, currentVariant,option_type,options);
              } else {
                  ProductButtonText(productWrapper, currentVariant, "");
              }
              if (productSection.querySelector("[data-sticky-products]")) {
                setTimeout(function() {
                    updateStickyOptions(
                        productWrapper,
                        productSection.querySelector("[data-sticky-products]"),
                        option_type
                    );
                }, 500);
            }
            }
        });
    });
}

function getCurrentSelectedVariant(
    options,
    option_type,
    selector,
    variantData
) {
    if (!variantData) return false;
    let currentVariant = variantData.find((variant) => {
        if (option_type === "options") {
            return !variant.options
                .map((option, index) => {
                    return options[index] === option;
                })
                .includes(false);
        }
        if (option_type === "id") {
            return variant.id == options;
            // return variant.title == options;
        }
    });
  if(!currentVariant && !selector.querySelector('[data-combined-listing-product]')){ 
        return getFirstAvailableVariant(
            options,
            option_type,
            selector,
            variantData
        );
    } else {
        return currentVariant;
    }
}

function onloadVariants(section = document) {
    //get parent options
    Array.from(
        section.querySelectorAll("[data-product_variant_options]")
    ).forEach(function(optionsParent) {
        if (optionsParent.closest("[data-sticky-products]")) return false;
        let productWrapper = optionsParent.closest("[data-product-wrapper]");
        let productSection = productWrapper.closest(".shopify-section");
        // create array from all options parent (ul)
        let productOptions = Array.from(productWrapper.querySelectorAll("[data-product-loop-variants]"));

        if(productSection.querySelector('[data-combined-listing-product]')) return;
      
        let option_type = optionsParent.getAttribute("data-button-type");
        // create global variable
        let options = "";
        if (productOptions) {
            if (option_type == "button") {
                // create array of selected options
                options = productOptions.map(function(option) {
                    return Array.from(option.querySelectorAll("input")).find(
                        (radio) => radio.checked
                    ).value;
                });
            } else {
                options = productOptions.map(function(option) {
                    return Array.from(option.querySelectorAll("[data-option]")).find(
                        (option) => option.selected
                    ).value;
                });
            }
        }

        let variantData = "";
        if (
            productWrapper.querySelector(
                '[type="application/json"][data-name="main-product"]'
            )
        ) {
            variantData = JSON.parse(
                productWrapper.querySelector(
                    '[type="application/json"][data-name="main-product"]'
                ).textContent
            );
        }
        currentVariant = getCurrentSelectedVariant(
            options,
            option_type,
            productWrapper,
            variantData
        );
        // trigger value on select
        if (currentVariant) {
            let productOptionsWithValues = "";
            if (
                productWrapper.querySelector(
                    '[type="application/json"][data-name="main-product-options"]'
                )
            ) {
                productOptionsWithValues = JSON.parse(
                    productWrapper.querySelector(
                        '[type="application/json"][data-name="main-product-options"]'
                    ).textContent
                );
            }
            if (productOptionsWithValues != "" && variantData != "") {
                updateOptionsAvailability(
                    variantData,
                    productOptionsWithValues,
                    currentVariant,
                    productOptions,
                    option_type
                );
            }
        }
        if (productSection.querySelector("[data-sticky-products]")) {
            setTimeout(function() {
                updateStickyOptions(
                    productWrapper,
                    productSection.querySelector("[data-sticky-products]"),
                    option_type
                );
            }, 100);
        }
    });
}

function stickyProductOptions(section = document) {
    let productContainers = section.querySelectorAll("[data-sticky-products]");
    Array.from(productContainers).forEach(function(container) {
        var stickyProductOptions =
            container.getElementsByClassName("productOption");
        if (stickyProductOptions.length > 0) {
            Array.from(stickyProductOptions).forEach(function(productOption) {
                productOption.addEventListener("change", () => {
                    let option_type = productOption
                        .closest("[data-product_variant_options]")
                        .getAttribute("data-button-type");
                    let optionId = productOption.getAttribute("data-id");
                    
                    optionId = optionId.replace(/^sticky-/, "");
                    if (option_type == "button") {
                        productOption
                            .closest(".shopify-section")
                            .querySelector("[data-id='" + optionId + "']")
                            .click();
                    } else {
                       
                        productOption
                            .closest(".shopify-section")
                            .querySelector("[data-id='" + optionId + "']").value =
                            productOption.value;
                        productOption
                            .closest(".shopify-section")
                            .querySelector("[data-id='" + optionId + "']")
                            .dispatchEvent(new Event("change"));
                    }
                });
            });
        }
    });
}

function updateStickyOptions(
    productWrapper,
    productStickyWrapper,
    option_type
) {
    if (
        productWrapper.querySelector("[data-product_variant_options]") &&
        productStickyWrapper.querySelector("[data-product_variant_options]")
    ) {
        let getproductoptionsHtmls = productWrapper.querySelector(
            "[data-product_variant_options]"
        ).innerHTML;
        let divContent = document.createElement("div");
        divContent.innerHTML = getproductoptionsHtmls;
        let optionsId = divContent.querySelectorAll(".productOption");
        Array.from(optionsId).forEach(function(option) {
            let optionsId = "sticky-" + option.id;
            option.setAttribute("id", optionsId);
            if (option_type == "button") {
                option.setAttribute("name", "sticky-" + option.name);
                option.nextElementSibling.setAttribute("for", optionsId);
                option.removeAttribute("checked");
                if (option.classList.contains("active")) {
                    option.setAttribute("checked", true);
                }
            }
        });
        productStickyWrapper.querySelector(
            "[data-product_variant_options]"
        ).innerHTML = divContent.innerHTML;
        stickyProductOptions(productStickyWrapper.closest(".shopify-section"));
    }
}

function getFirstAvailableVariant(options, option_type, selector, allVariants) {
    let availableVariant = null,
        slicedCount = 0;
    do {
        options.pop();
        slicedCount += 1;
        availableVariant = allVariants.find((variant) => {
            return variant["options"]
                .slice(0, variant["options"].length - slicedCount)
                .every((value, index) => value === options[index]);
        });
    } while (!availableVariant && options.length > 0);
    if (availableVariant) {
        let fieldsets = Array.from(
            selector.querySelectorAll("[data-product-loop-variants]")
        );
        fieldsets.forEach((fieldset, index) => {
            if (option_type == "dropdown") {
                let option = fieldset;
                if (option && option.value != availableVariant["options"][index]) {
                    option.value = availableVariant["options"][index];
                    option.dispatchEvent(new Event("change"));
                }
            } else {
                let option = fieldset.querySelector(
                    'input[value="' + CSS.escape(availableVariant["options"][index]) + '"]'
                );
                if (option && option.checked == false) {
                    option.click();
                }
            }
        });
    }
    return availableVariant;
}

const classAddToSelector = (
    selector,
    valueIndex,
    available,
    combinationExists,
    variantStyle
) => {
    if (variantStyle == "button") {
        const optionValue = Array.from(selector.querySelectorAll(".productOption"))[
            valueIndex
        ];
        if (optionValue) {
            optionValue.parentElement.classList.toggle("hidden", !combinationExists);
            optionValue.classList.toggle("not-available", !available);
        }
    } else {
        
        const optionValue = Array.from(
            selector.querySelectorAll(".productOption option")
        )[valueIndex];
        if (optionValue) {
            optionValue.classList.toggle("hidden", !combinationExists);
           
            optionValue.toggleAttribute("disabled", !available);

            //console.log(combinationExists);
            // if (combinationExists && !optionValue.hasAttribute("disabled")) {
            //     optionValue.setAttribute('selected', true);
            
            // } else {
            //     if(optionValue.hasAttribute("disabled")){
            //         optionValue.removeAttribute('selected');
            //     }
                
            // }
        
            
        }
    }
};

function updateOptionsAvailability(
    product,
    productOptions,
    selectedVariant,
    optionSelectors,
    variantStyle
) {
    if (!selectedVariant) {
        return;
    }
    if (optionSelectors && optionSelectors[0]) {
        productOptions[0]["values"].forEach((value, valueIndex) => {
            const combinationExists = product.some(
                    (variant) => variant["option1"] === value && variant
                ),
                availableVariantExists = product.some(
                    (variant) => variant["option1"] === value && variant["available"]
                );
            classAddToSelector(
                optionSelectors[0],
                valueIndex,
                availableVariantExists,
                combinationExists,
                variantStyle
            );
            if (optionSelectors[1]) {
                productOptions[1]["values"].forEach((value2, valueIndex2) => {
                    const combinationExists2 = product.some(
                            (variant) =>
                            variant["option2"] === value2 &&
                            variant["option1"] === selectedVariant["option1"] &&
                            variant
                        ),
                        availableVariantExists2 = product.some(
                            (variant) =>
                            variant["option2"] === value2 &&
                            variant["option1"] === selectedVariant["option1"] &&
                            variant["available"]
                        );
                    classAddToSelector(
                        optionSelectors[1],
                        valueIndex2,
                        availableVariantExists2,
                        combinationExists2,
                        variantStyle
                    );
                    if (optionSelectors[2]) {
                        productOptions[2]["values"].forEach((value3, valueIndex3) => {
                            const combinationExists3 = product.some(
                                    (variant) =>
                                    variant["option3"] === value3 &&
                                    variant["option1"] === selectedVariant["option1"] &&
                                    variant["option2"] === selectedVariant["option2"] &&
                                    variant
                                ),
                                availableVariantExists3 = product.some(
                                    (variant) =>
                                    variant["option3"] === value3 &&
                                    variant["option1"] === selectedVariant["option1"] &&
                                    variant["option2"] === selectedVariant["option2"] &&
                                    variant["available"]
                                );
                            classAddToSelector(
                                optionSelectors[2],
                                valueIndex3,
                                availableVariantExists3,
                                combinationExists3,
                                variantStyle
                            );
                        });
                    }
                });
            }
        });
    }
}

function updateInventroyBar(
    variantQty,
    variantPolicy,
    variantInventoryManagment,
    variant
) {
    let productInventorys = document.querySelectorAll(
        "[data-product-inventory-bar-wrapper]"
    );
    Array.from(productInventorys).forEach(function(productInventory) {
        if (productInventory) {
            let quantity = productInventory.dataset.stock;
            quantity = parseInt(quantity);
            let minInventroyQty = productInventory.dataset.min;
            minInventroyQty = parseInt(minInventroyQty);
            let statusInventory = productInventory.querySelector(
                "[data-inventory-status]"
            );
            if (variantQty >= 0 && variantPolicy != "") {
                quantity = variantQty;
                if (
                    quantity > 0 &&
                    quantity <= minInventroyQty &&
                    variantPolicy == "deny" &&
                    variantInventoryManagment != ""
                ) {
                    if (statusInventory) {
                        statusInventory.classList.remove("hidden");
                        statusInventory.classList.remove("instock");
                        statusInventory.classList.add("lowstock");
                    }
                    if (productInventory.querySelector(".product-inventory-count")) {
                        productInventory.querySelector(
                            ".product-inventory-count"
                        ).textContent = variantQty + " Low stock";
                    }
                } else if (
                    quantity >= 0 &&
                    variant.available == true &&
                    quantity > minInventroyQty
                ) {
                    if (statusInventory) {
                        statusInventory.classList.remove("hidden");
                        statusInventory.classList.remove("lowstock");
                        statusInventory.classList.add("instock");
                    }
                    if (productInventory.querySelector(".product-inventory-count")) {
                        productInventory.querySelector(
                            ".product-inventory-count"
                        ).textContent = quantity + " In stock";
                    }
                } else {
                    if (statusInventory) {
                        statusInventory.classList.add("hidden");
                    }
                }
                productInventory.setAttribute("data-stock", variantQty);
            } else {
                if (statusInventory) {
                    statusInventory.classList.add("hidden");
                }
            }
        }
    });
}

function collectionSwatch(section = document) {
    let elements = section.querySelectorAll(
        "[data-swatch-colors] .variant-option"
    );
    Array.from(elements).forEach(function(element) {
        element.addEventListener("change", function(e) {
            e.preventDefault();
            //get parent options
            let optionParent = element.closest("[data-swatch-colors]");
            let parentElement = element.closest(".product-card");
            if (optionParent) {
                let prevActiveOption = optionParent.querySelector(
                    "li.variant-option.selected"
                );
                if (prevActiveOption) {
                    prevActiveOption.classList.remove("selected");
                }
                element.classList.add("selected");
                let hidden_element = element.querySelector(".hidden");
                if (hidden_element) {
                    let hidden_image = hidden_element.innerHTML;
                    parentElement.querySelector(".product-img .media").innerHTML =
                        hidden_image;
                }
            }
        });
    });
}

function updatePrice(productSection, selectedVariant) {
    let parentSection = productSection;
    if (
        productSection
        .closest(".shopify-section")
        .querySelector("[data-sticky-products]")
    ) {
        parentSection = productSection.closest(".shopify-section");
    }
    const selectors = parentSection.querySelectorAll("[data-price]");
    Array.from(selectors).forEach(function(priceContainer) {
        let savingStatus = priceContainer.dataset.savingStatus;
        let savingtype = priceContainer.dataset.savingType;
        let savingContainer = priceContainer.querySelector("[data-price-saving]");
        let product_price = priceContainer.querySelector("[data-regular-price]");
        let price = parseInt(selectedVariant.price);
        let product_compare_price = priceContainer.querySelector(
            "[data-compare-price]"
        );
        let compare_price = parseInt(selectedVariant.compare_at_price);
        let variantSku = "";
        if (selectedVariant && selectedVariant.sku) {
            variantSku = selectedVariant.sku;
        }
        if (product_price) {
            product_price.innerHTML = Shopify.formatMoney(price, moneyFormat);
            product_price.classList.remove("hidden");
        }
        if (product_compare_price) {
            if (compare_price > price) {
                product_compare_price.innerHTML = Shopify.formatMoney(
                    compare_price,
                    moneyFormat
                );
                product_compare_price.classList.remove("hidden");
            } else {
                product_compare_price.classList.add("hidden");
            }
        }
        let variantSkuContainers =
            productSection.querySelectorAll("[data-variant-sku]");
        if (variantSkuContainers) {
            Array.from(variantSkuContainers).forEach(function(variantSkuContainer) {
                if (variantSkuContainer) {
                    variantSkuContainer.innerHTML = variantSku;
                }
            })

        }

        let unitPriceSelector = priceContainer.querySelector("[data-unit-price]");
        if (unitPriceSelector) {
            if (selectedVariant.unit_price_measurement) {
                var unitpriceText =
                    Shopify.formatMoney(selectedVariant.unit_price, moneyFormat) + " / ";
                unitpriceText +=
                    selectedVariant.reference_value == 1 ?
                    "" :
                    selectedVariant.unit_price_measurement.reference_value;
                unitpriceText +=
                    selectedVariant.unit_price_measurement.reference_unit + "</p>";
                unitPriceSelector.innerHTML = unitpriceText;
                unitPriceSelector.classList.remove("hidden");
            } else {
                unitPriceSelector.classList.add("hidden");
            }
        }
        if (savingContainer && savingStatus == "true") {
            if (compare_price > price) {
                let percentage =
                    Math.floor(((compare_price - price) / compare_price) * 100) + "% Off";
                let savedAmount =
                    Shopify.formatMoney(compare_price - price, moneyFormat) + " Off";
                if (savingtype == "percent-off") {
                    savingContainer.innerHTML = percentage;
                } else {
                    savingContainer.innerHTML = savedAmount;
                }
                savingContainer.classList.remove("hidden");
            } else {
                savingContainer.classList.add("hidden");
            }
        }
    });
}

function ProductButtonText(productWrapper, selectedVariant, variantInventory) {
    let parentSection = productWrapper;
    var termsConditionCheckbox = "";
    var stickyTermsConditionCheckbox = "";
    if (
        productWrapper
        .closest(".shopify-section")
        .querySelector("[data-sticky-products]")
    ) {
        parentSection = productWrapper.closest(".shopify-section");
    }
    if (productWrapper) {
      termsConditionCheckbox = parentSection.querySelectorAll(
        "[data-terms-conditions]"
      );
    }
    if(document.querySelector('[data-sticky-options]')){
        stickyTermsConditionCheckbox = document.querySelector('[data-sticky-options]');
    }
   
    const selectors = parentSection.querySelectorAll("[data-add-to-cart]");
    Array.from(selectors).forEach(function(cartButton) {
        if (cartButton.classList.contains('bundle-product-button')) return false;
        let cartButtonText = cartButton.querySelector("span");
        if (selectedVariant) {
            if (selectedVariant.available == false) {
                if (cartButtonText) {
                    cartButtonText.innerHTML = soldoutATCText;
                }
                cartButton.setAttribute("disabled", true);
                if (termsConditionCheckbox.length > 0) {
                  termsConditionCheckbox.forEach(function(checkbox){
                    checkbox.style.display = "none";
                    checkbox.querySelector("[data-product-terms]").checked = false;
                  })
                }
            } else {
                if (Shopify.PaymentButton) {
                    Shopify.PaymentButton.init();
                }
                if (cartButtonText) {
                    if (
                        preorderStatus &&
                        variantInventory &&
                        variantInventory.inventory_policy == "continue" &&
                        variantInventory.inventory_quantity <= 0
                    ) {
                        cartButtonText.innerHTML = preorderATCText;
                    } else {
                        cartButtonText.innerHTML = availableATCText;
                    }
                }
                 if (termsConditionCheckbox.length > 0) {
                  termsConditionCheckbox.forEach(function(checkbox){
                    checkbox.style.display = "block";
                    checkbox.querySelector("[data-product-terms]").checked = false;
                    cartButton.setAttribute("disabled", true);
                  
                  })          
                } else {
                  cartButton.removeAttribute("disabled");
                }
            }
        } else {
            if (cartButtonText) {
                cartButtonText.innerHTML = unavailableATCText;
                if (termsConditionCheckbox.length > 0) {
                  termsConditionCheckbox.forEach(function(checkbox){
                    checkbox.style.display = "none";
                    checkbox.querySelector("[data-product-terms]").checked = false;
                  })
                }
            }

            cartButton.setAttribute("disabled", true);
        }
    });
}

function featuredImage(selectedVariant, productWrapper) {
    if (selectedVariant.featured_media) {
        let variantMediaId = selectedVariant.featured_media.id;
        let variantMedia = productWrapper.querySelector(
            "#productmedia-" + variantMediaId
        );
        let mediaParent = productWrapper.querySelector("[data-product-main-media]");
        if (variantMedia && mediaParent) {
            if (mediaParent.classList.contains("flickity-enabled")) {
                let index = Array.from(variantMedia.parentElement.children).indexOf(
                    variantMedia
                );
                let slider = Flickity.data(mediaParent);
                slider.select(index);
            } else {
                let childCount = mediaParent.children.length;
                let firstChild = mediaParent.firstChild;
                if (childCount > 1) {
                    mediaParent.insertBefore(variantMedia, firstChild);
                }
            }
        }
    }
}

function thumbnailChange(section = document) {
    let anchorSelector = 'a.thumbnail_link[href^="#"]';
    let anchorList = section.querySelectorAll(anchorSelector);
    if (anchorList) {
        anchorList.forEach((link) => {
            link.onclick = function(e) {
                e.preventDefault();
                let destination = link
                    .closest("[data-product-media]")
                    .querySelector(this.hash);
                let showMoreButton = document.getElementById("showMoreButton");
                if (destination) {
                    if (destination.classList.contains("hidden-media")) {
                        showMoreButton.click();
                    }
                    if (!isOnScreen(destination)) {
                        destination.scrollIntoView({
                            behavior: "smooth",
                        });
                    }
                }
            };
        });
    }
}

function bundleProductInit(section = document) {
    let bundleWrapper = section.querySelector('[data-product-bundle-wrapper]');
    if (bundleWrapper) {
        let productGrids = bundleWrapper.querySelectorAll('[data-product-grid]');
        Array.from(productGrids).forEach(function(productGrid) {
            let variantElement = productGrid.querySelector('[data-bundle-product-options]');

            if (variantElement) {
                variantElement.addEventListener('change', function() {
                    let selectedOption = variantElement.options[variantElement.selectedIndex];
                    if (selectedOption) {
                        let productId = productGrid.querySelector('.bundle-product-id');
                        if (productId) {
                            productId.value = selectedOption.value;
                        }
                        let actualPrice = productGrid.querySelector('.actual-price');
                        if (actualPrice) {
                            actualPrice.innerHTML = selectedOption.dataset.price;
                        }
                        let comparePrice = productGrid.querySelector('.compare-price');
                        if (comparePrice) {
                            if (selectedOption.dataset.comparePrice) {
                                comparePrice.innerHTML = selectedOption.dataset.comparePrice;
                                comparePrice.classList.remove('hidden');
                            } else {
                                comparePrice.classList.add('hidden');
                            }
                        }
                    }
                })
            }

            let addToBundleBtn = productGrid.querySelector('[data-add-to-bundle]');
            if (addToBundleBtn) {
                addToBundleBtn.addEventListener('click', function() {
                    let productId = productGrid.querySelector('.bundle-product-id');
                    if (productId) {
                        if (addToBundleBtn.classList.contains('active')) {
                            productId.setAttribute('disabled', true)
                            addToBundleBtn.classList.remove('active');
                            addToBundleBtn.innerText = addToBundleBtn.dataset.text;
                        } else {
                            productId.removeAttribute('disabled')
                            addToBundleBtn.innerText = addToBundleBtn.dataset.addedText;
                            addToBundleBtn.classList.add('active')
                        }
                    }
                    setTimeout(() => {
                        let activeProduct = bundleWrapper.querySelectorAll(".bundle-product-id:not([disabled])");
                        let bundleAtc = bundleWrapper.querySelector('[data-add-to-cart]');
                        if (bundleAtc) {
                            if (activeProduct.length > 1) {
                                bundleAtc.removeAttribute('disabled')
                            } else {
                                bundleAtc.setAttribute('disabled', true)
                            }
                        }
                    }, 500);
                });
            }

        })

    }
}
/* Update pickUp availability start */
function pickUpAvialabiliy(parentSection, variant) {
    let pickupSection = parentSection.querySelector("[data-pickup-availability]");
    let pickupContent = parentSection.querySelector(
        "[data-pickup-availability-content]"
    );
    let pickupDrawer = parentSection
        .closest(".shopify-section")
        .querySelector("[data-pickup-location-list]");
    if (pickupSection && pickupContent && pickupDrawer) {
        if (variant != undefined && variant.available == true) {
            var rootUrl = pickupSection.dataset.rootUrl;
            var variantId = variant.id;
            if (!rootUrl.endsWith("/")) {
                rootUrl = rootUrl + "/";
            }
            var variantSectionUrl = `${rootUrl}variants/${variantId}/?section_id=pickup-availability`;
            fetch(variantSectionUrl)
                .then((response) => response.text())
                .then((text) => {
                    var pickupAvailabilityHTML = new DOMParser()
                        .parseFromString(text, "text/html")
                        .querySelector(".shopify-section");
                    let currentVariantPickupContent =
                        pickupAvailabilityHTML.querySelector(
                            "[data-pickup-availability-content]"
                        );
                    let currentVariantPickuplist = pickupAvailabilityHTML.querySelector(
                        "[data-pickup-location-list]"
                    );
                    pickupContent.innerHTML = currentVariantPickupContent ?
                        currentVariantPickupContent.innerHTML :
                        "";
                    pickupDrawer.innerHTML = currentVariantPickuplist ?
                        currentVariantPickuplist.innerHTML :
                        "";
                    if (currentVariantPickupContent.innerHTML != "") {
                        pickupSection.setAttribute("available", "");
                        pickupSection.classList.remove('hidden');
                        pickupDrawer.classList.remove('hidden');
                    } else {
                        pickupSection.removeAttribute("available");
                    }
                    SidedrawerEventInit(parentSection);
                })
                .catch((e) => {});
        } else {
            pickupContent.innerHTML = "";
            pickupDrawer.innerHTML = "";
            pickupSection.removeAttribute("available");
        }
    }
}

// end variant selector

function SidedrawerEventInit(section = document) {
    let sideDraweropenElements = section.querySelectorAll("[data-side-drawer-open]");
    Array.from(sideDraweropenElements).forEach(function(element) {
        element.addEventListener("click", (event) => {
            event.preventDefault();
            if (section.classList && section.classList.contains("product__wrapper")) {
                section = section.closest(".shopify-section");
            }
            
            let drawerElement = element.getAttribute("href");
            let sideDrawer = section.querySelector(drawerElement);
            if (element.classList.contains('header-contact') || element.classList.contains('need-help-text')) {
                sideDrawer = document.querySelector(drawerElement);
            }
            if (sideDrawer) {
                let recommendProducts = sideDrawer.querySelector(
                    "[data-recommendation-popup]"
                );
                if (sideDrawer.classList.contains("popup")) {
                    sideDrawer.style.display = "flex";
                    setTimeout(() => {
                        sideDrawer.classList.add("popup-visible");
                    }, 300);

                    if (sideDrawer.getAttribute("id") == "product-fetured-media-popup") {
                        let meidaIdIndex = element.getAttribute("data-index");
                        let sliderELement = sideDrawer.querySelector("[data-slideshow]");
                        if (sliderELement.classList.contains("flickity-enabled")) {
                            slideshowInit(sliderELement);
                        }
                        let flkty = Flickity.data(sliderELement);

                        if (flkty) {
                            if (flkty.selectedElements.length >= flkty.cells.length) {
                                sliderELement.classList.add("disable-arrows");
                                flkty.options.draggable = false;
                                flkty.updateDraggable();
                            } else {
                                flkty.options.draggable = true;
                                flkty.updateDraggable();
                                sliderELement.classList.remove("disable-arrows");
                            }
                            flkty.resize();

                            flkty.select(meidaIdIndex);
                        }
                    }
                } else {
                    sideDrawer.style.display = "flex";
                      if(element.classList.contains("search")){
                       const searchDrawercheck = sideDrawer.querySelector("[data-search-drawer]");
                      if(searchDrawercheck){  
                       searchDrawercheck.classList.remove("hidden");
                      }
                    }
                    setTimeout(() => {
                        sideDrawer.classList.add("sidebar-visible");
                    }, 300);
                    
                    if (recommendProducts && !recommendProducts.classList.contains("active")) {
                        setTimeout(() => {
                            recommendProducts.classList.add("active");
                        }, 1000);
                        slideshowElements();
                    }
                } 
                setTimeout(() => {
                    focusElementsRotation(sideDrawer);
                }, 1000);
                if(element.classList.contains("search")){
                    document.querySelector("body").classList.add("search-drawer-open"); 
                     let searchDrawer = document.querySelector("[data-search-drawer]");
                    searchDrawer.classList.remove("hidden");
                    let searchInput = searchDrawer.querySelector("input[data-search-input]");
                    if (searchInput) {
                        setTimeout(() => {
                            searchInput.focus();
                        }, 1000); 
                    }
                }
                document.querySelector("body").classList.add("no-scroll");
                document.querySelector("body").classList.add("popup-open");
            }
        });
    });

    let sideDrawercloseElements = section.querySelectorAll(
        "[data-side-drawer-close]"
    );
    Array.from(sideDrawercloseElements).forEach(function(element) {
        element.addEventListener("click", (event) => {
            event.preventDefault();

            let sideDrawer = element.closest("[data-side-drawer]");
            let recommendProducts;
            if (element.closest("[data-side-drawer]")) {
                recommendProducts = element
                    .closest("[data-side-drawer]")
                    .querySelector("[data-recommendation-popup]");
            }
            if(recommendProducts){
                if(element.closest(".side-drawer ").classList.contains("side-search-drawer")){
                    document.querySelector("body").classList.remove("search-drawer-open"); 
                }
            }
            if (sideDrawer) {
                if (
                    recommendProducts &&
                    recommendProducts.querySelector(".cart-recommandation-popup-inner") &&
                    recommendProducts.classList.contains("active")
                ) {
                    setTimeout(function() {
                        recommendProducts.classList.remove("active");
                    }, 200);
                    setTimeout(function() {
                        sideDrawer.classList.remove("sidebar-visible", "popup-visible");
                        document.querySelector("body").classList.remove("no-scroll");
                        document.querySelector("body").classList.remove("popup-open");
                    }, 1000);
                    setTimeout(function() {
                        sideDrawer.style.display = "flex";
                    }, 500);
                    setTimeout(function() {
                        sideDrawer.style.display = "none";
                    }, 1500);
                } else {
                    setTimeout(function() {
                        sideDrawer.style.display = "none";
                    }, 500);
                    sideDrawer.classList.remove("sidebar-visible", "popup-visible");
                    document.querySelector("body").classList.remove("no-scroll");
                    document.querySelector("body").classList.remove("popup-open");
                }

                sideDrawer.querySelectorAll("video").forEach((video) => {
                    video.muted = true;
                });
                sideDrawer.querySelectorAll("[data-video-audio]").forEach((element) => {
                    element.classList.remove("active");
                });

                stopFocusRotation();
                if (previousFocusElement) {
                    previousFocusElement.focus();
                }
                previousFocusElement = "";
                if (sideDrawer.classList.contains("address-sidebar")) {
                    let addressForm = sideDrawer.querySelector("form");
                    if (addressForm) {
                        addressForm.reset();
                    }
                }
            }
        });
    });
}

function get_header_height() {
    let headerHeight = document.querySelector("[data-header-section]");
    document
        .querySelector("body")
        .style.setProperty("--dynamicheaderHeight", "0px");
    // document.querySelector("body").style = `--dynamicheaderHeight:0px`;
    if (headerHeight) {
        let stickyType = headerHeight.closest(".main-header");
        if (stickyType.classList.contains("sticky-header")) {
            // document.querySelector("body").style = `--headerHeight:${headerHeight.offsetHeight}px`;
            document
                .querySelector("body")
                .style.setProperty("--headerHeight", `${stickyType.offsetHeight}px`);
            let dynamicHeaderHeight = stickyType
                .getBoundingClientRect()
                .height.toFixed(2);
            document
                .querySelector("body")
                .style.setProperty("--dynamicheaderHeight", `${dynamicHeaderHeight}px`);
        } else {
            document
                .querySelector("body")
                .style.setProperty("--headerHeight", `${stickyType.offsetHeight}px`);
        }
        window.addEventListener("resize", function() {
            setTimeout(function() {
                let stickyType = headerHeight.closest(".main-header");
                let headerHeightset = stickyType.getBoundingClientRect().height;
                if (stickyType.classList.contains("sticky-header")) {
                    document
                        .querySelector("body")
                        .style.setProperty("--headerHeight", `${headerHeightset}px`);
                } else {
                    document
                        .querySelector("body")
                        .style.setProperty("--headerHeight", `${headerHeightset}px`);
                }
            }, 500);
        });
    }
}

function quickviewElements(section = document) {
    let quickviewElements = section.querySelectorAll("[data-quick-view]");
    Array.from(quickviewElements).forEach(function(element) {
        initQuickviewAction(element);
    });
}

function initQuickviewAction(element) {
    element.addEventListener("click", (event) => {
        event.preventDefault();
        var _url = element.getAttribute("href");
        if (_url.indexOf("?") > -1) {
            _url = _url.split("?");
            _url = _url[0];
        }
        var productUrl = _url + "?section_id=product-quick-view";
        let popContainer = document.querySelector(".quickview-drawer");
        popContainer.querySelector(".quickview-drawer-content").innerHTML =
            preLoadLoadGif;
        element.classList.add("disabled");

        setTimeout(function() {
            document
                .querySelector(".quickview-drawer")
                .classList.add("sidebar-visible");
        }, 300);

        document.querySelector(".quickview-drawer").style.display = "flex";
        document.querySelector("body").classList.add("no-scroll");

        fetch(productUrl)
            .then((response) => response.text())
            .then((text) => {
                var sectionParent = new DOMParser()
                    .parseFromString(text, "text/html")
                    .querySelector(".shopify-section");
                var sectionInnerHTML = sectionParent.querySelector(
                    ".quickview-drawer-content"
                );
                if (popContainer) {
                    // setTimeout(function () {
                    popContainer.querySelector(".quickview-drawer-content").innerHTML =
                        sectionInnerHTML.innerHTML;
                    setTimeout(function() {
                        document.querySelector("body").classList.add("no-scroll");
                        onloadVariants(popContainer);
                        variant_selector(popContainer);
                        getATCelement();
                        if (Shopify.PaymentButton) {
                            Shopify.PaymentButton.init();
                        }
                        slideshowElements(popContainer);
                        getQuantityElement(popContainer);
                        focusElementsRotation(popContainer);
                        element.classList.remove("disabled");
                        SidedrawerEventInit();
                        customSliderArrowsEvents(popContainer);
                        addMultiplier();
                        outSideClickTrigger(popContainer);
                    }, 500);
                    // }, 1000);
                }
                productTermhandler();
            })
            .catch((e) => {});
    });
}

function accordion() {
    var acc = document.querySelectorAll("[data-collapsible-content]");
    var i;

    for (i = 0; i < acc.length; i++) {
        acc[i].addEventListener("click", function() {
            this.classList.toggle("active");
            var panel = this.nextElementSibling;
            if (panel.style.maxHeight) {
                panel.style.maxHeight = null;
            } else {
                panel.style.maxHeight = panel.scrollHeight + "px";
            }
        });
    }
    let get = document.querySelector(".modal__close-button");
    if (get) {
        get.addEventListener("click", function() {
            this.closest(".announcement-bar--content")
                .querySelector(".active")
                .classList.remove("active");
            this.closest(".announcement-collapsible-content").style.maxHeight = null;
        });
    }
}

function lookbook(section = document) {
    let active = section.querySelectorAll(".hotspot-dot");
    Array.from(active).forEach(function(active) {
        active.addEventListener("click", function(e) {
            e.preventDefault();
            let current = section.querySelectorAll(".product-hotspot.active");
            active.parentElement.classList.add("active");
            Array.from(current).forEach(function(activeMenu) {
                if (activeMenu.classList.contains("active")) {
                    activeMenu.classList.remove("active");
                }
            });
        });
    });
}

function marqueeTextAutoplay(section = document) {
    let marqueeElements = section.querySelectorAll("[data-marquee]");
    Array.from(marqueeElements).forEach((element) => {
        if (!element.querySelector("[data-marque-node]")) return false;
        let resizedMobile = false;
        let resizedDesktop = false;
        marqueeTextAutoplayInit(element);
        window.addEventListener("resize", function() {
            if (window.innerWidth > 767 && resizedDesktop == false) {
                marqueeTextAutoplayInit(element);
                resizedDesktop = true;
                resizedMobile = false;
            } else if (window.innerWidth < 768 && resizedMobile == false) {
                marqueeTextAutoplayInit(element);
                resizedMobile = true;
                resizedDesktop = true;
            }
        });
    });
}

function marqueeTextAutoplayInit(element) {
    let scrollingSpeed = parseInt(
        element.getAttribute("data-marquee-speed") || 15
    );
    if (
        window.innerWidth < 768 &&
        element.hasAttribute("data-marquee-speed-mobile")
    ) {
        scrollingSpeed = parseInt(
            element.getAttribute("data-marquee-speed-mobile")
        );
    }
    const contentWidth = element.clientWidth,
        node = element.querySelector("[data-marque-node]"),
        nodeWidth = node.clientWidth;
    let slowFactor = 1 + (Math.max(1600, contentWidth) - 375) / (1600 - 375);
    element.parentElement.style.setProperty(
        "--marqueeSpeed",
        `${((scrollingSpeed * slowFactor * nodeWidth) / contentWidth).toFixed(3)}s`
    );
}

function count_number(number) {
    return (number < 10 ? "0" : "") + number;
}

function countDownInit(element) {
    const second = 1000,
        minute = second * 60,
        hour = minute * 60,
        day = hour * 24,
        year = day * 365;
    var clearCountDown;
    clearCountDown = setInterval(function() {
        let days = element.querySelector(".days");
        let lowest_price = element.closest(".lowest-price-offer");
        let saleParent = element.closest("[data-counter-sale]");
        // let count_days = element.querySelector(".count-days .separator");
        // let day1 = "day";
        let hours = element.querySelector(".hours");
        let minutes = element.querySelector(".minutes");
        let seconds = element.querySelector(".seconds");
        let launch_date = element.getAttribute("data-launch-date");
        if (launch_date == undefined || launch_date == "") {
            return false;
        }
        let countDown = new Date(launch_date).getTime();
        let now = new Date().getTime();
        let distance = countDown - now;
        let days_text = count_number(Math.floor(distance / day));
        days.innerText = days_text;
        let hours_text = count_number(Math.floor((distance % day) / hour));
        hours.innerText = hours_text;
        let minutes_text = count_number(Math.floor((distance % hour) / minute));
        minutes.innerText = minutes_text;
        let seconds_text = count_number(Math.floor((distance % minute) / second)); 
        seconds.innerText = seconds_text;
        let cardClosest = element.closest(".product-card");
        if (cardClosest) {
            cardClosest.querySelector("[data-countdown-timer]").style.display =
                "block";
        }
        if (distance < 0) {
            clearInterval(clearCountDown);
            element.style.display = "none";
            if (lowest_price) {
                lowest_price.style.display = "none";
            }
            if (saleParent) {
                saleParent.style.display = "none";
            }
        } else {
            if (saleParent) {
                saleParent.style.display = "block";
            }
        }
    }, 1000);
}

function getCountDownElments(section = document) {
    let countDownElements = section.querySelectorAll("[data-countdown-timer]");
    Array.from(countDownElements).forEach(function(element) {
        countDownInit(element);
    });
}

function vertical_scroll(section = document) {
    let carouselElements = section.querySelectorAll("[data-carousal-container]");

    Array.from(carouselElements).forEach(function(carousel) {
        let slideButtons = carousel.querySelectorAll(".button_selector");
        let sectionCarousal = carousel.querySelector("[data-carousal]");
        let slidesSpeed = sectionCarousal.getAttribute("data-speed");
        Array.from(slideButtons).forEach(function(element) {
            element.addEventListener("click", function(e) {
                e.preventDefault();
                let current = carousel.querySelector(".button_selector.selected");
                let button_index = element.getAttribute("data-index");
                let top = -carousel.offsetHeight * button_index;
                if (current) {
                    current.classList.remove("selected");
                }
                element.classList.add("selected");
                sectionCarousal.style.top = top + "px";
            });
        });
        if (slidesSpeed) {
            autoplay_slides(carousel);
        }
    });
}

function autoplay_slides(carousel) {
    let slideIndex = 0;
    showSlides();

    function showSlides() {
        let i;
        let slides = carousel.getElementsByClassName("image-with-text-content");
        let dots = carousel.getElementsByClassName("dot");
        let sectionCarousal = carousel.querySelector("[data-carousal]");
        let slidesSpeed = sectionCarousal.getAttribute("data-speed");
        if (slidesSpeed) {
            for (i = 0; i < slides.length; i++) {
                slides[i].style.display = "none";
            }
            slideIndex++;
            if (slideIndex > slides.length) {
                slideIndex = 1;
            }
            for (i = 0; i < dots.length; i++) {
                dots[i].className = dots[i].className.replace("selected", "");
            }
            slides[slideIndex - 1].style.display = "block";
            dots[slideIndex - 1].className += "selected";
            setTimeout(showSlides, slidesSpeed);
        }
    }
}

function getcollageElments(section = document) {
    let collageElements = section.querySelectorAll("[data-testimonial-collage]");
    Array.from(collageElements).forEach(function(element) {
        testimonial_collage(element);
    });
}

function testimonial_collage(element) {
    let bigItem = element.querySelectorAll(".testimonial-item");
    let smallItemWrapper = element.querySelectorAll(".testimonial-logo-wrapper");
    Array.from(bigItem).forEach(function(bigItem) {
        let bigItemAttribute = bigItem.getAttribute("data-index");
        Array.from(smallItemWrapper).forEach(function(Itemsmall) {
            let small_item_hover = Itemsmall.querySelectorAll(
                ".testimonial-logo-holder"
            );
            Array.from(small_item_hover).forEach(function(smallItem) {
                smallItem.addEventListener("mouseover", function() {
                    let smallItemAttribute = smallItem.getAttribute("data-index");
                    if (smallItem.classList.contains("active")) {
                        return false;
                    }
                    active_collage_image(element);
                    if (bigItemAttribute == smallItemAttribute) {
                        smallItem.classList.add("active");
                        bigItem.classList.add("active");
                    }
                });
            });
        });
    });
}

function active_collage_image(element) {
    let _currentActive = element.querySelector(".testimonial-logo-holder.active");
    let _currentActiveItem = element.querySelector(".testimonial-item.active");
    if (_currentActive && _currentActiveItem) {
        _currentActive.classList.remove("active");
        _currentActiveItem.classList.remove("active");
    }
}

function tab_media_item() {
    let elements = document.querySelectorAll("[data-tab-media]");
    let dataIndex = "";
    if (elements) {
        Array.from(elements).forEach(function(element) {
            element.addEventListener("click", function(event) {
                if (element.classList.contains("active")) return false;
                let parent = element.closest(".shopify-section");
                dataIndex = element.getAttribute("data-index");
                closeVideoMedia(parent, false);
                let currentActiveTab = parent.querySelector("[data-tab-media].active");
                if (currentActiveTab) {
                    currentActiveTab.classList.remove("active", "left", "right");
                }
                elements.forEach(function(innerelement, index) {
                    innerelement.classList.remove("left", "right");
                    if (dataIndex > index) {
                        innerelement.classList.add("left");
                    } else {
                        innerelement.classList.add("right");
                    }
                });
                element.classList.add("active");
            });
        });
    }
}

function initStoreLocator(section = document) {
    if(googleMapApiKey != '' && googleMapId != '' ){
        const script = document.createElement("script");
        script.src ="https://maps.googleapis.com/maps/api/js?key="+googleMapApiKey+"&loading=async&callback=initStoreMap&v=weekly&libraries=marker";
        script.async = true;
        script.defer = true;
        document.body.appendChild(script);
    }
   
}
// Initialize store locator

async function getGeoDetails(geocoder, address) {
    let getAddress = new Promise(function(resolve, reject) {
        geocoder.geocode({
                address: address,
            },
            function(results, status) {
                if (status === "OK") {
                    resolve([
                        results[0].geometry.location.lat(),
                        results[0].geometry.location.lng(),
                    ]);
                } else {
                    reject(new Error("Couldnt't find the location " + address));
                }
            }
        );
    });
    return await getAddress;
}

 async  function initStoreMap(section = document) {
    let storeLocatorItems = section.querySelectorAll("[data-store-locator-map]");
    const { Map } = await google.maps.importLibrary("maps");
    const {AdvancedMarkerElement} = await google.maps.importLibrary("marker");
    Array.from(storeLocatorItems).forEach(function(mapSelector) {
      
            let geocoder = new google.maps.Geocoder();
            const storeLocatorItems = mapSelector
                .closest(".shopify-section")
                .querySelectorAll("[data-store-locator]");
            if (storeLocatorItems.length == 0) {
                return false;
            }
           
            const map = new Map(mapSelector, {
                center: {
                    lat: 0,
                    lng: 0,
                },
                zoom: 8,
                mapId: googleMapId
            });
            const markers = [];
            function updateMap (latitude, longitude){
                map.setCenter({
                    lat: latitude,
                    lng: longitude,
                });
                map.setZoom(15);
                const position = {
                    lat: latitude,
                    lng: longitude,
                };
                const marker =  new AdvancedMarkerElement({
                    position: position,
                    map: map
                });
               
                markers.push(marker);
            };

            let activeItem = mapSelector
                .closest(".shopify-section")
                .querySelector("[data-store-locator].active");

            if (!activeItem) {
                activeItem = mapSelector
                    .closest(".shopify-section")
                    .querySelector("[data-store-locator]");
            }

            let address = activeItem.getAttribute("data-address");
            let geoDetail = getGeoDetails(geocoder, address);
            geoDetail.then(function(address) {
                if (geoDetail != null) {
                    updateMap(address[0], address[1]);
                }
            });
            storeLocatorItems.forEach((item) => {
                item.addEventListener("click", () => {
                    const storeName = item.getAttribute("data-label");
                    let address = item.getAttribute("data-address");
                    storeLocatorItems.forEach((sibling) => {
                        if (sibling !== item) {
                            sibling.classList.remove("active");
                        }
                    });

                    item.classList.add("active");
                    let geoDetail = getGeoDetails(geocoder, address);
                    geoDetail.then(function(address) {
                        if (geoDetail != null) {
                            updateMap(address[0], address[1]);
                        }
                    });
                });
            });
 
    });
}
// Collapsible content
function getAllDetails(section = document) {
    var details = section.querySelectorAll("details");
    Array.from(details).forEach(function(detail) {
        detailsInit(detail);
    });
}

function detailsInit(detail) {
    let detailParent = detail.closest("[data-accordion-details]");
    if (!detailParent) return false;
    let parentElement = detailParent.closest(".collapsible-content-section");
    let getOpenattribute = "";
    if (parentElement) {
        let detailParentstyle = parentElement.querySelector("[data-open-style]");
        getOpenattribute = detailParentstyle.getAttribute("data-open");
    }
    let others = detailParent.querySelectorAll("details");
    detail.addEventListener("click", (event) => {
        if (detail.open) {
            others.forEach((other) => {
                if (other !== detail) {
                    other.removeAttribute("open");
                }
            });
        }
    });
}

class Accordion {
    constructor(el) {
        this.el = el;
        this.summary = el.querySelector("summary");
        this.content = el.querySelector(".detail-expand");
        this.animation = null;
        this.isClosing = false;
        this.isExpanding = false;
        this.summary.addEventListener("click", (e) => this.onClick(e));
    }

    onClick(e) {
        e.preventDefault();

        this.el.style.overflow = "hidden";

        if (this.isClosing || !this.el.open) {
            this.open();
        } else if (this.isExpanding || this.el.open) {
            this.shrink();
        }
    }

    shrink() {
        this.isClosing = true;
        const startHeight = `${this.el.offsetHeight}px`;
        const endHeight = `${this.summary.offsetHeight}px`;
        if (this.animation) {
            this.animation.cancel();
        }
        // Start a WAAPI animation
        this.animation = this.el.animate({
            height: [startHeight, endHeight],
        }, {
            duration: 400,
            easing: "ease-out",
        });

        // When the animation is complete, call onAnimationFinish()
        this.animation.onfinish = () => this.onAnimationFinish(false);
        this.animation.oncancel = () => (this.isClosing = false);
    }
    open() {
        this.el.style.height = `${this.el.offsetHeight}px`;
        this.el.open = true;
        window.requestAnimationFrame(() => this.expand());
    }

    expand() {
        // Set the element as "being expanding"
        this.isExpanding = true;
        const startHeight = `${this.el.offsetHeight}px`;
        const endHeight = `${
      this.summary.offsetHeight + this.content.offsetHeight
    }px`;

        if (this.animation) {
            this.animation.cancel();
        }
        this.animation = this.el.animate({
            height: [startHeight, endHeight],
        }, {
            duration: 400,
            easing: "ease-out",
        });
        this.animation.onfinish = () => this.onAnimationFinish(true);
        this.animation.oncancel = () => (this.isExpanding = false);
    }

    onAnimationFinish(open) {
        this.el.open = open;
        this.animation = null;
        this.isClosing = false;
        this.isExpanding = false;
        this.el.style.height = this.el.style.overflow = "";
    }
}

function detailDisclouserInit(section = document) {
    let detailsElements = section.querySelectorAll("[data-accordion-open]");
    if (detailsElements) {
        Array.from(detailsElements).forEach((detailsElement) => {
            new Accordion(detailsElement);
        });
    }
}

function videoBanner() {
    var documentScrollTop = document.documentElement.scrollTop;
    var imgbg = document.querySelector("[data-video-banner]");
    let limit = 3.3;
    let increment = 0;
    let radius = 20;
    let radiusincrement = 0;
    if (!imgbg) return false;
    window.addEventListener("scroll", function() {
        if (isOnScreen(imgbg)) {
            increment = increment + 0.1;
            radiusincrement = radiusincrement + 1;
            if (documentScrollTop < document.documentElement.scrollTop) {}
        } else {
            if (documentScrollTop > document.documentElement.scrollTop) {}
        }
        documentScrollTop = document.documentElement.scrollTop;
    });
}

function initHotspot(section = document) {
    let hotspotId = section.querySelectorAll("[data-hotspot-dot]");
    let crossProduct = section.querySelectorAll(".product-cross-icon");
    if (crossProduct) {
        Array.from(crossProduct).forEach((crossproduct) => {
            crossproduct.addEventListener("click", function(e) {
                e.preventDefault();
                crossproduct
                    .closest(".hotspot-product-main-inner.active")
                    .classList.remove("active");
                crossproduct
                    .closest(".hotspot-item")
                    .querySelector("[data-hotspot-dot].active")
                    .classList.remove("active");
            });
        });
    }
    if (hotspotId) {
        Array.from(hotspotId).forEach((product) => {
            product.addEventListener("click", function(event) {
                event.preventDefault();
                if (this.classList.contains("active")) {
                    this.classList.remove("active");
                    this.closest(".hotspot-item")
                        .querySelector(".hotspot-product-main-inner.active")
                        .classList.remove("active");
                    return false;
                }

                let dataProduct = this.getAttribute("data-product");
                let dataProductId = this.closest(".hotspot-item").querySelector(
                    '.hotspot-product-main-inner[data-id="' + dataProduct + '"]'
                );

                if (
                    this.closest("[data-hotspot-buttons]").querySelector(
                        "[data-hotspot-dot].active"
                    ) &&
                    this.closest(".hotspot-item").querySelector(
                        ".hotspot-product-main-inner.active"
                    )
                ) {
                    product
                        .closest("[data-hotspot-buttons]")
                        .querySelector("[data-hotspot-dot].active")
                        .classList.remove("active");
                    this.closest(".hotspot-item")
                        .querySelector(".hotspot-product-main-inner.active")
                        .classList.remove("active");
                }
                if (dataProductId) {
                    let productsContainer = dataProductId.closest(
                        ".hotspot-product-main"
                    );
                    let currentActiveProduct = productsContainer.querySelector(
                        ".hotspot-product-main-inner"
                    );
                    if (currentActiveProduct) {
                        dataProductId.classList.add("active");
                    }
                }

                let hotspotContainer = this.closest(".hotspot-item");
                let currentActiveHotspot =
                    hotspotContainer.querySelector("[data-hotspot-dot]");
                if (currentActiveHotspot) {
                    this.classList.add("active");
                }
            });
        });
    }
}

function detect_active_testimonial() {
    // get active
    var get_active = $("#testimonial-cards .testimonial-item:first-child").data(
        "class"
    );
    $("#testimonial-dots li").removeClass("active");
    $("#testimonial-dots li[data-class=" + get_active + "]").addClass("active");
}

function testimonialInit() {
    $("#testimonial-dots li").click(function() {
        $("#testimonial-dots li").removeClass("active");
        $(this).addClass("active");
        var get_slide = $(this).attr("data-class");
        $("#testimonial-cards .testimonial-item[data-class=" + get_slide + "]")
            .hide()
            .prependTo("#testimonial-cards")
            .fadeIn();
        $.each($(".testimonial-item"), function(index, dp_item) {
            // var item_height = $(dp_item).height();
            // $('.testimonial-slides').css('height',item_height+30);
            $(dp_item).attr("data-position", index + 1);
        });
        detect_active_testimonial();
    });
    let divElement = document.querySelector(".testimonial-slides");
    if (divElement) {
        let maxHeight = divElement.children[0].children[1].clientHeight;
        let elemRect = divElement.getBoundingClientRect;
        let elemHeight = elemRect.clientHeight;
        divElement.style.height = maxHeight + "px";
    }
}



function collectionCarousal() {
    $(".collection-carousel-item.hover-effect").hover(
        function() {
            $(this)
                .closest(".collection-carousel-wrapper")
                .find(".collection-carousel-item")
                .addClass("sibling");
            $(this).removeClass("sibling");
        },
        function() {
            $(".collection-carousel-item").removeClass("sibling");
        }
    );
}

// Product recommendation start
function productRecommendations() {
    const productRecommendationsSections = document.querySelectorAll(
        "[product-recommendations]"
    );
    Array.from(productRecommendationsSections).forEach(function(
        productRecommendationsSection
    ) {
        productRecommendationsInit(productRecommendationsSection);
    });
}

function productRecommendationsInit(productRecommendationsSection) {
    const url = productRecommendationsSection.dataset.url;

    fetch(url)
        .then((response) => response.text())
        .then((text) => {
            const html = document.createElement("div");
            html.innerHTML = text;
            const recommendations = html.querySelector("[product-recommendations]");
            if (recommendations && recommendations.innerHTML.trim().length) {
                productRecommendationsSection.innerHTML = recommendations.innerHTML;
                productRecommendationsSection.closest(
                    ".shopify-section"
                ).style.display = "block";
                let slider =
                    productRecommendationsSection.querySelector("[data-slideshow]");
                if (slider) {
                    slideshowElements(productRecommendationsSection);
                }
                quickviewElements(productRecommendationsSection);
                getCountDownElments(productRecommendationsSection);

                collectionSwatch(productRecommendationsSection);
                customSliderArrowsEvents(productRecommendationsSection);
                productCardHoverInit(productRecommendationsSection);
                badgesAnimation(productRecommendationsSection);
                if (aosAnimation) {
                    if (AOS) {
                        AOS.refreshHard();
                    }
                }
            }
        })
        .catch((e) => {
            console.error(e);
        });
}
// Product recommendation end
// Recently viewed products
function recentlyViewedProducts() {
    let rvpWrappers = document.querySelectorAll("[data-recent-viewed-products]");
    Array.from(rvpWrappers).forEach(function(rvp) {
        let currentProduct = parseInt(rvp.dataset.product);
        let section = rvp.closest(".shopify-section");
        let cookieName = "starlite-recently-viewed-products";
        let rvProducts = JSON.parse(window.localStorage.getItem(cookieName) || "[]");
        if (!isNaN(currentProduct)) {
            if (!rvProducts.includes(currentProduct)) {
                rvProducts.unshift(currentProduct);
            }
            window.localStorage.setItem(
                cookieName,
                JSON.stringify(rvProducts.slice(0, 14))
            );

            if (rvProducts.includes(parseInt(currentProduct))) {
                rvProducts.splice(rvProducts.indexOf(parseInt(currentProduct)), 1);
            }
        }
        let currentItems = rvProducts
            .map((item) => "id:" + item)
            .slice(0, 14)
            .join(" OR ");
        fetch(rvp.dataset.section + currentItems)
            .then((response) => response.text())
            .then((text) => {
                const html = document.createElement("div");
                html.innerHTML = text;
                const recents = html.querySelector("[data-recent-viewed-products]");
                if (recents && recents.innerHTML.trim().length) {
                    rvp.innerHTML = recents.innerHTML;
                    if (recents.innerHTML != '') {
                        rvp.closest(".shopify-section").classList.remove("hidden");
                    }

                    let slider = section.querySelector("[data-slideshow]");
                    if (slider) {
                        slideshowElements(section);
                    }
                    quickviewElements(section);
                    getCountDownElments(section);
                    collectionSwatch(section);
                    productCardHoverInit(section);
                    customSliderArrowsEvents(section);
                    badgesAnimation(section);
                    if (aosAnimation) {
                        if (AOS) {
                            AOS.refreshHard();
                        }
                    }
                }
            })
            .catch((e) => {
                console.error(e);
            });
    });
}
//end
var tag = document.createElement("script");
tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName("script")[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
ytApiLoaded = true;

function onYouTubeIframeAPIReady() {
    let youTubeVideos = document.querySelectorAll(".youtubeVideo");
    Array.from(youTubeVideos).forEach(function(video) {
        let divId = video.getAttribute("id");
        let vidId = video.getAttribute("data-id");
        //creates the player object
        // let ik_player = new YT.Player(divId);
        // //subscribe to events
        // ik_player.addEventListener("onReady", "onYouTubePlayerReady");
        // ik_player.addEventListener("onStateChange", "onYouTubePlayerStateChange");
        let player = new YT.Player(divId, {
            videoId: vidId,
            playerVars: {
                showinfo: 0,
                controls: 0,
                fs: 0,
                rel: 0,
                height: "100%",
                width: "100%",
                iv_load_policy: 3,
                html5: 1,
                loop: 1,
                autoplay: 1,
                playsinline: 1,
                modestbranding: 1,
                disablekb: 1,
                showinfo: 0,
                wmode: "opaque",
            },
            events: {
                onReady: onYouTubePlayerReady,
                onStateChange: onYouTubePlayerStateChange,
            },
        });
    });
}

function onYouTubePlayerReady(event) {
    event.target.mute();
    event.target.playVideo();
}

function onYouTubePlayerStateChange(event) {
    if (event.data == 1) {
        let deferredParent = event.target.g.closest('deferred-media');
        if (deferredParent) {
            let placeholderMedia = deferredParent.querySelector(".deferred-media-placeholder");
            if (placeholderMedia) {
                placeholderMedia.style.display = 'none';
            }
        }
    }
    if (event.data == 0) {
        event.target.playVideo();
    } else {
        closeVideoMedia();
    }
}

function mp4VideoReady() {
    document.querySelectorAll("video").forEach(function(video) {
        video.onplay = function() {
            closeVideoMedia();
        };
    });
}

function vimeoVideoReady(section = document) {
    section.querySelectorAll(".sr-vimeo-video").forEach(function(video) {
        let divId = video.getAttribute("id");
        let player = new Vimeo.Player(divId);
        player.on("play", function() {
            closeVideoMedia();
        });
    });
}

function customDropdownElements(section = document) {
    let customDropdowns = section.querySelectorAll(".detail-box");
    Array.from(customDropdowns).forEach(function (dropdown) {
        let dropdownButton = dropdown.querySelector(".detail-summary");
        if (dropdownButton) {
            dropdownButton.addEventListener("click", (event) => {
                event.preventDefault();
                
                let customSelectContent = dropdownButton.nextElementSibling;
                let customSelectList = customSelectContent
                    ? customSelectContent.querySelector(".custom-select-list")
                    : null;

                if (customSelectList && customSelectList.children.length === 0) {
                    fetch(window.Shopify.routes.root + "?section_id=country-list")
                        .then((response) => response.text())
                        .then((responseText) => {
                            let resultsMarkup = new DOMParser().parseFromString(responseText, "text/html");
                            customSelectList.innerHTML = resultsMarkup.querySelector("#shopify-section-country-list").innerHTML;
                        });
                }

                dropdown.classList.toggle("active");
                DOMAnimations.slideToggle(dropdown.querySelector(".detail-expand"), 300);
            });

            dropdown.onkeydown = function (e) {
                if (dropdownButton.tagName !== "BUTTON") {
                    if (e.keyCode === 13 || e.keyCode === 32) {
                        dropdownButton.click();
                    }
                }
            };
        }

        let dropdownContent = dropdown.querySelector(".detail-expand");
        if (dropdownContent) {
            dropdownContent.addEventListener("click", (event) => {
                dropdown.classList.remove("active");
                DOMAnimations.slideUp(dropdown.querySelector(".detail-expand"), 300);
            });
        }

        document.addEventListener("click", function (event) {
            let element = event.target;
            if (dropdown.contains(element) || element === dropdown) {
                return false;
            } else {
                if (dropdown.classList.contains("active")) {
                    dropdown.classList.remove("active");
                    DOMAnimations.slideUp(dropdown.querySelector(".detail-expand"), 300);
                }
            }
        });
    });
}

function onHoverMenuElements(section = document) {
    let onHoverMenuItems = section.querySelectorAll(
        ".categories-submenu-item"
    );
    Array.from(onHoverMenuItems).forEach(function(menuElement) {
        menuElement.addEventListener("mouseover", () => {
            Array.from(section.querySelectorAll(".categories-inner--submenu")).forEach(function(element) {
                if (menuElement.classList.contains("sub-category-menu")) {
                    let index = menuElement.dataset.index;
                    let contentElement = document.querySelector(".sub-category-menu-content-" + index);
                    if (contentElement == element) {
                        element.classList.remove("hidden");
                    } else {
                        element.classList.add("hidden");
                    }
                } else {
                    //element.classList.add("hidden");
                }
                
            });
            if(menuElement.classList.contains('active')) return;
            
            Array.from(menuElement.closest('ul').querySelectorAll('.categories-submenu-item')).map((item) => {
                item.classList.remove('active');
            });
            menuElement.classList.add('active')
            if(menuElement.querySelector('.categories-inner--submenu')){
                const menuSecondLevelHeight = menuElement.querySelector('.categories-inner--submenu').getBoundingClientRect().height
                menuElement.closest('.header-categories-wrapper').style.setProperty('--category-height', `${menuSecondLevelHeight}px`)
            }
        });
        
    });
    let onHoverMainNavElements = section.querySelectorAll(
        ".custom-details-disclosure"
    );
    Array.from(onHoverMainNavElements).forEach(function(navElement) {

        navElement.addEventListener("mouseover", () => {
            // let delay = 0.1;
            if (navElement.classList.contains('open')) return false;

            if (navElement.parentElement.classList.contains("has-children")) {
                document.querySelector("body").classList.add("megamenu-open");
                // let childelements = navElement.querySelectorAll(".custom-details-disclosure.open .nav-submenu li");
                // Array.from(childelements).forEach(function(childelement){
                //   childelement.style.transitionDelay  = delay +'s';
                //     delay=delay+0.1;
                // })
            }
            // Array.from(
            //     document.querySelectorAll("[data-search-input]")
            // ).forEach(function(element) {
            //     element.value = '';
            // });
            Array.from(
                document.querySelectorAll("[data-result-container]")
            ).forEach(function(element) {
                element.classList.add('hidden');
            });
            Array.from(
                document.querySelectorAll("[data-search-drawer]")
            ).forEach(function(element) {
                element.classList.add('hidden');
                element.classList.remove('active');
            });
            document.querySelector('body').classList.remove('search-drawer-open', 'no-scroll');

            Array.from(
                section.querySelectorAll(".category-custom-details-disclosure")
            ).forEach(function(element) {
                if (element.hasAttribute("open")) {
                    element.classList.remove("open");
                    element.removeAttribute("open");
                    document.querySelector("body").classList.remove("megamenu-open");
                }
            });

            Array.from(
                section.querySelectorAll(".custom-details-disclosure")
            ).forEach(function(element) {
                if (navElement == element) {
                    navElement.setAttribute("open", '');
                    navElement.classList.add("open");
                    navElement.closest(".header-nav-blocks").classList.add("megamenu-block");
                } else {
                    element.removeAttribute("open");
                    element.classList.remove("open");
                    Array.from(
                        element.querySelectorAll(".sub-menu-custom-details-disclosure")
                    ).forEach(function(childElement) {
                        childElement.removeAttribute("open");
                    });
                }
            });
        });

        navElement.addEventListener("mouseleave", () => {
            navElement.classList.remove("open");
            navElement.removeAttribute("open");
            document.querySelector("body").classList.remove("megamenu-open");
            // let childelements = navElement.querySelectorAll(".nav-submenu li");
            //   Array.from(childelements).forEach(function(childelement){
            //     childelement.style.transitionDelay  = 'unset';

            //   })
        });
    });
    let onHoverSubMenuElements = section.querySelectorAll(
        ".sub-menu-custom-details-disclosure"
    );
    Array.from(onHoverSubMenuElements).forEach(function(subMenuElement) {
        subMenuElement.addEventListener("mouseover", () => {
            Array.from(
                document.querySelectorAll(".sub-menu-custom-details-disclosure")
            ).forEach(function(element) {
                if (subMenuElement == element) {
                    element.setAttribute("open", "");
                } else {
                    element.removeAttribute("open");
                }
            });
        });
    });
    let categoriesSelectors = section.querySelectorAll(
        ".category-custom-details-disclosure"
    );
    Array.from(categoriesSelectors).forEach(function(categoriesSelector) {
        categoriesSelector.addEventListener("click", () => {
            Array.from(document.querySelectorAll(".categories-inner--submenu")).forEach(function(element) {
                   
                let index = element.dataset.index;
                let contentElement = document.querySelector(".sub-category-menu-content-" + index);
                if (index == 1) {
                    contentElement.classList.remove("hidden");
                } 
        
        });
            setTimeout(function() {

                if (categoriesSelector.hasAttribute("open")) {
                    Array.from(
                        document.querySelectorAll("[data-search-input]")
                    ).forEach(function(element) {
                        element.value = '';
                    });
                    Array.from(
                        document.querySelectorAll("[data-result-container]")
                    ).forEach(function(element) {
                        element.classList.add('hidden');
                    });
                    Array.from(
                        document.querySelectorAll("[data-search-drawer]")
                    ).forEach(function(element) {
                        element.classList.add('hidden');
                        element.classList.remove('active');
                    });
                    document.querySelector('body').classList.remove('search-drawer-open', 'no-scroll');
                    document.querySelector("body").classList.add("megamenu-open");
                } else {
                    document.querySelector("body").classList.remove("megamenu-open");
                }
            }, 100);
        });
    });

    
    Array.from(section.querySelectorAll('[data-child-index]')).forEach(function(singleChild) {
        singleChild.addEventListener("mouseover", () => {
            if(singleChild.classList.contains('active')) return;

            // Array.from(section.querySelectorAll('[data-child-index]')).forEach(function(child) {
            //     child.classList.remove('active');
            // });

            // Array.from(section.querySelectorAll('[data-grandchild-index]')).forEach(function(child) {
            //     child.classList.remove('active');
            // });

            // const secondLevelIndex = singleChild.getAttribute('data-child-index');
           
           singleChild.closest('[data-second-level]').querySelectorAll(`[data-child]`).forEach(function(child){
            child.classList.remove('active');
           });
           singleChild.closest('[data-second-level]').querySelectorAll(`[data-grandchild]`).forEach(function(grandchild){
            grandchild.classList.remove('active');
            });

            const secondLevelIndex = singleChild.getAttribute('data-child-index');
            singleChild.classList.add('active');
            singleChild.closest('li').querySelector(`[data-grandchild-index="third-level-menu-${secondLevelIndex}"]`).classList.add('active')
       
        })
    })
}

function collectionTabs(section = document) {
    let tabs = section.querySelectorAll(".product-tab-item");
    setTimeout(() => {
        Array.from(section.querySelectorAll('.tab-contents-item.hidden')).forEach(function(tabContent) {
            Array.from(tabContent.querySelectorAll('[data-product-grid]')).forEach(function(item) {
                item.classList.remove('aos-animate');
            })
        })
    }, 1000);

    Array.from(tabs).forEach(function(tab) {
        tab.addEventListener("click", () => {
            let parentSection = tab.closest('.shopify-section');
            let current = parentSection.querySelector(".product-tab-item.active");
            if (current) {
                current.classList.remove("active");
            }
            tab.classList.add("active");
            let activeTab = tab.getAttribute("data-tab");
            let sectionElement = parentSection.querySelector('#' + activeTab);
            // 👇️ hides element (still takes up space on the page)
            let contents = parentSection.querySelectorAll(".tab-contents-item");
            Array.from(contents).forEach(function(content) {
                if (content.id === activeTab) {
                    content.classList.remove("hidden");
                    setTimeout(() => {
                        Array.from(content.querySelectorAll('[data-product-grid]')).forEach(function(item) {
                            item.classList.add('aos-animate');
                        })
                    }, 100);
                } else {
                    content.classList.add("hidden");
                    Array.from(content.querySelectorAll('[data-product-grid]')).forEach(function(item) {
                        item.classList.remove('aos-animate');
                    })
                }
            });
            if (sectionElement) {
                let sliderELement = sectionElement.querySelector("[data-slideshow]");
                if (sliderELement.classList.contains("flickity-enabled")) {
                    slideshowInit(sliderELement);
                }
                let flkty = Flickity.data(sliderELement);
                if (flkty) {
                    if (flkty.selectedElements.length >= flkty.cells.length) {
                        sliderELement.classList.add("disable-arrows");
                        flkty.options.draggable = false;
                        flkty.updateDraggable();
                    } else {
                        flkty.options.draggable = true;
                        flkty.updateDraggable();
                        sliderELement.classList.remove("disable-arrows");
                    }
                    flkty.resize();
                }
            }
        });
    });

}

function featuredImages(section = document) {
    let featuredImageWrapper = section.querySelectorAll(
        "[data-featured-image-wrapper]"
    );
    Array.from(featuredImageWrapper).forEach(function(wrapper) {
        let windowTop = window.pageYOffset;
        let elementBottom = wrapper.offsetTop + wrapper.offsetHeight;
        let windowBottom = windowTop + window.innerHeight;
        if (windowBottom > elementBottom) {
            if (wrapper.querySelector(".item-second")) {
                wrapper.querySelector(".item-second").style.cssText =
                    "transform: translate3d(0px, 0vw, 0px";
            }
            if (wrapper.querySelector(".item-third")) {
                wrapper.querySelector(".item-third").style.cssText =
                    "transform: translate3d(0px, 0vw, 0px";
            }
        } else {
            if (wrapper.querySelector(".item-second")) {
                wrapper.querySelector(".item-second").style.cssText =
                    "transform: translate3d(0px, -10vw, 0px";
            }
            if (wrapper.querySelector(".item-third")) {
                wrapper.querySelector(".item-third").style.cssText =
                    "transform: translate3d(0px, -20vw, 0px";
            }
        }
        window.addEventListener("scroll", function() {
            if (isOnScreen(wrapper)) {
                Array.from(wrapper.querySelectorAll("[data-featured-image]")).forEach(
                    function(fImage) {
                        let min = 0;
                        if (fImage.classList.contains("item-second")) {
                            min = -10;
                        }
                        if (fImage.classList.contains("item-third")) {
                            min = -20;
                        }
                        let windowTop = window.pageYOffset;
                        let elementTop = wrapper.offsetTop;
                        let windowHeight = Math.min(500, window.innerHeight);
                        let topDifference = elementTop - windowTop;
                        if (topDifference >= 0) {
                            let initials =
                                ((windowHeight - topDifference) / windowHeight) * 100;
                            let finals = ((100 - initials) / 100) * min;
                            let finalTranslate = Math.max(min, Math.min(finals, 0));
                            fImage.style.cssText = `transform: translate3d(0px, ${finalTranslate}vw, 0px)`;
                        }
                    }
                );
            }
        });
    });
}

function announcementCollapsiblecontent(section = document) {
    let toggle_btn = section.querySelectorAll(".announcement-btn");
    let contents = section.querySelectorAll(".announcement-dropdown");
    Array.from(toggle_btn).forEach(function(btn) {
        btn.addEventListener("click", () => {
            let current = section.querySelector(".announcement-btn.active");
            // if (current) {
            //     current.classList.remove("active");
            // }
            btn.classList.toggle("active");
            if (
                document.querySelector("body").classList.contains("announcement-open")
            ) {
                document.querySelector("body").classList.remove("announcement-open");
                document.querySelector("body").classList.remove("no-scroll");
            } else {
                document.querySelector("body").classList.add("announcement-open");
                document.querySelector("body").classList.add("no-scroll");
            }

            let activeTab = btn.getAttribute("data-toggle");
            //let sectionElement = document.getElementById(activeTab);
            // 👇️ hides element (still takes up space on the page)
            Array.from(contents).forEach(function(content) {
                if (content.id === activeTab) {
                    content.classList.toggle("show");
                } else {
                    // content.classList.add("show-toggle-content");
                }
            });
        });
    });
}

function headerNavigationPosition(section = document) {
    if (window.innerWidth < 992) return false;
    let allNavigations = section.querySelectorAll("[data-navigation-item]");
    Array.from(allNavigations).forEach(function(navItem) {
        navItem.classList.remove("left-menu");
        let windowSize = window.innerWidth - 200;
        let currentPosition = navItem.offsetLeft + navItem.clientWidth;
        if (navItem.querySelector(".nav-submenu.inner")) {
            currentPosition =
                currentPosition +
                navItem.querySelector(".nav-submenu.inner").clientWidth;
        }
        if (currentPosition >= windowSize) {
            navItem.classList.add("left-menu");
        }
    });
}
window.addEventListener("resize", (event) => {
    setTimeout(function() {
        let sliderElements = document.querySelectorAll("[data-slideshow]");
        Array.from(sliderElements).forEach(function(selector) {
            if (!selector.classList.contains("flickity-enabled")) {
                slideshowInit(selector);
            }
            if (selector.classList.contains("slideshow-section")) {
                let options = JSON.parse(selector.dataset.slideshow);
                if (options) {
                    let flkty = new Flickity(selector, options);
                     let thumbnailItems = document.querySelectorAll('.slideshow-thumbnail');
                        thumbnailItems.forEach(function(thumbnailItem) {
                            thumbnailItem.style.transition = ''; // Corrected syntax: '0.5s ease'
                        });
                        flkty.destroy();
                        slideshowInit(selector);
                }
            }
            let flkty = Flickity.data(selector);
            if (flkty) {
                if (flkty.selectedElements.length >= flkty.cells.length) {
                    selector.classList.add("disable-arrows");
                    flkty.options.draggable = false;
                    flkty.updateDraggable();
                } else {
                    flkty.options.draggable = true;
                    flkty.updateDraggable();
                    selector.classList.remove("disable-arrows");
                }
             
                setTimeout(() => {
                    flkty.resize();
                }, 500)
                
            }
        });
    }, 500);
    if (window.innerWidth > 991) {
        if (document.body.classList.contains("nav-open")) {
            document.body.classList.remove("nav-open");
        }
    } else {
        if (document.querySelector(".category-custom-details-disclosure")) {
            if (
                document
                .querySelector(".category-custom-details-disclosure")
                .hasAttribute("open")
            ) {
                document
                    .querySelector(".category-custom-details-disclosure")
                    .removeAttribute("open");
                document.querySelector("body").classList.remove("megamenu-open");
            }
        }
    }
    headerNavigationPosition();
});



var mouse_is_inside = false;

function outSideClickTrigger(section = document) {
    let elementList = section.querySelectorAll(
        "[data-humburger-body],[data-hamburger-menu],.compare-modal-content,[data-button-compare],[data-quick-view],.side-drawer-content,.product-menus-list-item,[data-side-drawer-open],.sr-product-model-item,.header-top-wrap,.header-search,.search-content,[data-search-open],.header-categories-wrapper,.category-custom-details-disclosure,.custom-details-disclosure,.sub-menu-custom-details-disclosure, .announcement-dropdown,.popup-content-inner,[data-cart-drwaer-body]"
    );
    Array.from(elementList).forEach(function(element) {
        element.addEventListener("mouseover", () => {
            mouse_is_inside = true;
        });

        element.addEventListener("mouseout", () => {
            mouse_is_inside = false;
        });
    });

    document.addEventListener("click", function() {
        if (!mouse_is_inside) {
            document.querySelector("body").classList.remove("no-scroll");
            document.querySelector("body").classList.remove("popup-open");
            let searchDrawer = document.querySelector("[data-search-drawer]");
            if (searchDrawer) {
                let headerStyle = searchDrawer.getAttribute("data-header");
                let resultContainer = searchDrawer.querySelector(
                    "[data-result-container]"
                );
                let suggestionContainer = searchDrawer.querySelector(
                    "[data-suggestions-container]"
                );
                if (suggestionContainer) {
                    suggestionContainer.classList.remove("hidden");
                }
                searchDrawer.classList.add("hidden");
                searchDrawer.classList.remove("active");
                document.querySelector("body").classList.remove("search-drawer-open");
                if (resultContainer) {
                    resultContainer.classList.add("hidden");
                }
                if (
                    headerStyle == "logo_with_search_bar" &&
                    document.querySelector("[data-search-input]")
                ) {
                    document.querySelector("[data-search-input]").value = "";
                }
            }
            let announcementActive = document.querySelector(
                ".announcement-btn.active"
            );
            if (announcementActive) {
                announcementActive.click();
            }
            Array.from(
                document.querySelectorAll(".categories-inner--submenu")
            ).forEach(function(element) {
                element.classList.add("hidden");
            });
            Array.from(
                document.querySelectorAll(".category-custom-details-disclosure")
            ).forEach(function(element) {
                element.removeAttribute("open");
                document.querySelector("body").classList.remove("megamenu-open");
            });
        }
    });

    document.addEventListener("keyup", function(event) {
        if (event.keyCode == 27) {
            let searchDrawer = document.querySelector("[data-search-drawer]");
            if (searchDrawer) {
                let headerStyle = searchDrawer.getAttribute("data-header");
                let resultContainer = searchDrawer.querySelector(
                    "[data-result-container]"
                );
                let suggestionContainer = searchDrawer.querySelector(
                    "[data-suggestions-container]"
                );
                if (suggestionContainer) {
                    suggestionContainer.classList.remove("hidden");
                }
                searchDrawer.classList.add("hidden");
                searchDrawer.classList.remove("active");
                if (resultContainer) {
                    resultContainer.classList.add("hidden");
                }
                if (headerStyle == "logo_with_search_bar" && document.querySelector("[data-search-input]")
) {
                    document.querySelector("[data-search-input]").value = "";
                }
            }
            document.querySelector("body").classList.remove("no-scroll");
            let announcementActive = document.querySelector(
                ".announcement-btn.active"
            );
            if (announcementActive) {
                announcementActive.click();
            }
            Array.from(
                document.querySelectorAll(".categories-inner--submenu")
            ).forEach(function(element) {
                element.classList.add("hidden");
            });
            Array.from(
                document.querySelectorAll(".category-custom-details-disclosure")
            ).forEach(function(element) {
                element.removeAttribute("open");
                document.querySelector("body").classList.remove("megamenu-open");
            });
            let sideDraweropenElements =
                section.querySelectorAll("[data-side-drawer]");
            Array.from(sideDraweropenElements).forEach(function(sideDrawer) {
                if (sideDrawer.classList.contains("collection-filter-sidebar"))
                    return false;
                setTimeout(function() {
                   
                    sideDrawer.style.display = "none";
                }, 300);
                sideDrawer.classList.remove("sidebar-visible", "popup-visible");
                document.querySelector("body").classList.remove("no-scroll");
                stopFocusRotation();
                if (previousFocusElement) {
                    if (previousFocusElement.classList.contains("product-quickview")) {
                        if (
                            previousFocusElement
                            .closest("[data-product-grid]")
                            .querySelector(".product-title")
                        ) {
                            previousFocusElement
                                .closest("[data-product-grid]")
                                .dispatchEvent(new Event("mouseover"));
                            previousFocusElement
                                .closest("[data-product-grid]")
                                .querySelector(".product-title")
                                .focus();
                        }
                    } else {
                        previousFocusElement.focus();
                    }
                }
                previousFocusElement = "";
                if (sideDrawer.classList.contains("address-sidebar")) {
                    let addressForm = sideDrawer.querySelector("form");
                    if (addressForm) {
                        addressForm.reset();
                    }
                }
            });
        }
    });

    document.addEventListener("mouseover", function() {
        if (!mouse_is_inside) {
            // Array.from(
            //     document.querySelectorAll(".categories-inner--submenu")
            // ).forEach(function(element) {
            //     element.classList.add("hidden");
            // });
            Array.from(
                document.querySelectorAll(".category-custom-details-disclosure")
            ).forEach(function(element) {
                if(element.hasAttribute("open")) return false;
                element.removeAttribute("open");
                document.querySelector("body").classList.remove("megamenu-open");
            });
            Array.from(
                document.querySelectorAll(".custom-details-disclosure")
            ).forEach(function(element) {
                element.removeAttribute("open");
                element.classList.remove("open");
                element
                    .closest(".header-nav-blocks")
                    .classList.remove("megamenu-block");
            });
            Array.from(
                document.querySelectorAll(".sub-menu-custom-details-disclosure")
            ).forEach(function(element) {
                element.removeAttribute("open");
            });
        }
    });
}

let lastScrollTop = 0;

function showPosition(element) {
    var originalPosition = element.style.position;
    element.style.position = "static";
    element.style.position = originalPosition;
    return element.getBoundingClientRect().top;
}

function onScrollImageWithText() {
    let lastScroll = 0;
    let checkScroll;
    var st = window.pageYOffset || document.documentElement.scrollTop;
    if (st > lastScroll) {
        checkScroll = false;
    } else if (st < lastScroll) {
        checkScroll = true;
    }
    lastScroll = st <= 0 ? 0 : st;
    let imageCarousels = document.querySelectorAll("[data-image-with-text-grid]");
    if (imageCarousels) {
        Array.from(imageCarousels).forEach(function(imageCarousel) {
            const original_width = imageCarousel.offsetWidth;
            let children = imageCarousel.getElementsByClassName(
                "image-with-text-content"
            );
            if (children && children.length > 0) {
                for (var i = 0; i < children.length; i++) {
                    let item = 0;
                    if (i == 0) {
                        item = 1;
                    } else {
                        item = i + 1;
                    }
                    if (showPosition(children[i]) > 24 * item) {
                        children[i].style.width = original_width + "px";
                    }
                    if (showPosition(children[i]) == 24 * item && !checkScroll) {
                        let previous_width = children[i].offsetWidth;
                        children[i].style.width = parseInt(previous_width - 1) + "px";
                    } else if (showPosition(children[i]) == 24 * item && checkScroll) {
                        let previous_width = children[i].offsetWidth;
                        children[i].style.width = parseInt(previous_width + 1) + "px";
                    }
                }
            }
        });
    }
}

function isScrolledIntoView($el) {
    var doc = document.documentElement;
    var winTop = (window.pageYOffset || doc.scrollTop) - (doc.clientTop || 0);
    var winBottom = winTop + window.innerHeight;
    var elTop = $el.offsetTop;
    return elTop <= winBottom + 50;
}

function scrollTop() {
    let back_to_top = document.querySelector("#back_to_top");
    if (!back_to_top) {
        return false;
    } else {
        back_to_top.addEventListener("click", function() {
            topFunction();
        });
        window.onscroll = function() {
            if (document.documentElement.scrollTop > 900) {
                back_to_top.classList.remove("hidden");
                back_to_top.classList.add("show");
            } else {
                back_to_top.classList.remove("show");
                back_to_top.classList.add("hidden");
            }
        };
    }

    function topFunction() {
        window.scrollTo({ top: 0, behavior: "smooth" });
    }
}

function productCardHoverInit() {
    productOnHoverQucikviewButton();
}

function productOnHoverQucikviewButton(section = document) {
    let hoverelements = document.querySelectorAll(
        ".product-card-item[data-product-hover]"
    );
    Array.from(hoverelements).forEach(function(hoverelement) {
        if (hoverelement) {
            hoverelement.addEventListener("mouseover", function(element) {
                let heightBase = 0;
                if (window.innerWidth > 1024) {
                    if (hoverelement.querySelector(".product-quickview-button")) {
                        const imageHeight =
                            hoverelement.querySelector(".product-card-img").offsetHeight;
                        const infoHeight = hoverelement.querySelector(
                            ".product-card-detail"
                        ).offsetHeight;
                        heightBase = imageHeight + infoHeight;
                        const actionsHeight =
                            hoverelement.querySelector(".product-quickview-button")
                            .offsetHeight || 0;
                        const heightExpanded = heightBase + actionsHeight;
                        hoverelement.querySelector(".product-card").style.height =
                            heightExpanded + "px";
                        hoverelement.style.height = heightBase + "px";
                        if (!hoverelement.closest(".flickity-enabled")) {
                            Array.from(hoverelements).forEach(function(element) {
                                element.querySelector(".product-card").style.zIndex = "1";
                            });
                            hoverelement.querySelector(".product-card").style.zIndex = "2";
                        }
                    }
                }
            });
            hoverelement.addEventListener("mouseleave", function(element) {
                if (window.innerWidth > 1024) {
                    if (hoverelement.querySelector(".product-quickview-button")) {
                        hoverelement.querySelector(".product-card").style.height = null;
                        hoverelement.style.height = null;
                        if (!hoverelement.closest(".flickity-enabled")) {
                            Array.from(hoverelements).forEach(function(element) {
                                element.querySelector(".product-card").style.zIndex = null;
                            });
                            hoverelement.querySelector(".product-card").style.zIndex = null;
                        }
                    }
                }
            });
        }
    });
}

function verifyAge(event) {
    event.preventDefault();
    let target = event.target;
    let ageVerificationContainer = target.closest(".age-verification");
    if (ageVerificationContainer) {
        ageVerificationContainer.classList.remove("active");
        document.querySelector("body").classList.remove("no-scroll");
        setCookie("ageVerified", "true", 15);
    }
}

function rejectAgeVerify(event) {
    event.preventDefault();
    let target = event.target;
    let ageVerificationWrapper = target.closest(".age-verification-wrapper");
    if (ageVerificationWrapper) {
        let declineContainer = ageVerificationWrapper.querySelector(
            ".age-verification-decline"
        );
        if (declineContainer) {
            target.closest(".age-verification-outer").classList.remove("active");
            declineContainer.classList.add("active");
        }
    }
}

function backToAgeVerify(event) {
    event.preventDefault();
    let target = event.target;
    let ageVerificationWrapper = target.closest(".age-verification-wrapper");
    if (ageVerificationWrapper) {
        let ageVerificationContainer = ageVerificationWrapper.querySelector(
            ".age-verification-outer"
        );
        if (ageVerificationContainer) {
            target.closest(".age-verification-decline").classList.remove("active");
            ageVerificationContainer.classList.add("active");
        }
    }
}

function compareProducts(event) {
    let currentElement = event.target;
    if (!currentElement.closest(".compare-checkbox").classList.contains("checked_label")) {
        currentElement.closest("body").querySelector(".compare-basket").classList.add("open");
        updateCompareProducts(currentElement, "add");
    } else {
        updateCompareProducts(currentElement, "remove");
    }
}

function updateCompareProducts(currentElement, method) {
    let cookieName = "products-compare";
    //let getProductid = currentElement.getAttribute('data-product-id');
    let getProductid = parseInt(currentElement.getAttribute("data-product-id"));
    let cvProducts = JSON.parse(window.localStorage.getItem(cookieName) || "[]");
    let select_checkbox = document.querySelectorAll(".js-compare-checkbox");
    if (!isNaN(getProductid)) {
        if (method == "add") {
            if (!cvProducts.includes(getProductid)) {
                cvProducts.push(getProductid);
                Array.from(select_checkbox).forEach(function(checked_box) {
                    let getProductid = parseInt(
                        checked_box.getAttribute("data-product-id")
                    );
                    if (cvProducts.includes(getProductid) && cvProducts.length < 5) {
                        checked_box.setAttribute("checked", true);
                        checked_box.closest(".compare-checkbox").classList.add("checked_label");
                    }
                });
            }
            if (cvProducts.length >= 4) {
                document.querySelector("body").classList.add("no-compare");
            } else {
                document.querySelector("body").classList.remove("no-compare");
            }
            if (document.querySelector("[data-button-compare]")) {
                if (cvProducts.length == 1) {
                    document
                        .querySelector("[data-button-compare]")
                        .setAttribute("disabled", true);
                } else {
                    document
                        .querySelector("[data-button-compare]")
                        .removeAttribute("disabled");
                }
            }
        } else {
            if (cvProducts.includes(getProductid)) {
                let index = cvProducts.indexOf(getProductid);
                if (index > -1) {
                    cvProducts.splice(index, 1);
                    Array.from(select_checkbox).forEach(function(checked_box) {
                        checked_box.setAttribute("checked", false);
                        checked_box.closest(".compare-checkbox").classList.remove("checked_label");
                        let getProductid = parseInt(
                            checked_box.getAttribute("data-product-id")
                        );
                        if (cvProducts.includes(getProductid)) {
                            checked_box.setAttribute("checked", true);
                            checked_box
                                .closest(".compare-checkbox")
                                .classList.add("checked_label");
                        }
                    });
                }
            }
            document.querySelector("body").classList.remove("no-compare");
            if (document.querySelector("[data-button-compare]")) {
                if (cvProducts.length == 1) {
                    document
                        .querySelector("[data-button-compare]")
                        .setAttribute("disabled", true);
                } else {
                    document
                        .querySelector("[data-button-compare]")
                        .removeAttribute("disabled");
                }
            }
        }
        window.localStorage.setItem(
            cookieName,
            JSON.stringify(cvProducts.slice(0, 4))
        );
        if (cvProducts.length > 0) {
            if (document.querySelector(".compare-btn-sidebar")) {
                document
                    .querySelector(".compare-btn-sidebar")
                    .classList.remove("hidden");
            }
            let currentItems = cvProducts
                .map((item) => "id:" + item)
                .slice(0, 4)
                .join(" OR ");
            getCompareGridData(currentItems);
        } else {
            if (document.querySelector(".compare-btn-sidebar")) {
                document.querySelector(".compare-btn-sidebar").classList.add("hidden");
            }
            if (document.querySelector("body").querySelector(".compare-basket")) {
                document
                    .querySelector("body")
                    .querySelector(".compare-basket")
                    .classList.remove("open");
            }
            if (
                document.querySelector("body").classList.contains("compare-popup-open")
            ) {
                document.querySelector("body").classList.remove("compare-popup-open");
                document.querySelector("body").classList.remove("no-scroll");
            }
            if (document.querySelector("#bucketContainer")) {
                document.querySelector("#bucketContainer").innerHTML = "";
            }
        }
    }
}

function compareBarViewToggle(section = document) {
    let toggleButtons = section.querySelectorAll(".compact-view-button");
    Array.from(toggleButtons).forEach(function(toggleButton) {
        toggleButton.addEventListener("click", function(event) {
            if (toggleButton.parentElement.classList.contains("compact-view")) {
                toggleButton.parentElement.classList.remove("compact-view");
            } else {
                toggleButton.parentElement.classList.add("compact-view");
            }
        });
    });
}

function getCompareGridData(products) {
    let CompareproductParent = document.querySelector(
        "[data-compare-product-wrapper]"
    );
    if (CompareproductParent) {
        let CompareproductWrapper =
            CompareproductParent.getAttribute("data-section");
        fetch(mainSearchUrl + CompareproductWrapper + products)
            .then((response) => response.text())
            .then((text) => {
                let resultsMarkup = new DOMParser()
                    .parseFromString(text, "text/html")
                    .querySelector(".shopify-section");
                document.getElementById("bucketContainer").innerHTML =
                    resultsMarkup.querySelector("[data-compare-items]").innerHTML;
                let compareModelInfo = document.querySelector("[compare-model-info]");
                compareButtonContent();
                compareModelInfo.innerHTML = resultsMarkup.querySelector(
                    "[data-compare-items-info]"
                ).innerHTML;
                getATCelement();
                let modelProductcount = compareModelInfo
                    .querySelector(".compare-modal-results")
                    .getAttribute("data-products-count");
                let removeItems = document.querySelectorAll("[data-remove-icon]");
                removeCompareGridData(removeItems);
                setTimeout(function() {
                    if (modelProductcount == 0) {
                        if (
                            compareModelInfo
                            .closest("[data-compare-product-wrapper]")
                            .querySelector(".compare-basket")
                        ) {
                            compareModelInfo
                                .closest("[data-compare-product-wrapper]")
                                .querySelector(".compare-basket")
                                .classList.remove("open");
                        }
                        if (
                            compareModelInfo
                            .closest("[data-compare-product-wrapper]")
                            .querySelector(".compare-modal-results")
                        ) {
                            compareModelInfo.querySelector(
                                ".compare-modal-results"
                            ).style.display = "none";
                        }
                        if (
                            compareModelInfo
                            .closest("[data-compare-product-wrapper]")
                            .querySelector(".empty-modal-info")
                        ) {
                            compareModelInfo
                                .querySelector(".compare-modal-results")
                                .querySelector(".empty-modal-info").style.display = "block";
                        }
                        if(compareModelInfo.querySelector("[data-compare-model-close]")){
                        compareModelInfo.querySelector("[data-compare-model-close]").click();
                        }  
                    } else {
                        if (compareModelInfo.closest(".compare-modal-results")) {
                            if (
                                compareModelInfo
                                .closest(".compare-modal-results")
                                .querySelector(".compare-modal-results")
                            ) {
                                compareModelInfo.querySelector(
                                    ".compare-modal-results"
                                ).style.display = "block";
                            }
                            if (
                                compareModelInfo
                                .closest(".compare-modal-results")
                                .querySelector(".empty-modal-info")
                            ) {
                                compareModelInfo
                                    .querySelector(".compare-modal-results")
                                    .querySelector(".empty-modal-info").style.display = "none";
                            }
                        }
                    }
                }, 500);
                CloseCompareModel();

                return false;
            })
            .catch((e) => {
                console.error(e);
            });
    }
}

function removeCompareGridData(removeItems) {
    Array.from(removeItems).forEach(function(element) {
        element.addEventListener("click", function(event) {
            event.preventDefault();
            let cookieName = "products-compare";
            //let getProductid = currentElement.getAttribute('data-product-id');
            let removeProductId = parseInt(
                this.querySelector(".remove_icon").getAttribute("data-remove")
            );
            let cvProducts = JSON.parse(
                window.localStorage.getItem(cookieName) || "[]"
            );
            if (cvProducts.includes(removeProductId)) {
                let index = cvProducts.indexOf(removeProductId);
                if (index > -1) {
                    cvProducts.splice(index, 1);
                }
            }
            let select_checkbox = document.querySelectorAll(
                '.js-compare-checkbox[data-product-id="' + removeProductId + '"]'
            );
            Array.from(select_checkbox).forEach(function(checked_box) {
                if (
                    checked_box
                    .closest(".compare-checkbox")
                    .classList.contains("checked_label")
                ) {
                    checked_box
                        .closest(".compare-checkbox")
                        .classList.remove("checked_label");
                }
            });
            window.localStorage.setItem(
                cookieName,
                JSON.stringify(cvProducts.slice(0, 4))
            );

            if (cvProducts.length == 0) {
                if (document.querySelector(".compare-btn-sidebar")) {
                    document
                        .querySelector(".compare-btn-sidebar")
                        .classList.add("hidden");
                }
                document
                    .querySelector("body")
                    .querySelector(".compare-basket")
                    .classList.remove("open");
                if (
                    document
                    .querySelector("body")
                    .classList.contains("compare-popup-open")
                ) {
                    document.querySelector("body").classList.remove("compare-popup-open");
                    document.querySelector("body").classList.remove("no-scroll");
                }
            }
            if (cvProducts.length >= 0) {
                let currentItems = cvProducts
                    .map((item) => "id:" + item)
                    .slice(0, 4)
                    .join(" OR ");
                getCompareGridData(currentItems);
            }
            if (cvProducts.length >= 4) {
                document.querySelector("body").classList.add("no-compare");
            } else {
                document.querySelector("body").classList.remove("no-compare");
            }
            if (document.querySelector("[data-button-compare]")) {
                if (cvProducts.length == 1) {
                    document
                        .querySelector("[data-button-compare]")
                        .setAttribute("disabled", true);
                } else {
                    document
                        .querySelector("[data-button-compare]")
                        .removeAttribute("disabled");
                }
            }
        });
    });
}

function compareButtonContent(section = document) {
    let compareButton = section.querySelector("[data-button-compare]");
    let compareWrapper = section.querySelector(
        ".compare-modal-content[data-side-drawer]"
    );
    compareButton.addEventListener("click", function() {
        if (compareWrapper) {
            if (compareWrapper.classList.contains("popup")) {
                compareWrapper.classList.add("popup-visible");
                compareWrapper.style.display = "flex";
                document.querySelector("body").classList.add("no-scroll");
            }
        }
        setTimeout(() => {
            focusElementsRotation(compareWrapper);
        }, 500);
        document.querySelector("body").classList.add("compare-popup-open");
        // CloseCompareModel();
    });
}

function checkedboxCookies() {
    let cookieName = "products-compare";
    let select_checkbox = document.querySelectorAll(".js-compare-checkbox");
    let cvProducts = JSON.parse(window.localStorage.getItem(cookieName) || "[]");
    let currentItems = cvProducts
        .map((item) => "id:" + item)
        .slice(0, 4)
        .join(" OR ");

    if (cvProducts.length > 0) {
        getCompareGridData(currentItems);
        if (document.querySelector(".compare-btn-sidebar")) {
            document.querySelector(".compare-btn-sidebar").classList.remove("hidden");
        }
    }

    Array.from(select_checkbox).forEach(function(checked_box) {
        let getProductid = parseInt(checked_box.getAttribute("data-product-id"));
        if (cvProducts.includes(getProductid)) {
            checked_box.setAttribute("checked", true);
            checked_box.closest(".compare-checkbox").classList.add("checked_label");
        }
    });

    if (cvProducts.length <= 4) {
        document.querySelector("body").classList.add("no-compare");
    } else {
        document.querySelector("body").classList.remove("no-compare");
    }
    if (document.querySelector("[data-button-compare]")) {
        if (cvProducts.length == 1) {
            document
                .querySelector("[data-button-compare]")
                .setAttribute("disabled", true);
        } else {
            document
                .querySelector("[data-button-compare]")
                .removeAttribute("disabled");
        }
    }
}

function CloseCompareModel(section = document) {
    let CloseCompareModelElements = section.querySelectorAll(
        "[data-compare-model-close]"
    );
    Array.from(CloseCompareModelElements).forEach(function(drawer_element) {
        drawer_element.addEventListener("click", (event) => {
            event.preventDefault();
            let sideDrawers = drawer_element.closest("[data-side-drawer]");
            if (sideDrawers) {
                sideDrawers.classList.remove("popup-visible");
                if (sideDrawers.classList.contains("popup")) {
                    // sideDrawers.fadeOut(500)
                }
                if (
                    document
                    .querySelector("body")
                    .classList.contains("compare-popup-open")
                ) {
                    document.querySelector("body").classList.remove("compare-popup-open");
                    document.querySelector("body").classList.remove("no-scroll");
                }
            }
        });
    });
    let close_button = document.querySelector("#closeButton");
    if (close_button) {
        close_button.addEventListener("click", function(e) {
            document.querySelector(".compare-basket").classList.remove("open");
        });
    }
}

function toggleCompareBasket(event) {
    event.preventDefault();
    let basket = document.querySelector(".compare-basket");
    if (basket) {
        if (basket.classList.contains("open")) {
            basket.classList.remove("open");
        } else {
            basket.classList.add("open");
        }
    }
}

function closeNewsletterOfferPopup(event) {
    event.preventDefault();
    let newsletterofferPopupContainer =
        document.querySelector(".newsletter-popup");
    if (newsletterofferPopupContainer) {
        setCookie(
            "newsletterofferPopUpClosed",
            "true",
            newsletterofferPopupExpDays
        );
        newsletterofferPopupContainer.classList.remove("active");
        document.querySelector("body").classList.remove("no-scroll");
    }
}

function showMoremedia(section = document) {
    let showMoreButton = document.getElementById("showMoreButton");
    let mediaItems = document.querySelectorAll(".featured_product_image_item");
    if (showMoreButton) {
        showMoreButton.addEventListener("click", function() {
            let allMediaVisible = showMoreButton.textContent === "Show More";
            mediaItems.forEach(function(mediaItem, index) {
                if (index > 3) {
                    mediaItem.classList.toggle("hidden-media", !allMediaVisible);
                }
            });
            showMoreButton.textContent = allMediaVisible ? "Show Less" : "Show More";
            if (allMediaVisible) {
                setTimeout(function() {
                    let lastMediaItem = mediaItems[mediaItems.length - 1];
                    lastMediaItem.scrollIntoView();
                }, 100);
            } else {
                window.scrollTo({ top: 0, behavior: "smooth" });
            }
        });
    }
    return false;
}

function announementHeightOnScroll() {
    let announcementSection = document.querySelector(".announcement-section");
    if (!announcementSection) return false;
    let annoucementHeight = announcementSection.offsetHeight;
    let scrollTop = window.scrollY;
    if (scrollTop > annoucementHeight) {
        document
            .querySelector("body")
            .style.setProperty("--announcementHeight", `0px`);
    } else {
        let annouceHeight = Math.max(annoucementHeight - scrollTop, 0);
        document
            .querySelector("body")
            .style.setProperty("--announcementHeight", `${annouceHeight}px`);
    }
}

function mobileNavigation(_section = document) {
    let header = _section.querySelector(".main-header");
    if (header) {
        let mobileMenuSelector = header.querySelector("[data-mobile-menu]");
        if (mobileMenuSelector) {
            mobileMenuSelector.addEventListener("click", function(event) {
                event.preventDefault();
                if (mobileMenuSelector.classList.contains("active")) {
                    mobileMenuSelector.classList.remove("active");
                    document.querySelector("body").classList.remove("nav-open");
                    setTimeout(() => {
                        Array.from(header.querySelectorAll(".child")).forEach(function(
                            menu
                        ) {
                            DOMAnimations.slideUp(menu);
                        });
                    }, 200);
                } else {
                    mobileMenuSelector.classList.add("active");
                    document.querySelector("body").classList.add("nav-open");
                }
            });
            document.addEventListener("click", function(event) {
                let element = event.target;
                if (
                    mobileMenuSelector.contains(element) ||
                    element === mobileMenuSelector ||
                    header.querySelector("#mobileMenu").contains(element) ||
                    element === header.querySelector("#mobileMenu")
                ) {
                    return false;
                } else {
                    if (mobileMenuSelector.classList.contains("active")) {
                        mobileMenuSelector.classList.remove("active");
                        document.querySelector("body").classList.remove("nav-open");
                        setTimeout(() => {
                            Array.from(header.querySelectorAll(".child")).forEach(function(
                                menu
                            ) {
                                DOMAnimations.slideUp(menu);
                            });
                        }, 200);
                    }
                }
            });
        }

        let subMenuSelectors = header.querySelectorAll("[data-submenu-trigger]");
        Array.from(subMenuSelectors).forEach(function(subMenu) {
            subMenu.addEventListener("click", function(event) {
                event.preventDefault();
                let subChildSelector = subMenu.dataset.submenuTrigger;
                let subChild = header.querySelector(
                    '[data-inner-item="' + subChildSelector + '"]'
                );
                if (subMenu.classList.contains("active")) {
                    subMenu.classList.remove("active");
                    subMenu.closest(".nav-item-header").classList.remove("active-bg");
                    if (subChild) {
                        DOMAnimations.slideUp(subChild);
                    }
                } else {
                    subMenu.classList.add("active");
                    subMenu.closest(".nav-item-header").classList.add("active-bg");
                    if (subChild) {
                        DOMAnimations.slideDown(subChild);
                    }
                }
            });
        });

        let menuTabs = header.querySelectorAll(".menu-tab");
        Array.from(menuTabs).forEach(function(tab) {
            tab.addEventListener("click", function(event) {
                event.preventDefault();
                if (tab.classList.contains("active")) return false;
                let activeMenuTab = header.querySelector(".menu-tab.active");
                if (activeMenuTab) {
                    activeMenuTab.classList.remove("active");
                }
                tab.classList.add("active");
                let tabContent = header.querySelector(".tabcontent." + tab.dataset.tab);
                let currentTabContent = header.querySelector(".tabcontent.active");
                if (currentTabContent && tabContent) {
                    Array.from(currentTabContent.querySelectorAll(".child")).forEach(
                        function(menu) {
                            DOMAnimations.slideUp(menu);
                        }
                    );
                    currentTabContent.classList.add("hidden");
                    currentTabContent.classList.remove("active");
                    tabContent.classList.remove("hidden");
                    tabContent.classList.add("active");
                }
            });
        });

        if (
            header.classList.contains("sticky-header") &&
            header.dataset.stickyType === "on_scroll"
        ) {
            let windowScrollTop = window.scrollY;
            document.addEventListener("scroll", function() {
                let scrollHeight = header.offsetHeight * 2;
                if (window.scrollY > scrollHeight) {
                    if (windowScrollTop > window.scrollY) {
                        header.parentElement.classList.remove("sticky-header-hidden");
                        document
                            .querySelector("body")
                            .classList.remove("sticky-header-hide");
                    } else {
                        if (!document
                            .querySelector("body")
                            .classList.contains("search-drawer-open")
                        ) {
                            if (!document.querySelector("body").classList.contains('hamburger-open')) {
                                header.parentElement.classList.add("sticky-header-hidden");
                            }
                            setTimeout(function() {
                                header.parentElement.classList.add("scroll-sticky");
                            }, 500);
                            document
                                .querySelector("body")
                                .classList.add("sticky-header-hidden");
                        }
                    }
                } else {
                    header.parentElement.classList.remove("sticky-header-hidden");
                    header.parentElement.classList.remove("scroll-sticky");
                    document
                        .querySelector("body")
                        .classList.remove("sticky-header-hidden");
                }
                windowScrollTop = window.scrollY;

                if (header.parentElement.classList.contains("sticky-header-hidden")) {
                    document
                        .querySelector("body")
                        .style.setProperty("--dynamicheaderHeight", `0px`);
                } else {
                    let headerHeight = header.getBoundingClientRect().height.toFixed(2);
                    document
                        .querySelector("body")
                        .style.setProperty("--dynamicheaderHeight", `${headerHeight}px`);
                }
            });
        } else if (!header.classList.contains("sticky-header")) {
            header.parentElement.classList.remove("sticky");
        }
        document
            .querySelector("body")
            .style.setProperty(
                "--headerHeight",
                `${header.parentElement.offsetHeight}px`
            );
        announementHeightOnScroll();
    } else {
        document.querySelector("body").style.setProperty("--headerHeight", `0px`);
    }
}

function productGiftOptions(section = document) {
    let giftCardWrappers = section.querySelectorAll("[data-gift-card-box]");
    Array.from(giftCardWrappers).forEach(function(giftCard) {
        let jsCheck = giftCard.querySelector("[data-js-gift-card-selector]");
        if (jsCheck) {
            jsCheck.disabled = false;
            jsCheck.addEventListener("click", function() {
                let giftCardContent = giftCard.querySelector(
                    "[data-gift-card-content]"
                );
                if (jsCheck.checked) {
                    DOMAnimations.slideDown(giftCardContent, 500);
                } else {
                    DOMAnimations.slideUp(giftCardContent, 500);
                    let formErrorWrapper = giftCard.querySelector(
                        ".form-message__wrapper"
                    );
                    if (formErrorWrapper) {
                        formErrorWrapper.classList.add("hidden");
                        let formErrorMessage =
                            formErrorWrapper.querySelector(".error-message");
                        if (formErrorMessage) {
                            formErrorMessage.innerHTML = "";
                        }
                    }
                }
            });
        }
        let nojsCheck = giftCard.querySelector("[data-no-js-gift-card-selector]");
        if (nojsCheck) {
            nojsCheck.disabled = true;
        }
    });
}

function colorMode() {
    let checkboxToggles = document.querySelectorAll(".toggle-checkbox");

    Array.from(checkboxToggles).forEach(function(checkboxToggle) {
        checkboxToggle.addEventListener("change", () => {
            if (checkboxToggle.checked) {
                document.querySelector("html").setAttribute("color-mode", "dark");
                localStorage.darkMode = "true";
            } else {
                document.querySelector("html").setAttribute("color-mode", "light");
                localStorage.darkMode = "false";
            }
            // // document.body.classList.toggle('dark-mode');
            // // document.body.classList.toggle('light-mode');
            // localStorage.darkMode = (localStorage.darkMode == "true") ? "false" : "true";
        });
    });
}

function quickNav(section = document) {
    let quickNav = section.querySelectorAll(".product-filter-boxes button");
    Array.from(quickNav).forEach(function(quickNav) {
        quickNav.addEventListener("click", function(e) {
            e.preventDefault();
            quickNav
                .closest(".product-filter-boxes")
                .querySelector(".quick-nav__listbox")
                .classList.toggle("active");
            getSelectedvalue();
        });
    });
}

function getSelectedvalue(section = document) {
    let sectionFilter = section.querySelector("[data-multiboxes-filter]");
    let sectionParentValue = sectionFilter.closest(".shopify-section");
    let selectValueOne = sectionParentValue.querySelector(
        '.product-filter-boxes[data-level="1"]'
    );
    let selectValueTwo = sectionParentValue.querySelector(
        '.product-filter-boxes[data-level="2"]'
    );
    let selectValueThree = sectionParentValue.querySelector(
        '.product-filter-boxes[data-level="3"]'
    );
    let Parentelement = "";
    let getDatavalue = "";
    if (selectValueOne) {
        Parentelement = selectValueOne.querySelector("ul.active");
        if (Parentelement) {
            let Levelonevalues = Parentelement.querySelectorAll(
                "li.custom-select__option"
            );
            Array.from(Levelonevalues).forEach(function(Levelonevalue) {
                Levelonevalue.addEventListener("click", function(e) {
                    let setDatavalue = false;
                    e.preventDefault();
                    getDatavalue = this.getAttribute("data-value");
                    let getValuetext = this.querySelector(
                        "span.navigation_title"
                    ).innerText;
                    selectValueOne.querySelector("button span.text_btn").innerHTML =
                        getValuetext;
                    let getUrl = this.getAttribute("data-url");
                    if (getUrl != "") {
                        document
                            .querySelector("[data-navigation-url]")
                            .setAttribute("href", getUrl);
                    }
                    if (selectValueTwo) {
                        let ParentelementTwo = selectValueTwo.querySelector("ul");
                        if (ParentelementTwo) {
                            let LevelonevaluesTwo = ParentelementTwo.querySelectorAll(
                                "li.custom-select__option"
                            );
                            Array.from(LevelonevaluesTwo).forEach(function(LevelTwovalue) {
                                let getDatavalueTwo =
                                    LevelTwovalue.getAttribute("data-parent-handle");
                                if (getDatavalueTwo.includes(getDatavalue)) {
                                    setDatavalue = true;
                                    LevelTwovalue.style.display = "block";
                                } else {
                                    LevelTwovalue.style.display = "none";
                                    ParentelementTwo.classList.remove("active");
                                }
                                if (setDatavalue == true) {
                                    LevelTwovalue.closest(".custom-select").classList.remove(
                                        "disabled_btn"
                                    );
                                    Parentelement.classList.remove("active");
                                } else {
                                    LevelTwovalue.closest(".custom-select").classList.add(
                                        "disabled_btn"
                                    );
                                    let placeholderTextTwo = LevelTwovalue.closest(
                                            ".custom-select"
                                        )
                                        .querySelector("button span.text_btn")
                                        .getAttribute("data-placeholder-text");
                                    selectValueTwo.querySelector(
                                        "button span.text_btn"
                                    ).innerHTML = placeholderTextTwo;
                                    selectValueThree
                                        .querySelector(".custom-select")
                                        .classList.add("disabled_btn");
                                    let placeholderTextThree = selectValueThree
                                        .querySelector("button span.text_btn")
                                        .getAttribute("data-placeholder-text");
                                    selectValueThree.querySelector(
                                        "button span.text_btn"
                                    ).innerHTML = placeholderTextThree;
                                    document
                                        .querySelector("[data-navigation-url]")
                                        .classList.remove("disabled_btn");
                                }

                                LevelTwovalue.addEventListener("click", function(e) {
                                    e.preventDefault();
                                    let setsecondDatavalue = false;
                                    getDatavalueThree = this.getAttribute("data-value");
                                    let getValuetext = this.querySelector(
                                        "span.navigation_title"
                                    ).innerText;
                                    selectValueTwo.querySelector(
                                        "button span.text_btn"
                                    ).innerHTML = getValuetext;
                                    let getUrl = this.getAttribute("data-url");
                                    if (getUrl != "") {
                                        document
                                            .querySelector("[data-navigation-url]")
                                            .setAttribute("href", getUrl);
                                    }
                                    if (selectValueThree) {
                                        let ParentelementThree =
                                            selectValueThree.querySelector("ul");
                                        if (ParentelementThree) {
                                            let LevelonevaluesThree =
                                                ParentelementThree.querySelectorAll(
                                                    "li.custom-select__option"
                                                );
                                            Array.from(LevelonevaluesThree).forEach(function(
                                                LevelThreevalue
                                            ) {
                                                let parentgetDatavalueThree =
                                                    LevelThreevalue.getAttribute("data-parent-handle");
                                                if (
                                                    getDatavalueThree.includes(parentgetDatavalueThree)
                                                ) {
                                                    setsecondDatavalue = true;
                                                    LevelThreevalue.style.display = "block";
                                                } else {
                                                    LevelThreevalue.style.display = "none";
                                                    ParentelementThree.classList.remove("active");
                                                }
                                                if (setsecondDatavalue == true) {
                                                    LevelThreevalue.closest(
                                                        ".custom-select"
                                                    ).classList.remove("disabled_btn");
                                                    ParentelementTwo.classList.remove("active");
                                                } else {
                                                    LevelThreevalue.closest(
                                                        ".custom-select"
                                                    ).classList.add("disabled_btn");
                                                    document
                                                        .querySelector("[data-navigation-url]")
                                                        .classList.remove("disabled_btn");
                                                    let placeholderTextThree = selectValueThree
                                                        .querySelector("button span.text_btn")
                                                        .getAttribute("data-placeholder-text");
                                                    selectValueThree.querySelector(
                                                        "button span.text_btn"
                                                    ).innerHTML = placeholderTextThree;
                                                    document
                                                        .querySelector("[data-navigation-url]")
                                                        .classList.remove("disabled_btn");
                                                }
                                                LevelThreevalue.addEventListener("click", function(e) {
                                                    let getUrl = this.getAttribute("data-url");
                                                    if (getUrl != "") {
                                                        let getValuetext = this.querySelector(
                                                            "span.navigation_title"
                                                        ).innerText;
                                                        selectValueThree.querySelector(
                                                            "button span.text_btn"
                                                        ).innerHTML = getValuetext;
                                                        document
                                                            .querySelector("[data-navigation-url]")
                                                            .setAttribute("href", getUrl);
                                                        ParentelementThree.classList.remove("active");
                                                        document
                                                            .querySelector("[data-navigation-url]")
                                                            .classList.remove("disabled_btn");
                                                    }
                                                });
                                            });
                                        }
                                    }
                                });
                            });
                        }
                    }
                });
            });
        }
    }
}

function ageVerifiedpopup() {
    let ageVerified = getCookie("ageVerified");
    let ageVerificationParent = document.querySelector("[data-age-verification]");
    if (ageVerificationParent) {
        let ageVerificationStatus = ageVerificationParent.getAttribute(
            "data-age-verification-status"
        );
        if (
            ageVerificationStatus == "true" &&
            ageVerified != "true" &&
            window.location.pathname.indexOf("/challenge") < 0 &&
            Shopify.designMode == undefined
        ) {
            let ageVerificationContainer =
                document.querySelector(".age-verification");
            if (ageVerificationContainer) {
                ageVerificationContainer.classList.add("active");
                document.querySelector("body").classList.add("no-scroll");
            }
        }
    }
}

function closeVideoMedia(section = document, screenVisibilityCheck) {
    section.querySelectorAll(".youtube_video").forEach((video) => {
        if (
            (!isOnScreen(video) || screenVisibilityCheck == false) &&
            (video.dataset.autoplay == "false" ||
                video.classList.contains("sr-youtube-video"))
        ) {
            video.contentWindow.postMessage(
                '{"event":"command","func":"' + "pauseVideo" + '","args":""}',
                "*"
            );
        }
    });
    section.querySelectorAll(".vimeo_video").forEach((video) => {
        if (
            (!isOnScreen(video) || screenVisibilityCheck == false) &&
            (video.dataset.autoplay == "false" ||
                video.classList.contains("sr-vimeo-video"))
        ) {
            video.contentWindow.postMessage('{"method":"pause"}', "*");
        }
    });
    section.querySelectorAll("video").forEach((video) => {
        if (
            (!isOnScreen(video) || screenVisibilityCheck == false) &&
            !video.hasAttribute("autoplay")
        ) {
            video.pause();
        }
    });
}

function newsletterofferPopup() {
    let newsletterParent = document.querySelector(".newsletter-popup");
    if (newsletterParent) {
        if (
            newsletterofferFormSubmitted == true &&
            newsletterofferPopupEnable == true
        ) {
            setCookie(
                "newsletterofferPopUpClosed",
                "true",
                newsletterofferPopupExpDays
            );
        }
        let newsletterofferPopupStatus = getCookie("newsletterofferPopUpClosed");
        if (
            newsletterofferFormSubmitted == false &&
            newsletterofferPopupEnable == true &&
            newsletterofferPopupStatus != "true" &&
            window.location.pathname.indexOf("/challenge") < 0 &&
            Shopify.designMode == undefined
        ) {
            let newsletterofferPopupContainer =
                document.querySelector(".newsletter-popup");
            if (newsletterofferPopupContainer) {
                newsletterofferPopupContainer.classList.add("active");
                document.querySelector("body").classList.add("no-scroll");
            }
        }
    }
}
var DOMAnimations = {
    slideUp: function(element, duration = 500) {
        return new Promise(function(resolve, reject) {
            element.style.height = element.offsetHeight + "px";
            element.style.transitionProperty = `height, margin, padding`;
            element.style.transitionDuration = duration + "ms";
            element.offsetHeight;
            element.style.overflow = "hidden";
            element.style.height = 0;
            element.style.paddingTop = 0;
            element.style.paddingBottom = 0;
            element.style.marginTop = 0;
            element.style.marginBottom = 0;
            window.setTimeout(function() {
                element.style.display = "none";
                element.style.removeProperty("height");
                element.style.removeProperty("padding-top");
                element.style.removeProperty("padding-bottom");
                element.style.removeProperty("margin-top");
                element.style.removeProperty("margin-bottom");
                element.style.removeProperty("overflow");
                element.style.removeProperty("transition-duration");
                element.style.removeProperty("transition-property");
                resolve(false);
            }, duration);
        });
    },

    slideDown: function(element, duration = 500) {
        return new Promise(function(resolve, reject) {
            element.style.removeProperty("display");
            let display = window.getComputedStyle(element).display;

            if (display === "none") display = "block";

            element.style.display = display;
            let height = element.offsetHeight;
            element.style.overflow = "hidden";
            element.style.height = 0;
            element.style.paddingTop = 0;
            element.style.paddingBottom = 0;
            element.style.marginTop = 0;
            element.style.marginBottom = 0;
            element.offsetHeight;
            element.style.transitionProperty = `height, margin, padding`;
            element.style.transitionDuration = duration + "ms";
            element.style.height = height + "px";
            element.style.removeProperty("padding-top");
            element.style.removeProperty("padding-bottom");
            element.style.removeProperty("margin-top");
            element.style.removeProperty("margin-bottom");
            window.setTimeout(function() {
                element.style.removeProperty("height");
                element.style.removeProperty("overflow");
                element.style.removeProperty("transition-duration");
                element.style.removeProperty("transition-property");
            }, duration);
        });
    },

    slideToggle: function(element, duration = 500) {
        if (window.getComputedStyle(element).display === "none") {
            return this.slideDown(element, duration);
        } else {
            return this.slideUp(element, duration);
        }
    },

    classToggle: function(element, className) {
        if (element.classList.contains(className)) {
            element.classList.remove(className);
        } else {
            element.classList.add(className);
        }
    },
};

function toggleAccountPopup(event, accountType) {
    event.preventDefault();
    let element = event.target;
    if (accountType == "dropdown") {
        let toggleElement = document.querySelector("[data-account-dropdown]");
        if (toggleElement) {
            DOMAnimations.slideToggle(toggleElement, 250);
        }
    }
}

function toggleStoredetailsPopup(event) {
    event.preventDefault();
    let element = event.target;
    let storeDetailsElements = document.querySelectorAll("[data-storedetails-dropdown]");
    Array.from(storeDetailsElements).forEach(function(storeDetailsElement) {
        if (storeDetailsElement) {
            DOMAnimations.slideToggle(storeDetailsElement, 250);
        }

    })
    // if (window.getComputedStyle(storeDetailsElement).display == "none") {
    //     console.log('iffffff')
    //     storeDetailsElement.style.display = 'block';
    // } else {
    //     console.log('elseeee')
    //     storeDetailsElement.style.display = 'none';
    // }
    // console.log(storeDetailsElement)
    
}

function toggleForm(event) {
    event.preventDefault();
    let element = event.target;
    let elementParent = element.closest(".customer-account-popup");
    let closeElement = elementParent.querySelector("#" + element.dataset.close);
    let openElement = elementParent.querySelector("#" + element.dataset.open);
    if (openElement && closeElement) {
        closeElement.style.display = "none";
        openElement.style.display = "block";
    }
}

function closeDropdowns() {
    var mouse_is_insides = false;
    const accountDropdownElements = document.querySelectorAll(
        "[data-account-dropdown], .header-icons-link.account, [data-storedetails-dropdown], .support-content-wrapper"
    );
    accountDropdownElements.forEach((accountDropdownElement) => {
        accountDropdownElement.addEventListener("mouseover", () => {
            mouse_is_insides = true;
        });

        accountDropdownElement.addEventListener("mouseout", () => {
            mouse_is_insides = false;
        });
    });
    document.body.addEventListener("click", () => {
        if (!mouse_is_insides) {
            if (document.querySelector("[data-account-dropdown]")) {
                DOMAnimations.slideUp(
                    document.querySelector("[data-account-dropdown]")
                );
            }
            let storeDetailsElements = document.querySelectorAll("[data-storedetails-dropdown]");
            Array.from(storeDetailsElements).forEach(function(storeDetailsElement) {
                if (storeDetailsElement) {
                    DOMAnimations.slideUp(storeDetailsElement);
                }
            })
        }
    });
}

function imagesBanner(section = document) {
    let bannerSelector = section.querySelectorAll("[data-banner-text]");
    Array.from(bannerSelector).forEach(function(bannerSelector) {
        let parentSection = bannerSelector.closest(".shopify-section");
        bannerSelector.addEventListener("mouseover", function(e) {
            let textAttribute = bannerSelector.dataset.blockId;
            let activeImageSelector = parentSection.querySelector(
                `[data-banner-image].active`
            );
            let currentImageSelector = parentSection.querySelector(
                `[data-banner-image][data-block-id="${textAttribute}"]`
            );
            let activeTextSelector = parentSection.querySelector(
                `[data-banner-text].active`
            );
            let currentTextSelector = parentSection.querySelector(
                `[data-banner-text][data-block-id="${textAttribute}"]`
            );
            if (currentImageSelector) {
                if (activeImageSelector) {
                    activeImageSelector.classList.remove("active");
                }
                currentImageSelector.classList.add("active");
            }
            if (currentTextSelector) {
                if (activeTextSelector) {
                    activeTextSelector.classList.remove("active");
                }
                currentTextSelector.classList.add("active");
            }
        });
    });
}

document.addEventListener("scroll", function() {
    announementHeightOnScroll();
    closeVideoMedia();
    if (
        document.body.scrollTop > 300 ||
        document.documentElement.scrollTop > 300
    ) {
        if (document.querySelector(".compare-btn-sidebar")) {
            document.querySelector(".compare-btn-sidebar").classList.add("show");
        }
    } else {
        if (document.querySelector(".compare-btn-sidebar")) {
            document.querySelector(".compare-btn-sidebar").classList.remove("show");
        }
    }
});
document.addEventListener("resize", function() {
    productCardHoverInit();
});

function stickyAddToCartInit(section = document) {
    let mainProductForm = section.querySelector(
        '.product-content-wrapper .shopify-product-form[action^="' + cartAdd + '"]'
    );
    if (mainProductForm) {
        let formScrollTop = mainProductForm.offsetTop + 500;
        let stickyBar = section.querySelector("[data-sticky-products]");
        if (stickyBar) {
            window.addEventListener("scroll", function(event) {
                if (isOnScreen(mainProductForm, true) || window.scrollY < formScrollTop) {
                    stickyBar.classList.remove("sticky-visible");
                } else {
                    stickyBar.classList.add("sticky-visible");
                }
            });
        }
    }
}

function stickyProductContentSlide(section = document) {
    if (section.querySelector("[data-sticky-options-btn")) {
        let stcikyIcon = section.querySelector("[data-sticky-options-btn]");
        let StickyContent = document.querySelector("[data-sticky-options]");
        let stickyBar = section.querySelector("[data-sticky-products]");
        stcikyIcon.addEventListener("click", (e) => {

            if (stcikyIcon.classList.contains("active")) {
                stcikyIcon.classList.remove("active");
            } else {
                stcikyIcon.classList.add("active");
            }
            DOMAnimations.slideToggle(StickyContent, 500);
        });
        if (stickyBar.querySelector('[data-sticky-product-close]')) {
            stickyBar.querySelector('[data-sticky-product-close]').addEventListener('click', function(event) {
                event.preventDefault();
                if (stickyBar.classList.contains("sticky-visible")) {
                    stickyBar.classList.remove("sticky-visible");
                    setTimeout(function() {
                        stickyBar.style.display = 'none';
                    }, 400)
                }
            })
        }
    }
}

function categoriesSidebar() {
    let categoriesButton = document.querySelector("[data-categories-btn]");
    let categoriesWrapper = document.querySelector("[data-categories-wrapper]");
    let categoriesClosebutton = document.querySelector("[data-categories-close]");
    let sidebarOverlay = document.querySelector("[data-sidebar-overlay]");
    if (categoriesButton) {
        categoriesButton.addEventListener("click", function(event) {
            event.preventDefault();
            this.closest("[data-categories-wrapper]").classList.add("active");
            document.querySelector("body").classList.add("sidebar-category-overlay");
        });
    }
    if (categoriesClosebutton) {
        categoriesClosebutton.addEventListener("click", function(event) {
            event.preventDefault();
            let categoriesWrapperActive = document.querySelector(
                "[data-categories-wrapper].active"
            );
            if (categoriesWrapper.classList.contains("active")) {
                setTimeout(function() {
                    if (categoriesWrapperActive) {
                        categoriesWrapperActive.classList.remove("active");
                    }
                    if (document.querySelector("body.sidebar-category-overlay")) {
                        document
                            .querySelector("body.sidebar-category-overlay")
                            .classList.remove("sidebar-category-overlay");
                    }
                }, 100);
            }
        });
    }
    if (sidebarOverlay) {
        sidebarOverlay.addEventListener("click", function(event) {
            event.preventDefault();
            categoriesClosebutton.click();
        });
    }
}

function headerHamburgerMenu(section = document) {
    if (document.querySelector("[data-hamburger-menu]")) {
        let hamburgerheader = document.querySelector("[data-hamburger-menu]");

        hamburgerheader.addEventListener("click", function(event) {
            event.preventDefault();
            // hamburgerheader.closest("header").style.zIndex =100;
            let hamburgerBodyElement = hamburgerheader.getAttribute("href");
            let hamburgerBody = document.querySelector(hamburgerBodyElement);
            let menuStatus = 'close';
            if (hamburgerBody) {
                if (!hamburgerBody.classList.contains("is-visible")) {

                    hamburgerBody.style.display = 'block';
                    document.body.classList.add("hamburger-open");
                    document.body.classList.add("no-scroll");

                    let menuitems = hamburgerBody.querySelectorAll("[data-menu-items]");
                    setTimeout(() => {
                        hamburgerBody.classList.add("is-visible");
                        menuStatus = 'open'
                    }, 200);
                    setTimeout(() => {
                        if (menuStatus == 'open') {
                            Array.from(menuitems).forEach(function(menuitem) {
                                menuitem.classList.add("animation")
                                setTimeout(function() {
                                    menuitem.classList.add("animated")
                                }, 100)
                            })
                        }
                    }, 700);
                    previousFocusElement = hamburgerBody;
                    focusElementsRotation(hamburgerBody);
                }
            }
        })

        let hamburgerMenuCloses = document.querySelectorAll("[data-hamburger-menu-close]");
        Array.from(hamburgerMenuCloses).forEach(function(hamburgerMenuClose) {

            hamburgerMenuClose.addEventListener("click", function(event) {
                event.preventDefault();
                // hamburgerMenuClose.closest("header").style.zIndex =6;
                let hamburgerBodyElement = document.querySelector("[data-humburger-body]")
                setTimeout(() => {
                    hamburgerBodyElement.style.display = 'none';
                    let menuitems = hamburgerBodyElement.querySelectorAll("[data-menu-items]");
                    Array.from(menuitems).forEach(function(menuitem) {
                        menuitem.classList.remove("animation", "animated")
                    })
                }, 500);
                document.body.classList.remove("hamburger-open", "no-scroll");
                hamburgerBodyElement.classList.remove("is-visible");
            })
        })

    }
}


function hamburgerHoverMenu() {
    let hamburgerMenuItems = document.querySelectorAll("[data-menu-items]");
    Array.from(hamburgerMenuItems).forEach(function(hamburgerMenuItem) {
        if (hamburgerMenuItem) {
            hamburgerMenuItem.addEventListener("mouseover", function(event) {
                hamburgerMenuItem.classList.add("active");
                if (hamburgerMenuItem.querySelector(".dropdown-menus-main")) {
                    hamburgerMenuItem.querySelector(".dropdown-menus-main").classList.add("active");
                }
            })

            hamburgerMenuItem.addEventListener("mouseleave", function(event) {
                hamburgerMenuItem.classList.remove("active");
                if (hamburgerMenuItem.querySelector(".dropdown-menus-main")) {
                    hamburgerMenuItem.querySelector(".dropdown-menus-main").classList.remove("active");
                }
            })
        }
    })

    let hamburgerSubmenuItems = document.querySelectorAll("[data-menu-dropdown]");
    Array.from(hamburgerSubmenuItems).forEach(function(hamburgerSubmenuItem) {
        if (hamburgerSubmenuItem) {
            hamburgerSubmenuItem.addEventListener("click", function(event) {
                if (hamburgerSubmenuItem.closest(".dropdown-menus-inner").classList.contains("active")) {
                    hamburgerSubmenuItem.closest(".dropdown-menus-inner").classList.remove("active");
                } else {
                    hamburgerSubmenuItem.closest(".dropdown-menus-inner").classList.add("active")
                }
            })
        }

    })

}

function initBeforeAfter(section = document) {
    let cursors = section.querySelectorAll("#before-after-cursor-point");
    Array.from(cursors).forEach(function(cursor) {
        beforeAfterImage(cursor);
    });
}

function beforeAfterImage(cursor) {
    let parentSection = cursor.closest(".shopify-section");
    if (!cursor.offsetParent) {
        return false;
    }
    cursor.addEventListener("input", function() {
        let firstImage = parentSection.querySelector(".before-after-main-image");
        firstImage.style.clipPath = `polygon(0 0, ${this.value}% 0, ${this.value}% 100%, 0% 100%)`;
        firstImage.closest(".before-after-wrapper").style.setProperty("--position", this.value + "%");
    });

}

function windowResize() {
    window.addEventListener("resize", function() {
        setTimeout(function() {
            initBeforeAfter();

        }, 500);
    });
}

function imageWithCarousel(section = document) {
    const features = document.querySelectorAll(".image-with-text-content");
    let totalcount = features.length - 1;
    observer = new IntersectionObserver(
        (wrappers) => {
            wrappers.forEach((wrapper) => {
                let element = wrapper.target;
                if (wrapper.intersectionRatio > 0.7) {
                    let parentSection = element.closest(".shopify-section");
                    let index = element.getAttribute("data-card");

                    if (index != 0) {
                        index = index - 1;
                        parentSection
                            .querySelector('[data-card="' + index + '"]')
                            .classList.add("show-feature");
                    }
                    if (totalcount == index + 1) {
                        element.classList.add("show-feature");
                    }
                } else {
                    element.classList.remove("show-feature");
                }
            });
        }, { threshold: 0.7 }
    );
    features.forEach((feature) => observer.observe(feature));
}

function addMultiplier(section = document) {
    let productWrappers = section.querySelectorAll("[data-product-wrapper]");
    Array.from(productWrappers).forEach(function(productWrapper) {
        let multiplierValues = productWrapper.querySelectorAll(
            "[data-add-multiplier]"
        );
        Array.from(multiplierValues).forEach(function(multiplier) {
            if (multiplier) {
                multiplier.addEventListener("click", function(event) {
                    event.preventDefault();
                    let quantityValue = parseInt(this.getAttribute("data-value"));
                    multiplier
                        .closest("[data-product-wrapper]")
                        .querySelector("[data-quantity-input]").value = quantityValue;
                  if(multiplier.closest("[data-product-wrapper]").querySelector("#sticky_quantity")){
                    multiplier.closest("[data-product-wrapper]").querySelector("#sticky_quantity").value = quantityValue;
                  }
                    setTimeout(function() {
                        multiplier
                            .closest("[data-product-wrapper]")
                            .querySelector("[data-add-to-cart]")
                            .click();
                    }, 100);
                });
            }
        });
    });
}

function productTermhandler() {
    let productTerms = document.querySelectorAll("[data-product-terms]");
    if (productTerms) {
        Array.from(productTerms).forEach(function(productTerm) {
            productTerm.addEventListener("click", function(event) {
                if (productTerm.checked) {
                    if(productTerm.closest(".shopify-section").querySelector(".pdp-form-action-wrapper [data-add-to-cart]")){
                        productTerm.closest(".shopify-section").querySelector(".pdp-form-action-wrapper [data-add-to-cart]").removeAttribute("disabled");
                    }
                    if(productTerm.closest(".shopify-section").querySelector(".product_form_wrapper [data-add-to-cart]")){
                        productTerm.closest(".shopify-section").querySelector(".product_form_wrapper [data-add-to-cart]").removeAttribute("disabled");
                    }
                    if (productTerm.closest(".shopify-section").querySelector(".product-add-to-cart-sticky-content")
                    ) {
                        productTerm.closest(".shopify-section").querySelector(".product-add-to-cart-sticky-content [data-add-to-cart]").removeAttribute("disabled");
                        // productTerm.closest(".shopify-section").querySelector(".product-add-to-cart-sticky-content [data-product-terms]").setAttribute("checked",true);
                        // productTerm.closest(".shopify-section").querySelector(".pdp-form-action-wrapper [data-product-terms]").setAttribute("checked",true);

                        productTerm.closest(".shopify-section").querySelector(".product-add-to-cart-sticky-content [data-product-terms]").checked = true;
                        productTerm.closest(".shopify-section").querySelector(".pdp-form-action-wrapper [data-product-terms]").checked = true;
                    }
                } else {
                    if(productTerm.closest(".shopify-section").querySelector(".pdp-form-action-wrapper [data-add-to-cart]")){
                        productTerm.closest(".shopify-section").querySelector(".pdp-form-action-wrapper [data-add-to-cart]").setAttribute("disabled", true);
                    }
                    if(productTerm.closest(".shopify-section").querySelector(".product_form_wrapper [data-add-to-cart]")){
                        productTerm.closest(".shopify-section").querySelector(".product_form_wrapper [data-add-to-cart]").setAttribute("disabled", true);
                    }
                    if (
                        productTerm
                        .closest(".shopify-section")
                        .querySelector(".product-add-to-cart-sticky-content")
                    ) {
                        productTerm
                            .closest(".shopify-section")
                            .querySelector(
                                ".product-add-to-cart-sticky-content [data-add-to-cart]"
                            )
                            .setAttribute("disabled", true);
                            // productTerm.closest(".shopify-section").querySelector(".product-add-to-cart-sticky-content [data-product-terms]").removeAttribute("checked");
                            // productTerm.closest(".shopify-section").querySelector(".pdp-form-action-wrapper [data-product-terms]").removeAttribute("checked");

                            productTerm.closest(".shopify-section").querySelector(".product-add-to-cart-sticky-content [data-product-terms]").checked = false;
                            productTerm.closest(".shopify-section").querySelector(".pdp-form-action-wrapper [data-product-terms]").checked = false;
                            
                    }
                }
           
            });
        });
    }
}
let badgesInterval = bdageAnimationSeconds * 1000 + 500;

function badgesAnimation(section = document) {
    let getBadges = section.querySelectorAll(".product-card-badges");
    Array.from(getBadges).forEach(function(getBadge) {
        let badgeIndex = 0;
        let customBadges = getBadge.querySelectorAll(".custom-badge");
        if (customBadges.length > 1) {
            Array.from(customBadges).forEach(function(custombadge, index) {
                if (index != 0) {
                    custombadge.style.display = "none";
                }
            });
            setInterval(function() {
                customBadges[badgeIndex].fadeOut(500);
                badgeIndex = badgeIndex + 1;
                if (badgeIndex >= customBadges.length) {
                    badgeIndex = 0;
                }
                setTimeout(function() {
                    customBadges[badgeIndex].fadeIn(500);
                }, 550);
            }, badgesInterval);
        }
    });
}
class DeferredMedia extends HTMLElement {
    constructor() {
        super();
        let loadBtn='';
        if(this.closest(".product-gallery-img-item")){
            loadBtn = this.closest(".product-gallery-img-item").querySelector('.js-load-media');
        }else{
            if(this.closest(".shopify-section")){
                loadBtn = this.closest(".shopify-section").querySelector(".js-load-media");
            }            
        }
   
        // const loadBtn = this.closest(".shopify-section").querySelector(".js-load-media");
        if (loadBtn) {
            loadBtn.addEventListener("click", this.loadContent.bind(this));
        } else {
            this.addObserver();
        }
    }
    addObserver() {
        if ("IntersectionObserver" in window === false) return;
        const observer = new IntersectionObserver(
            (entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        // this.loadContent(false, false, 'observer');
                        this.loadContent();
                        observer.unobserve(this);
                    }
                });
            }, { rootMargin: "0px 0px 900px 0px" }
        );
        observer.observe(this);
    }
    loadContent() {
        if (!this.querySelector("template")) return false;
        const content =
            this.querySelector("template").content.firstElementChild.cloneNode(true);
            
        this.appendChild(content);
        if (this.dataset.type == "youtube") {
            onYouTubeIframeAPIReady(this.closest(".shopify-section"));
        }

        if (this.querySelector("video") && (this.querySelector("video").hasAttribute("autoplay") || this.querySelector("video").hasAttribute("data-autoplay") ) || this.querySelector("video") &&(this.querySelector("video").classList.contains("local_videos"))) {
            this.querySelector("video").play();
        }
        let placeholderMedia = this.querySelector(".deferred-media-placeholder");
        if (placeholderMedia) {
            if (this.dataset.type == "vimeo") {
                setTimeout(function() {
                    placeholderMedia.style.display = 'none';
                }, 2000)
            }
            if (this.querySelector("video")) {
                this.querySelector("video").addEventListener("playing", function() {
                    placeholderMedia.style.display = 'none';
                });
            }

            if (this.parentElement.classList.contains('parallax-image')) {
                new universalParallax(this).init({
                    speed: 10
                });
            }
        }
    }
}
customElements.define("deferred-media", DeferredMedia);

class DeferredSlider extends HTMLElement {
    constructor() {
        super();
        this.addObserver();
    }
    addObserver() {
        if ("IntersectionObserver" in window === false) return;
        const observer = new IntersectionObserver(
            (entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        // this.loadContent(false, false, 'observer');
                        this.loadContent();
                        observer.unobserve(this);
                    }
                });
            }, { rootMargin: "0px 0px 700px 0px" }
        );
        observer.observe(this);
    }
    loadContent() {
        if (!this.querySelector("template")) return false;
        const content = this.querySelector("template").content.firstElementChild.cloneNode(true);
        this.appendChild(content);
        slideshowElements(this);
        customSliderArrowsEvents(this);
        quickviewElements(this);
        getCountDownElments(this);
        collectionSwatch(this);
        productCardHoverInit(this);
        badgesAnimation(this);
        if (aosAnimation) {
            if (AOS) {
                AOS.refreshHard();
            }
        }

    }
}
customElements.define("deferred-slider", DeferredSlider);

var lastScrollTopValue = 0;
class Timeline extends HTMLElement{
    constructor(){
        super();
        window.addEventListener('scroll',  this.timelineOnScrollHandler.bind(this))
       
    }
    
    timelineOnScrollHandler(){
        let thisSection = this;
        this.contentItems = this.querySelectorAll("[data-content-item]");
        var st = window.pageYOffset || document.documentElement.scrollTop; 
        Array.from(this.contentItems).forEach(function(contentItem){
            const center=  window.innerHeight / 2
            const { top, bottom } =contentItem.querySelector(".timeline-content-text").getBoundingClientRect();
            if (st > lastScrollTopValue){
                if(center > top &&  bottom>0 ){
                    if(contentItem.querySelector(".timeline-image").classList.contains("active"))return false;
                    if(thisSection.querySelector(".timeline-image.active")){
                        thisSection.querySelector(".timeline-image.active").classList.remove("active")
                    }
                    contentItem.querySelector(".timeline-image").classList.add("active")
                }
            }else{
                if(top < center &&  bottom > center ){
                    let dataIndex = contentItem.getAttribute("data-id");
                    dataIndex = parseInt(dataIndex) + 1
                    if(contentItem.querySelector(".timeline-image").classList.contains("active"))return false;
                    if(thisSection.querySelector(".timeline-image.active")){
                        thisSection.querySelector(".timeline-image.active").classList.remove("active")
                    }
                    contentItem.querySelector(".timeline-image").classList.add("active")
                    
                }
            }
          

        }) 
        lastScrollTopValue = st; 
    }
    
}
customElements.define("time-line-content", Timeline);
function markeranimation(section = document) {
    let markervalue = section.querySelectorAll('.marker-svg path');
    Array.from(markervalue).forEach(function(marker) {
        if (isOnScreen(marker)) {
            if (marker.closest(".marker-svg")) {
                setTimeout(function() {
                    marker.closest(".marker-svg").classList.add("marker-animation")
                }, 500)

            }

        }
    })
}

function announcementSocialWidth(){
    let socialMediaIcons = document.querySelector(".announcement-bar-left");
    if(socialMediaIcons){
    let socialiconsinnerwidth = socialMediaIcons.offsetWidth;
    let body_element = document.querySelector("body");
    body_element.style.setProperty('--announce-social-width',socialiconsinnerwidth+'px');
    }
  }

window.addEventListener('scroll', function() {
    sectionLoadSelector();
});

function sectionLoadSelector(){
    document.querySelectorAll("section").forEach((section) => {
        let markervalue = section.querySelectorAll('.marker-svg path');
        Array.from(markervalue).forEach(function(marker) {
            if (isOnScreen(marker)) {
                if (marker.closest(".marker-svg")) {
                    setTimeout(function() {
                        marker.closest(".marker-svg").classList.add("marker-animation")
                    }, 500)

                }

            }
        });
        if (isOnScreen(section)) {
            if (section.classList.contains("before-after-image")) {
                setTimeout(function() {
                    if (!section.classList.contains('section-in-view')) {
                        section.querySelector(".before-after-wrapper").classList.add("animating")
                        setTimeout(function() {
                            section.querySelector(".before-after-wrapper").classList.remove("animating")
                        }, 1000)
                    }
                    section.classList.add("section-in-view");

                }, 1000)
            } else {
                setTimeout(function() {
                    section.classList.add("section-in-view");
                }, 500)
            }

        }
    });
}

document.addEventListener("DOMContentLoaded", function() {
    onloadEvents();  
    onloadVariants();
});
function onloadEvents(){
    announementHeightOnScroll();
    videoPlayInit();
    // stickyformqty();
    toggleVideoAudio();
    announcementSocialWidth();
    slideshowElements();
    menuDropdown();
    mobileNavigation();
    compareBarViewToggle();
    search_drawer();
    variant_selector();
    bundleProductInit();
    get_header_height();
    quickviewElements();
    footerDropdownCheck();
    search_drawer_tab();
    accordion();
    cartNoteUpdate();
    collectionSwatch();
    customSliderArrowsEvents();
    getCountDownElments();
    marqueeTextAutoplay();
    initStoreLocator();
    getAllDetails();
    onHoverMenuElements();
    headerNavigationPosition();
    customDropdownElements();
    let observer = new IntersectionObserver(function(entries) {
        let ele = entries.filter((entry) => entry.isIntersecting);
        let body_element = document.querySelector("body");
        if (ele.length > 0) {
            ele = ele[0].target;
            body_element.classList.add("overflow-hidden");
        } else {
            body_element.classList.remove("overflow-hidden");
        }
    });
    lookbook();
    vertical_scroll();
    getcollageElments();
    detailDisclouserInit();
    tab_media_item();
    videoBanner();
    initHotspot();
    testimonialInit();
    SidedrawerEventInit();
    productRecommendations();
    recentlyViewedProducts();
    thumbnailChange();
    mp4VideoReady();
    vimeoVideoReady();
    outSideClickTrigger();
    collectionCarousal();
    collectionTabs();
    scrollTop();
    announcementCollapsiblecontent();
    checkedboxCookies();
    CloseCompareModel();
    showMoremedia();
    colorMode();
    productGiftOptions();
    quickNav();
    ageVerifiedpopup();
    //newsletterPopup();
    newsletterofferPopup();
    productCardHoverInit();
    closeDropdowns();
    featuredImages();
    revealCollection();
    imagesBanner();
    cartTermhandlerClick();
    stickyFooterInit();
    needHelpTabs();
    cartTermsHandler();
    stickyProductContentSlide();
    stickyAddToCartInit();
    stickyProductOptions();
    categoriesSidebar();
    initBeforeAfter();
    windowResize();
    addMultiplier();
    imageWithCarousel();
    productTermhandler();
    badgesAnimation();
    headerHamburgerMenu();
    hamburgerHoverMenu();
    markeranimation();
    sectionLoadSelector();
    if (aosAnimation) {
        if (AOS) {
            AOS.refreshHard();
        }
    }
}
function revealCollection(section = document) {
    let revealSelector = section.querySelectorAll("[data-reveal]");
    Array.from(revealSelector).forEach(function(revealSelector) {
        revealSelector.addEventListener("mouseover", function(e) {
            if (window.innerWidth < 768) return false;
            let revealImageSelector = revealSelector.querySelector(
                "[data-reveal-image]"
            );
            if (revealImageSelector) {
                revealSelector.classList.add("active");
                revealImageSelector.classList.add("active");
            }
        });
        revealSelector.addEventListener("mousemove", function(e) {
            if (window.innerWidth < 768) return false;
            let revealImageSelector = revealSelector.querySelector("img");
            if (revealImageSelector) {
                let position = getMousePos(e);
                let x = position.x - revealSelector.offsetWidth / 2;
                let y = position.y - revealSelector.offsetHeight / 2;
                revealImageSelector.style.translate = `${x}px ${y}px`;
            }
        });
        revealSelector.addEventListener("mouseout", function(e) {
            if (window.innerWidth < 768) return false;
            let revealImageSelector = revealSelector.querySelector(
                "[data-reveal-image]"
            );
            if (revealImageSelector) {
                revealSelector.classList.remove("active");
                revealImageSelector.classList.remove("active");
                setTimeout(function() {
                    revealImageSelector.style.translate = `0px 0px`;
                }, 500);
            }
        });
    });
}

function toggleVideoAudio(section = document) {
    let toggleSelectors = section.querySelectorAll("[data-video-audio]");
    Array.from(toggleSelectors).forEach(function(element) {
        element.addEventListener("click", function(e) {
            let parent = element.closest(".short-video-content");
            if (parent.querySelector("video")) {
                if (element.classList.contains("active")) {
                    element.classList.remove("active");
                    parent.querySelector("video").muted = true;
                } else {
                    element.classList.add("active");
                    parent.querySelector("video").muted = false;
                }
            }
        });
    });
}

function cartTermhandlerClick() {
    let cartTerms = document.querySelector("[data-cart-terms]");
    if (cartTerms) {
        cartTerms.addEventListener("click", function(event) {
            cartTermsHandler();
        });
    }
}

function cartTermsHandler() {
    let cartTerms = document.querySelector("[data-cart-terms]");
    if (cartTerms) {
        if (cartTerms.checked) {
            cartTerms
                .closest("[data-cart-wrapper]")
                .querySelector('[name="checkout"]')
                .removeAttribute("disabled");
        } else {
            cartTerms
                .closest("[data-cart-wrapper]")
                .querySelector('[name="checkout"]')
                .setAttribute("disabled", true);
        }
    }
}
if (typeof ImageWithTextCarousel !== 'function') {
    class ImageWithTextCarousel extends HTMLElement {
        constructor() {
            super();
            this.init();
        }

        init() {
            this.slides = [];
            this.slide = 0;
            this.querySelectorAll('.image-with-text-content').forEach(elm => {
                this.slides.push({
                    parent: elm,
                    children: elm.querySelector('.row'),
                    media: elm.querySelectorAll('.image-with-text-image-wrapper'),
                    text: elm.querySelector('.image-with-text-carousel-content')
                })
            });
            this.zoomEffect = true;
            this.paralex = false;


            this.slideRaf = true;

            this.onScrollHandler = (() => {
                if (this.slideRaf) {
                    this.slideRaf = false;
                    if(this.slides.length > 0){  // added code for removing console errors 
                       requestAnimationFrame(this.CarouselAnimation.bind(this));
                    }
                }
            }).bind(this);
            window.addEventListener('scroll', this.onScrollHandler, { passive: true });
            window.addEventListener('resize', this.onScrollHandler, { passive: true });
            this.onScrollHandler();

        }


        CarouselAnimation(e) {
                const sliderOffset = this.parentElement.getBoundingClientRect().y + window.scrollY,
                    scrollTop = window.scrollY,
                    sliderHeight = Math.min(this.slides[0].children.offsetHeight, window.innerHeight + (!this.classList.contains('vertical-slider--no-padding') ? (10 * 2) : 0) - 0);
                this.parentElement.classList.add('has-children-' + this.slides.length);
                this.slides.forEach((item, i) => {
                            let slideY = (scrollTop - sliderOffset + (window.innerHeight - sliderHeight)) - (sliderHeight * i),
                                slideYXZ = slideY - (window.innerHeight - sliderHeight);
                            if (item.media[0] && item.parent.getBoundingClientRect().y < window.innerHeight && item.parent.getBoundingClientRect().y > -window.innerHeight) {
                                if (scrollTop <= sliderOffset) {
                                    if (i == 0 || (item.parent.getBoundingClientRect().y + item.parent.offsetHeight <= window.innerHeight)) {
                                        if (this.classList.contains('fullwidth-wrapper')) {
                                            item.media.forEach(elm => {
                                                        elm.style.transform = `${this.paralex ? `translateY(0)` : ''}`;
              });
              }else{
              item.media.forEach(elm=>{
                elm.style.transform = `${this.zoomEffect ? `scale(1)` : ''} ${this.paralex ? `translateY(0)` : ''}`;
              });
              item.children.style.transform = `scale(1)`;
              }
            } else {
              if(this.classList.contains('fullwidth-wrapper')){
                item.media.forEach(elm=>{
                  const mediaScale = (100 - (slideY * 100 / sliderHeight) / 12);
                  elm.style.transform = `${this.paralex ? `translateY(${mediaScale <= 100 ? 0 : slideY/2}px)` : ''}`;
                });
              }else{
                item.media.forEach(elm=>{
                  const mediaScale = (100 - (slideY * 100 / sliderHeight) / 12);
                  elm.style.transform = `${this.zoomEffect ? `scale(${Math.max(100, mediaScale)}%)` : ''} ${this.paralex ? `translateY(${mediaScale <= 100 ? 0 : slideY/2}px)` : ''}`;
                });
                item.children.style.transform = `${this.zoomEffect ? `scale(1)` : ''}`;                
              }
            }
          } else if ( slideY < 0 ) {
            if(this.classList.contains('fullwidth-wrapper')){
              item.media.forEach(elm=>{
                elm.style.transform = `${this.paralex ? `translateY(${slideY/2}px)` : ''}`;
              });
            }else{
              item.media.forEach(elm=>{
                elm.style.transform = `${this.zoomEffect ? `scale(${(100 - (slideY * 100 / sliderHeight) / 12)}%)` : ''} ${this.paralex ? `translateY(${slideY/2}px)` : ''}`;
              });
            }
          } else if ( slideY >= 0 && slideYXZ <= 0 ) {
            if(this.classList.contains('fullwidth-wrapper')){
              item.media.forEach(elm=>{
                elm.style.transform = `${this.paralex ? `translateY(0)` : ''}`;
              });
            }else{
              item.media.forEach(elm=>{
                elm.style.transform = `${this.zoomEffect ? `scale(1)` : ''} ${this.paralex ? `translateY(0)` : ''}`;
              });
              item.children.style.transform = `${this.zoomEffect ? `scale(1)` : ''}`;
            }
          } else if ( slideYXZ > 0 && i != this.slides.length - 1 ) {
            if(this.classList.contains('fullwidth-wrapper')){
              item.media.forEach(elm=>{
                elm.style.transform = `${this.paralex ? `translateY(${-slideYXZ/4}px)` : ''}`;
              });
            }else{
              item.media.forEach(elm=>{
                elm.style.transform = `${this.paralex ? `translateY(${-slideYXZ/4}px)` : ''}`;
              });
               item.children.style.transform = `${this.zoomEffect ? `scale(${(100 - (slideYXZ * 100 / sliderHeight) / 40)}%)` : ''}`;
            }
          } 
        }
      });

      this.slideRaf = true;

    }

  }

  if ( typeof customElements.get('image-with-text-carousel') == 'undefined' ) {
   customElements.define('image-with-text-carousel', ImageWithTextCarousel);
  }
}


function needHelpTabs(section = document){
  let tabHeadings = section.querySelectorAll('[data-help-tab]');
  Array.from(tabHeadings).forEach(function(tabHead){
    tabHead.addEventListener('click',function(){
      if(tabHead.classList.contains('active')) return false;
      let helpTabWrapper = tabHead.closest('[data-help-tab-wrapper]')
      if(helpTabWrapper){
        let helpTabContent = helpTabWrapper.querySelector('#' + tabHead.dataset.tab);
        if(helpTabContent){
          let activeTabContent = helpTabWrapper.querySelector('.help-list-tab-content-item.active');
          if(activeTabContent){
            activeTabContent.classList.remove('active');
            activeTabContent.fadeOut(100)
          }
          let activeTabHead = helpTabWrapper.querySelector('.help-list-tab-item.active');
          if(activeTabHead){
            activeTabHead.classList.remove('active');
          }
          tabHead.classList.add('active');
          helpTabContent.classList.add('active');
          setTimeout(() => {
            helpTabContent.fadeIn(300)
          }, 200);
        }
      }
    })
  })
}

function stickyFooterInit(section = document) {
  const stickyFooter = section.querySelector("[data-footer-sticky]");
  if(stickyFooter){
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            document.body.classList.add('footer-sticky');
            observer.unobserve(stickyFooter);
          }
        });
      },
      { rootMargin: `0px 0px ${document.body.scrollHeight / 3}px 0px` }
    );
    observer.observe(stickyFooter)
  }
}





function footerDropdownCheck(){
  window.addEventListener("scroll", function () {
    let windowCenter = window.innerHeight / 2;
    if (document.querySelector('.footer-bottom')) {
      let elementScrollTop = document.querySelector('.footer-bottom').getBoundingClientRect().top;
      if (isOnScreen(document.querySelector('.footer-bottom'))) {
        if(elementScrollTop < windowCenter){
          document.querySelector('.footer-bottom').classList.add('bottom')
        }
        else{
          document.querySelector('.footer-bottom').classList.remove('bottom')
        }
      }
    }
    if (document.querySelector('.footer-newsletter-localization')) {
        let elementScrollTop = document.querySelector('.footer-newsletter-localization').getBoundingClientRect().top;
        if (isOnScreen(document.querySelector('.footer-newsletter-localization'))) {
          if(elementScrollTop < windowCenter){
            document.querySelector('.footer-newsletter-localization').classList.add('bottom')
          }
          else{
            document.querySelector('.footer-newsletter-localization').classList.remove('bottom')
          }
        }
      }
  });
}


class OdoMeter extends HTMLElement {
    constructor() {
        super();
        this.addObserver();
    }

    addObserver() {
        if ('IntersectionObserver' in window === false) return;
        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    this.loadContent();
                    observer.unobserve(this);
                }
            });
        }, { rootMargin: '0px 0px -300px 0px' });

        observer.observe(this);
    }

    loadContent() {
        let $el = $(this);
        $({ Counter: 0 }).animate({ Counter: $el.data('counter') }, {
            duration: 2000,
            easing: 'swing',
            step: function() {
                $el.text(Math.ceil(this.Counter));
            },
            complete: function() {
                $el.text($el.data('counter'));
            }

        });
    }
}

customElements.define('odo-meter', OdoMeter);

/*class CategorisList extends HTMLElement {
    constructor() {
        super();
        Array.from(this.querySelectorAll('[data-content-item]')).map((dataItem) => {
            dataItem.addEventListener('mouseover', this.onActionHandler.bind(this, dataItem));
        });

    }
    onActionHandler(eventItem) {
        console.log("this", this, eventItem)
        const section = this.closest('section');

        const dataContentItems = this.querySelectorAll('[data-content-item]')
        
        if(eventItem.classList.contains('active')) return;
        Array.from(this.querySelectorAll('[data-content-item]')).map((item) => {
            item.classList.remove('active');
        });

        Array.from(this.querySelectorAll('[data-image-item]')).map((item) => {
            item.classList.remove('active');
        });

        eventItem.classList.add('active');
        
        section.querySelector(`[data-image-item="categories-image-item-${eventItem.dataset.contentItem}"]`).classList.add('active');
    }
}
customElements.define('categories-list', CategorisList);*/



class CategorisList extends HTMLElement {
    constructor() {
        super();
        Array.from(this.querySelectorAll('[data-content-item]')).forEach((dataItem) => {
            dataItem.addEventListener('mouseover', this.onActionHandler.bind(this, dataItem));
        });
    }

    onActionHandler(eventItem) {
        const section = this.closest('section');

        
        
        if (eventItem.classList.contains('active')) return;

        // Find the currently active item and add the 'processing' class
        const activeItem = this.querySelector('[data-image-item].active');
        if (activeItem) {
            activeItem.classList.remove('active');
            activeItem.classList.add('processing');
            setTimeout(() => {
                activeItem.classList.remove('processing');
                
            }, 400);
        }

        // Remove 'active' class from all content items
        Array.from(this.querySelectorAll('[data-content-item]')).forEach((item) => {
            item.classList.remove('active');
           
        });

        // Add 'active' class to the event item
        eventItem.classList.add('active');
       

        // Add 'active' class to the corresponding image item
        const imageItem = section.querySelector(`[data-image-item="categories-image-item-${eventItem.dataset.contentItem}"]`);
        if (imageItem) {
            imageItem.classList.add('active');
          
            
        }
        section.querySelectorAll('[data-image-item]').forEach((item) => {
            if (item.classList.contains('active'))
            {
                item.style.zIndex = '3';
            }else{
                item.style.zIndex = '1';
            }
            
        });
    }
}

customElements.define('categories-list', CategorisList);

class QuantityBasedPrice extends HTMLElement {
  
  static observedAttributes = ["qty-in-cart"];

    constructor() {
      super();
      this.parent = this.closest('[data-product-quantity-wrapper]');
      this.input = this.parent?.querySelector('[data-quantity-input]');
      this.pricePerItemSelector = this.querySelector('[price-per-item--current]');
      this.cartItemLabelSelector = this.querySelector('[data-items-in-cart]');
      this.dataArray = [];
      if(this.querySelector('[data-variant-price-breaks]') && this.querySelector('[data-variant-price-breaks]').textContent != ''){
        this.dataArray = JSON.parse(this.querySelector('[data-variant-price-breaks]').textContent)
      }
      if(this.dataArray.length == 0) return;
      if(this.input){
        this.input.addEventListener('change',this._updatePrice.bind(this))
      }
    }
  _updatePrice(){
    if(this.dataArray.length > 0 && this.input && this.pricePerItemSelector){
        this.Qty = parseInt(this.input.value);
        this.cartQty = parseInt(this.input.dataset.cartQty);
        this.step = parseInt(this.input.step); 
      
        let currentQty = this.cartQty + this.Qty;
        for (let priceItem of this.dataArray) {
          if (currentQty >= priceItem.qty) {
            this.pricePerItemSelector.innerHTML = priceItem.label
            break;
          }
        }
    }
  }
  attributeChangedCallback(name, oldValue, newValue) {
    if(name == 'qty-in-cart'){
      this._updateCartText(newValue);
      this._updateInput(newValue);
      this._updatePrice();
    }
  }

  _updateCartText(value){
    if(this.cartItemLabelSelector){
      this.cartItemLabelSelector.innerHTML = this.dataset.cartLabel.replace('{{ item }}', value)
      if(parseInt(value) > 0){
        this.cartItemLabelSelector.classList.remove('hidden');
      }
      else{
        this.cartItemLabelSelector.classList.add('hidden');
      }
    }
    
  }
  
  _updateInput(value){
    if(this.input){
      this.input.dataset.cartQty = value;
      const inputCartQuantity = this.input.dataset.cartQty ? parseInt(this.input.dataset.cartQty) : 0,
          inputMin = this.input.dataset.min ? parseInt(this.input.dataset.min) : 1,
          inputMax = this.input.dataset.max ? parseInt(this.input.dataset.max) : null,
          inputStep = this.input.step ? parseInt(this.input.step) : 1;

        let min = inputMin;
        const max = inputMax === null ? inputMax : inputMax - inputCartQuantity;
        if (max !== null) min = Math.min(min, max);
        if (inputCartQuantity >= inputMin) min = Math.min(min, inputStep);

        this.input.min = min;

        if (max) {
          this.input.max = max;
        } else {
          this.input.removeAttribute('max');
        }
        this.input.value = min;
    }
    
  }
}

customElements.define('quantity-based-price', QuantityBasedPrice);

class CartItemQuantity extends HTMLElement {
    constructor() {
      super();
      this.selector = `quantity-based-price[data-variant-id="${this.dataset.variant}"]`;
      const qty = this.dataset.quantity;
      Array.from(document.querySelectorAll(this.selector)).forEach(function(selector){
        selector.setAttribute('qty-in-cart',qty)
      })
    }
}


customElements.define('cart-item-quantity', CartItemQuantity);
