// Появление строки поиска при нажатии на лупу

document.addEventListener("DOMContentLoaded", function () {
    function toggleSearch() {
        const searchContainer = document.querySelector('.search-container');
        searchContainer.classList.toggle('active');
    }

    const searchIcon = document.querySelector('.search-icon');
    searchIcon.addEventListener('click', toggleSearch);
});

document.addEventListener('DOMContentLoaded', function () {
    const searchIcon = document.querySelector('.search-icon');
    const searchInput = document.querySelector('.search-input');
    const searchForm = document.querySelector('.search-container form');

    searchIcon.addEventListener('click', function (e) {
        e.preventDefault(); // Предотвращаем отправку формы при клике на иконку
        searchInput.classList.toggle('active');
        if (searchInput.classList.contains('active')) {
            searchInput.focus();
        }
    });

    // Предотвращаем скрытие строки поиска при клике внутри формы
    searchForm.addEventListener('click', function (e) {
        e.stopPropagation();
    });

    // Скрываем строку поиска при клике вне её
    document.addEventListener('click', function (e) {
        if (!searchForm.contains(e.target) && searchInput.classList.contains('active')) {
            searchInput.classList.remove('active');
        }
    });

    // Проверяем, есть ли текст в поле поиска при загрузке страницы
    if (searchInput.value.trim() !== '') {
        searchInput.classList.add('active');
    }
});