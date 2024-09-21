document.addEventListener('click', function(e) {
    if (e.target.classList.contains('toggle-content')) {
        const postContent = e.target.closest('.post').querySelector('.post-content');
        const postText = postContent.querySelector('.post-text');
        const postTags = postContent.querySelector('.post-tags'); // Убедитесь, что эта переменная существует
        const postActions = postContent.querySelector('.post-actions');

        if (postText.classList.contains('hidden-content')) {
            postText.classList.remove('hidden-content');
            postTags.classList.remove('hidden-content');
            postActions.classList.remove('hidden-content');
            e.target.textContent = '-';
        } else {
            postText.classList.add('hidden-content');

            postActions.classList.add('hidden-content');
            e.target.textContent = '+';
        }
    }
});