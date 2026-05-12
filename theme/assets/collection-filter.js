window.addEventListener('load', (event) => {
    applyFilters();
    sortByoptions();
    // SidedrawerEventInit();

});
window.addEventListener('resize', (event) => {
  if (window.innerWidth > 1024 && document.querySelector('#Collection-filter-sidebar')) {
    document.querySelector('#Collection-filter-sidebar').style.removeProperty("display");
  }
});
let triggered = false;

function fetchFilterData(url) {
    return fetch(url)
        .then(response => response.text())
}

function applyFilters() {
    let section = document.getElementById('CollectionProductsParent');
    let filterForm = document.getElementById('FiltersForm');
    let sectionParent = section.closest('.shopify-section');
    let sectionId = section.dataset.id;
    if (section) {
        if (!filterForm) {
            return false;
        }
        collection_price_range(sectionId, sectionParent);
        let inputs = filterForm.querySelectorAll('input[type=checkbox]');
        Array.from(inputs).forEach(function(input) {
            input.addEventListener('click', () => {
              SidedrawerEventInit();
              getFilterData(input, sectionId);
            });
        });
    }
}

function sortByoptions() {
    let section = document.querySelector('.collection-wrapper');
    let sortBy = document.querySelectorAll('[name="sort_by"]');
    if (section) {
        let sectionId = section.querySelector('.collection_products').dataset.id;
        Array.from(sortBy).forEach(function(sort) {
            sort.addEventListener("change", (e) => {
                e.preventDefault();
                sort.closest('.collection-sortby-item').classList.remove('selected');
                sort.closest('.collection-sortby-item').classList.add('selected');
                let sortMenu = section.querySelector('.collection-sortby-inner');
                let sortList = sortMenu.querySelector('.collection-sortby-detail');
                if (sortMenu.hasAttribute('open')) {
                    DOMAnimations.slideUp(sortList);
                }
                SidedrawerEventInit();
                getFilterData(sort, sectionId);
            });
        });
    }
}

function getFilterData(input, sectionId, remove, minPriceRange, maxPriceRange) {
    let section = document.getElementById('CollectionProductsParent');
    let sectionParent = section.closest('.shopify-section');
    let filterForm = document.getElementById('FiltersForm');
    let formData = new FormData(filterForm);
    let searchParameters = new URLSearchParams(formData).toString();
    let url = window.location.pathname + '?section_id=' + sectionId + '&' + searchParameters;
    let updateUrl = window.location.pathname + '?' + searchParameters;
    if (remove) {
        url = remove;
        updateUrl = remove;
    } 
    let get_html = fetchFilterData(url).then((responseText) => {
        let resultData = new DOMParser().parseFromString(responseText, 'text/html');
        let itemResultcount = resultData.querySelector('.Product-result .total_products');
        let element = document.getElementById('CollectionProductsParent');
        let html = resultData.getElementById('CollectionProductsParent');
        let mobileSort = document.querySelector('[data-mobile-sort]');
        let resultMobileSort = resultData.querySelector('[data-mobile-sort]');
        let filter_element = document.querySelector('.collection-filter-sidebar');
        let filter_html = resultData.querySelector('.collection-filter-sidebar');
        if (element) {
            element.innerHTML = html.innerHTML;
            let scrollDiv = document.getElementById('CollectionProductsParent');
            if(mobileSort && resultMobileSort){
                mobileSort.innerHTML = resultMobileSort.innerHTML;
            }
            scrollIntoView(scrollDiv);
            filter_element.innerHTML = filter_html.innerHTML;
            applyFilters();
            remove_filter(sectionParent, sectionId);
            SidedrawerEventInit();
           
        } else {
            let productResultContainer = element.querySelector('[data-collection-products]');
            if (productResultContainer) {
                productResultContainer.innerHTML = noResultFound;
            }
        }
        collectionSwatch();
        history.pushState({}, null, updateUrl);
        sortByoptions();
        triggered = false
        loadMoreCollection();
        getCountDownElments();
        quickviewElements();
        customDropdownElements();
        SidedrawerEventInit();
        productCardHoverInit();
        if(aosAnimation){
            if (AOS) {
                AOS.refreshHard();
            }
        }
    });
}

function scrollIntoView(selector, offset = 0) {
    window.scroll(0, selector.offsetTop - offset);
}

function remove_filter(sectionParent, sectionId) {
    var removeFilters = sectionParent.querySelectorAll('a.sr-applied-filter-remove');
    Array.from(removeFilters).forEach(function(removeFilter) {
        removeFilter.addEventListener('click', function(event) {
            event.preventDefault();
            if (removeFilter.hasAttribute('sr-applied-filter-cross-all')) {
                var _url = removeFilter.getAttribute('href');
                getFilterData(removeFilter, sectionId, _url);
                return false;
            } else {
                var _url = removeFilter.getAttribute('href');
                getFilterData(removeFilter, sectionId, _url);
            }
        });
    });
}

function collection_price_range(sectionId, sectionParent) {
    const rangeInput = document.querySelectorAll(".sr-range-input input"),
        priceInput = document.querySelectorAll(".sr-price-input input"),
        range = document.querySelector("#priceSilderProgress");
    if (rangeInput.length > 0) {
        let priceGap = rangeInput[0].getAttribute('step');
        priceInput.forEach((input) => {
            input.addEventListener("change", (e) => {
                let minPrice = parseInt(priceInput[0].value),
                    maxPrice = parseInt(priceInput[1].value),
                    maxPriceRange = parseInt(priceInput[1].getAttribute("data-max-value"));
                if (minPrice > maxPriceRange) {
                    minPrice = maxPriceRange;
                    priceInput[0].value = minPrice;
                }
                getFilterData(input, sectionId)
            });
        });
        rangeInput.forEach((input) => {
            input.addEventListener("change", (event) => {
                rangeSlider(input, event);
                getFilterData(input, sectionId);
            });
            input.addEventListener("input", (event) => {
                rangeSlider(input, event);
            });

        });
        var rangeSlider = function(input, event) {
            let minVal = parseInt(rangeInput[0].value),
                maxVal = parseInt(rangeInput[1].value);
            minPriceRange = Math.max(0,((minVal / rangeInput[0].max) * 100));
            maxPriceRang = Math.max(0,(100 - (maxVal / rangeInput[1].max) * 100));
            if (maxVal - minVal < priceGap) {
                if (event.target.className === "priceslider-range-min") {
                    rangeInput[0].value = maxVal - priceGap;
                } else {
                    rangeInput[1].value = minVal + priceGap;
                }
            } else {
                priceInput[0].value = minVal;
                priceInput[1].value = maxVal;
                range.style.left = minPriceRange + "%";
                range.style.right = maxPriceRang + "%";
            }
        }
    }
}

//Infinite scroll
function Onscrollproducts() {
    window.addEventListener('scroll', function() {
        let scrollElement = document.querySelector("[data-scroll]");
        if (scrollElement) {
            infiniteScroll(scrollElement);          
        }
    });
}

function infiniteScroll(scrollElement) {
    if (scrollElement && scrollElement.querySelector('a')) {
        let nextUrl = scrollElement.querySelector('a').getAttribute('href');
        if (isOnScreen(scrollElement) && (triggered == false)) {
            triggered = true;
            scrollElement.querySelector('a').remove();
            scrollElement.querySelector('.load').classList.remove('hidden');
            fetchFilterData(nextUrl).then((responseText) => {
                scrollElement.remove();
                const resultData = new DOMParser().parseFromString(responseText, 'text/html');
                let html = resultData.querySelector('#CollectionProductsParent');
                let element = document.querySelector('#CollectionProductsParent');
                /* result for the collection page */
                if (html) {
                    element.querySelector('[data-collection-products]').innerHTML += html.querySelector('[data-collection-products]').innerHTML;
                    getCountDownElments();
                    triggered = false
                    loadMoreCollection();
                    quickviewElements();
                    productCardHoverInit();
                    if(aosAnimation){
                        if (AOS) {
                            AOS.refreshHard();
                        }
                    }
                }

            });

        }
    }

}

function loadMoreCollection(section = document) {
    let loadmoreButton = section.querySelector('[data-products-load]');
    if (loadmoreButton) {
        loadmoreButton.addEventListener("click", function(event) {
            event.preventDefault();
            let scrollElement = loadmoreButton.closest('[data-load-more]');
            if (scrollElement) {
                infiniteScroll(scrollElement);
            }            
        });
    }
}
document.addEventListener('DOMContentLoaded', function() {
    Onscrollproducts();
    loadMoreCollection();
});
document.addEventListener('shopify:block:select', function (event) {
    let _block = event.target;
    Onscrollproducts(_block);
    loadMoreCollection(_block);
});
document.addEventListener('shopify:section:load', function (event) {
    let _section = event.target;
    Onscrollproducts(_section);
    loadMoreCollection(_section);
});