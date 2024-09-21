// Появление строки поиска при нажатии на лупу

document.addEventListener("DOMContentLoaded", function () {
    function toggleSearch() {
        const searchContainer = document.querySelector('.search-container');
        searchContainer.classList.toggle('active');
    }

    const searchIcon = document.querySelector('.search-icon');
    searchIcon.addEventListener('click', toggleSearch);
});