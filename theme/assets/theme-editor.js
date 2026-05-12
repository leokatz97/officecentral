document.addEventListener("shopify:block:select", function(event) {
    let _block = event.target;
    let slider = _block.closest("[data-slideshow]");
    if (slider && slider.classList.contains("flickity-enabled")) {
        let index = Array.from(_block.parentElement.children).indexOf(_block);
        let mainSlider = Flickity.data(slider);
        if (mainSlider) {
            mainSlider.select(index);
        }
    }
    if (aosAnimation) {
        if (AOS) {
            AOS.refreshHard();
        }
    }
    if(_block.closest("time-line-content")){
        
      let topElement = _block.closest("time-line-content");
      if(_block.querySelector(".timeline-image").classList.contains("active"))
      return false;
      if(topElement.querySelector(".timeline-image.active")){
        topElement.querySelector(".timeline-image.active").classList.remove("active");
      }
        _block.querySelector(".timeline-image").classList.add("active")
      
    }

    menuDropdown(_block);
    marqueeTextAutoplay(_block);
    lookbook(_block);
    variant_selector(_block);
    getCountDownElments(_block);
    vertical_scroll(_block);
    getcollageElments(_block);
    // initStoreLocator(_block);
    let vertical_slider = _block.closest("[data-carousal-container]");
    if (vertical_slider) {
        _block.click();
    }
    detailDisclouserInit(_block);
    tab_media_item(_block);
    let tabMediacontent = _block.closest(".tab-media-wrapper");
    if (tabMediacontent) {
        _block.click();

    }
    videoBanner(_block);
    initHotspot(_block);
    testimonialInit(_block);
    getAllDetails(_block);
    SidedrawerEventInit(_block);
    productRecommendations(_block);
    recentlyViewedProducts(_block);
    quickviewElements(_block);
    mp4VideoReady(_block);
    vimeoVideoReady(_block);
    collectionTabs();
    scrollTop(_block);
    checkedboxCookies(_block);
    CloseCompareModel(_block);
    showMoremedia(_block);
    announcementCollapsiblecontent(_block);
    ageVerifiedpopup(_block);
    onHoverMenuElements(_block);
    //newsletterPopup(_block);
    newsletterofferPopup(_block);
    quickNav(_block);
    productCardHoverInit(_block);
    get_header_height(_block);
    imagesBanner(_block);
    categoriesSidebar(_block);
    headerHamburgerMenu(_block);
    hamburgerHoverMenu(_block);

});

document.addEventListener("shopify:section:select", function(event) {
    let _section = event.target;
    let quick_drawer = _section.querySelector("[data-quick-drawer]");
    if (quick_drawer) {
        quick_drawer.classList.add("sidebar-visible");
        quick_drawer.style.display = "flex";
        quick_drawer.style.opacity = 1;
    }

    let information_drawer = _section.querySelector(".need-help-drawer");
    if (information_drawer) {
        information_drawer.classList.add("sidebar-visible");
        information_drawer.style.display = "flex";
    }

    if (_section.classList.contains("age-verification")) {
        setTimeout(function() {
            if (_section.childElementCount == 0) {
                _section.classList.remove("active");
                document.querySelector("body").classList.remove("no-scroll");
            } else {
                _section.classList.add("active");
                document.querySelector("body").classList.add("no-scroll");
            }
        }, 100);
    }
    if (_section.classList.contains("newsletter-popup")) {
        setTimeout(function() {
            if (_section.childElementCount <= 1) {
                _section.classList.remove("active");
                document.querySelector("body").classList.remove("no-scroll");
            } else {
                _section.classList.add("active");
                document.querySelector("body").classList.add("no-scroll");
            }
        }, 100);
    }
    let categoriesButton = _section.querySelector("[data-categories-btn]");
    if (categoriesButton) {
        categoriesButton
            .closest("[data-categories-wrapper]")
            .classList.add("active");
        document.querySelector("body").classList.add("sidebar-category-overlay");
    }
    if (aosAnimation) {
        if (AOS) {
            AOS.refreshHard();
        }
    }
});

document.addEventListener("shopify:section:deselect", function(event) {
    let _section = event.target;
    if (aosAnimation) {
        if (AOS) {
            AOS.refreshHard();
        }
    }
    let quick_drawer = _section.querySelector("[data-quick-drawer]");
    if (quick_drawer) {
        quick_drawer.classList.remove("sidebar-visible");
        quick_drawer.style.display = "none";
        quick_drawer.style.opacity = 0;
    }
    let information_drawer = _section.querySelector(".need-help-drawer");
    if (information_drawer) {
        information_drawer.classList.remove("sidebar-visible");
        information_drawer.style.display = "none";
    }

    let compareModel = _section.querySelector(".compare-modal-content");
    if (compareModel) {
        compareModel.classList.add("popup-visible");
        compareModel.style.display = "none";
        compareModel.style.opacity = 0;
    }
    if (_section.classList.contains("age-verification")) {
        _section.classList.remove("active");
        document.querySelector("body").classList.remove("no-scroll");
    }

    if (_section.classList.contains("newsletter-popup")) {
        _section.classList.remove("active");
        document.querySelector("body").classList.remove("no-scroll");
    }

    let categoriesButton = _section.querySelector("[data-categories-btn]");
    if (categoriesButton) {
        categoriesButton
            .closest("[data-categories-wrapper]")
            .classList.remove("active");
        document.querySelector("body").classList.remove("sidebar-category-overlay");
    }

});

document.addEventListener("shopify:section:load", function(event) {
    let _section = event.target;
    let videoPlayButton = _section.querySelector("[data-video-play-button]");

    bundleProductInit(_section);
    if (videoPlayButton) {
        playButtonClickEvent(videoPlayButton);
    }

    if (_section.querySelector('.parallax-image')) {
        new universalParallax(_section).init({
            speed: 10
        });
    }
    mobileNavigation(_section);
    let sliders = _section.querySelectorAll("[data-slideshow]");
    Array.from(sliders).forEach(function(selector) {
        if (selector && !selector.classList.contains("flickity-enabled")) {
            slideshowInit(selector);
        }
    });
    if (_section.classList.contains("age-verification")) {
        if (_section.childElementCount == 0) {
            setTimeout(function() {
                _section.classList.remove("active");
                document.querySelector("body").classList.remove("no-scroll");
            }, 100);
        }
    }
    if (_section.classList.contains("newsletter-popup")) {
        if (_section.childElementCount <= 1) {
            setTimeout(function() {
                _section.classList.remove("active");
                document.querySelector("body").classList.remove("no-scroll");
            }, 100);
        }
    }
    if (_section.classList.contains("header")) {
        colorMode();
    }
    if (_section.classList.contains("footer")) {
        footerDropdownCheck();
    }
    getATCelement(_section);
    announcementSocialWidth(_section);
    stickyformqty(_section);
    customSliderArrowsEvents(_section);
    collectionCarousal(_section);
    menuDropdown(_section);
    onHoverMenuElements(_section);
    compareBarViewToggle(_section);
    accordion(_section);
    lookbook(_section);
    search_drawer(_section);
    getQuantityElement(_section);
    variant_selector(_section);
    marqueeTextAutoplay(_section);
    getCountDownElments(_section);
    vertical_scroll(_section);
    getcollageElments(_section);
    needHelpTabs(_section);
    if (document.querySelector("[data-footer-sticky]")) {
        stickyFooterInit(_section);
    } else {
        document.body.classList.remove('footer-sticky')
    }
    badgesAnimation(_section);
    detailDisclouserInit(_section);
    if (typeof window.google === "undefined" || typeof window.google.maps === "undefined") {
        initStoreLocator();
    } else {
        initStoreMap(_section);
    }
    tab_media_item(_section);
    videoBanner(_section);
    toggleVideoAudio(_section);
    initHotspot(_section);
    getAllDetails(_section);
    SidedrawerEventInit(_section);
    productRecommendations(_section);
    recentlyViewedProducts(_section);
    quickviewElements(_section);
    customDropdownElements(_section);
    mp4VideoReady(_section);
    vimeoVideoReady(_section);
    headerNavigationPosition(_section);
    outSideClickTrigger(_section);
    collectionTabs(_section);
    scrollTop(_section);
    checkedboxCookies(_section);
    CloseCompareModel(_section);
    showMoremedia(_section);
    announcementCollapsiblecontent(_section);
    ageVerifiedpopup(_section);
    newsletterofferPopup(_section);
    quickNav(_section);
    productCardHoverInit(_section);
    get_header_height(_section);
    featuredImages(_section);
    revealCollection(_section);
    imagesBanner(_section);
    initBeforeAfter(_section);
    windowResize(_section);
    stickyProductContentSlide(_section);
    stickyAddToCartInit(_section);
    imageWithCarousel(_section);
    productTermhandler(_section);
    headerHamburgerMenu(_section);
    hamburgerHoverMenu(_section);
    markeranimation(_section);
    sectionLoadSelector(_section);
    if (aosAnimation) {
        if (AOS) {
            AOS.refreshHard();
        }
    }
    window.addEventListener('scroll', function() {
        document.querySelectorAll("section").forEach((section) => {
            if (isOnScreen(section)) {

                if (section.classList.contains("before-after-image")) {
                    setTimeout(function() {
                        section.classList.add("section-in-view");

                        section.querySelector(".before-after-wrapper").classList.add("animating")
                        setTimeout(function() {
                            section.querySelector(".before-after-wrapper").classList.remove("animating")
                        }, 1000)
                    }, 1000)
                } else {
                    setTimeout(function() {
                        section.classList.add("section-in-view");
                    }, 500)
                }

            }
        });
    });
});