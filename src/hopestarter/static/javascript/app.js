
(function() {
    // Adjust the content of the page below the header
    var height = document.getElementsByTagName("header")[0].offsetHeight;
    document.getElementsByClassName("first")[0].style.paddingTop = height + 'px';
})();
