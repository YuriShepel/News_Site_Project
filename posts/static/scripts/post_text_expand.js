$(document).ready(function () {
    $('.post-text').each(function () {
        var $content = $(this);
        var $text = $content.find('p');
        var fullText = $content.data('full-content');
        var shortLength = $content.data('short-length');
        var $expandBtn = $content.find('.expand-btn');
        var $expandBtn = $('<div class="expand-btn">РАЗВЕРНУТЬ</div>');


        if (!$content.find('.gradient-overlay').length) {
            $content.append('<div class="gradient-overlay"></div>');
        }
        if (fullText.length <= shortLength) {
            return; // Если длина текста не превышает shortLength, кнопка не требуется
        }

        $content.append($expandBtn);
        $expandBtn.on('click', function () {
            $content.toggleClass('expanded');
            if ($content.hasClass('expanded')) {
                $text.text(fullText);
                $(this).text('СВЕРНУТЬ');
                $content.append($(this));  // Перемещаем кнопку в конец контента
            } else {
                $text.text($text.text().substring(0, shortLength) + '...');
                $(this).text('РАЗВЕРНУТЬ');
                $content.append($(this));  // Возвращаем кнопку в исходное положение
            }
        });
    });
});