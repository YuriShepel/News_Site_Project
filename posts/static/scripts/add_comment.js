// document.addEventListener('DOMContentLoaded', function () {
//     const form = document.getElementById('comment-form');
//     const commentsContainer = document.getElementById('comments-container');
//     // Настройка marked.js
//     marked.setOptions({
//         breaks: true, // Переносы строк будут преобразованы в <br>
//         gfm: true, // Использовать GitHub Flavored Markdown
//     });
//
//     // Функция для рендеринга Markdown
//     function renderMarkdown() {
//         const comments = document.querySelectorAll('.comment-text');
//         comments.forEach(comment => {
//             let rawText = comment.textContent.trim(); // Убираем лишние пробелы в начале и конце
//             // Удаляем пробелы в начале каждой строки
//             rawText = rawText.replace(/^\s+/gm, '');
//             comment.innerHTML = marked(rawText);
//         });
//     }
//
//     // Вызываем функцию при загрузке страницы
//     renderMarkdown();
//
//     form.addEventListener('submit', function (e) {
//         e.preventDefault();
//         submitComment(form);
//     });
//
//     commentsContainer.addEventListener('click', function (e) {
//         if (e.target.classList.contains('reply-button')) {
//             const commentId = e.target.dataset.commentId;
//             const authorName = e.target.dataset.author;
//             const commentElement = document.querySelector(`#comment-${commentId} .comment-text`);
//
//             let commentText = commentElement.innerText.trim();
//             // Экранируем символы Markdown в тексте комментария
//             commentText = commentText.replace(/([*_`\\])/g, '\\$1');
//             // Удаляем переносы строк и заменяем их на пробелы
//             commentText = commentText.replace(/\n/g, ' ');
//
//             // Формируем текст ответа с цитатой на одной строке и новой строкой для ответа
//             const replyText = `> ${commentText}\n\n**@${authorName}**, `;
//
//             const commentBody = document.getElementById('id_body');
//             commentBody.value = replyText;
//             commentBody.focus();
//
//             // Устанавливаем курсор в конец текста
//             commentBody.setSelectionRange(commentBody.value.length, commentBody.value.length);
//
//             form.scrollIntoView({behavior: 'smooth'});
//         }
//     });
//
//     function submitComment(form) {
//         console.log('Form submitted');
//
//         const formData = new FormData(form);
//         const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
//
//         fetch(form.action, {
//             method: 'POST',
//             body: formData,
//             headers: {
//                 'X-Requested-With': 'XMLHttpRequest',
//                 'X-CSRFToken': csrfToken
//             },
//             credentials: 'same-origin'
//         })
//             .then(response => response.json())
//             .then(data => {
//                 console.log('Response:', data);
//                 if (data.success) {
//                     commentsContainer.insertAdjacentHTML('afterbegin', createCommentHTML(data.comment));
//                     form.reset();
//                     // Рендерим Markdown для нового комментария
//                     renderMarkdown();
//                 } else {
//                     console.log('Error in response:', data.errors);
//                     alert('Произошла ошибка при отправке комментария. Пожалуйста, проверьте введенные данные.');
//                 }
//             })
//             .catch(error => {
//                 console.error('Fetch error:', error);
//                 alert('Произошла ошибка при отправке комментария. Пожалуйста, попробуйте еще раз позже.');
//             });
//     }
//
//     function createCommentHTML(comment) {
//         // Убираем лишние пробелы в начале и конце текста комментария
//         const cleanCommentBody = comment.body.trim().replace(/^\s+/gm, '');
//         return `
//             <div class="comment" id="comment-${comment.id}">
//                 <div class="comment-content">
//                     <div class="comment-meta">
//                         Опубликовано <a href="#">${comment.name}</a> • только что
//                         • (${comment.created_date})
//                     </div>
//                     <div class="comment-text">
//                         ${marked(cleanCommentBody)}
//                     </div>
//                     <button class="reply-button" data-comment-id="${comment.id}" data-author="${comment.name}">Ответить</button>
//                     <div class="dividing-section"></div>
//                 </div>
//             </div>
//         `;
//     }
//
//     // Добавляем функцию предпросмотра
//     const previewButton = document.getElementById('preview-button');
//     const previewContainer = document.getElementById('preview-container');
//
//     if (previewButton && previewContainer) {
//         previewButton.addEventListener('click', function () {
//             const commentBody = document.getElementById('id_body');
//             const previewContent = marked(commentBody.value);
//             previewContainer.innerHTML = previewContent;
//             previewContainer.style.display = 'block';
//         });
//     }
// });


document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('comment-form');
    const commentsContainer = document.getElementById('comments-container');
    // Настройка marked.js
    marked.setOptions({
        breaks: true, // Переносы строк будут преобразованы в <br>
        gfm: true, // Использовать GitHub Flavored Markdown
    });

    function renderMarkdown(element = null) {
        const comments = element
            ? [element.querySelector('.comment-text')]
            : document.querySelectorAll('.comment-text');

        comments.forEach(comment => {
            if (comment) {
                let rawText = comment.textContent.trim();
                rawText = rawText.replace(/^\s+/gm, '');
                comment.innerHTML = marked(rawText);
            }
        });
    }

    function renderMarkdownForElement(element) {
        const commentText = element.querySelector('.comment-text');
        if (commentText) {
            let rawText = commentText.textContent.trim();
            rawText = rawText.replace(/^\s+/gm, '');
            commentText.innerHTML = marked(rawText);
        }
    }

    renderMarkdown();

    form.addEventListener('submit', function (e) {
        e.preventDefault();
        submitComment(form);
    });

    commentsContainer.addEventListener('click', function (e) {
        if (e.target.classList.contains('reply-button')) {
            const commentId = e.target.dataset.commentId;
            const authorName = e.target.dataset.author;
            const commentElement = document.querySelector(`#comment-${commentId} .comment-text`);

            let commentText = commentElement.innerText.trim();
            // Экранируем символы Markdown в тексте комментария
            commentText = commentText.replace(/([*_`\\])/g, '\\$1');
            // Удаляем переносы строк и заменяем их на пробелы
            commentText = commentText.replace(/\n/g, ' ');

            // Формируем текст ответа с цитатой на одной строке и новой строкой для ответа
            const replyText = `> ${commentText}\n\n**@${authorName}**, `;

            const commentBody = document.getElementById('id_body');
            commentBody.value = replyText;
            commentBody.focus();

            commentBody.setSelectionRange(commentBody.value.length, commentBody.value.length);

            form.scrollIntoView({behavior: 'smooth'});
        }
    });

    function submitComment(form) {
        console.log('Form submitted');

        const formData = new FormData(form);
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrfToken
            },
            credentials: 'same-origin'
        })
            .then(response => response.json())
            .then(data => {
                console.log('Response:', data);
                if (data.success) {
                    commentsContainer.insertAdjacentHTML('afterbegin', createCommentHTML(data.comment));
                    form.reset();
                    // Рендерим Markdown только для нового комментария
                    const newComment = commentsContainer.querySelector('.comment');
                    renderMarkdownForElement(newComment);
                } else {
                    console.log('Error in response:', data.errors);
                    alert('Произошла ошибка при отправке комментария. Пожалуйста, проверьте введенные данные.');
                }
            })
            .catch(error => {
                console.error('Fetch error:', error);
                alert('Произошла ошибка при отправке комментария. Пожалуйста, попробуйте еще раз позже.');
            });
    }

    function createCommentHTML(comment) {
        const cleanCommentBody = comment.body.trim().replace(/^\s+/gm, '');
        return `
            <div class="comment" id="comment-${comment.id}">
                <div class="comment-content">
                    <div class="comment-meta">
                        Опубликовано <a href="#">${comment.name}</a> • только что
                        • (${comment.created_date})
                    </div>
                    <div class="comment-text">
                        ${cleanCommentBody}
                    </div>
                    <button class="reply-button" data-comment-id="${comment.id}" data-author="${comment.name}">Ответить</button>
                    <div class="dividing-section"></div>
                </div>
            </div>
        `;
    }

    const previewButton = document.getElementById('preview-button');
    const previewContainer = document.getElementById('preview-container');

    if (previewButton && previewContainer) {
        previewButton.addEventListener('click', function () {
            const commentBody = document.getElementById('id_body');
            const previewContent = marked(commentBody.value);
            previewContainer.innerHTML = previewContent;
            previewContainer.style.display = 'block';
        });
    }
});