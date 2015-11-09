
$(function() {
    var lang = $('html').attr('lang');
    var title = (lang == 'cs') ? 'Trvalý odkaz' : 'Permanent link';

    var selectors = [];
    for (var i = 1; i <= 6; i++) {
        selectors.push('h' + i + '[id]');
    }

    $(selectors.join(', ')).each(function () {
        var $heading = $(this);

        var $link = $('<a/>', {
            'href': '#' + $heading.attr('id'),
            'class': 'permalink',
            'title': title,
            'text': '¶',
        });
        var $container = $('<span/>', {
            'class': 'permalink-container',
        });

        $heading.append($container);
        $container.append($link);
    });
});
