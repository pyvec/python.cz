
$(function() {
    var lang = $('html').attr('lang');
    var title = (lang == 'cs') ? 'Trvalý odkaz' : 'Permanent link';

    var selectors = [];
    for (var i = 1; i <= 6; i++) {
        selectors.push('h' + i + '[id]');
    }

    $(selectors.join(', ')).each(function () {
        var el = $(this);
        var link = $('<a/>', {
            'href': '#' + el.attr('id'),
            'class': 'permalink',
            'title': title,
            'text': '¶',
        });
        el.append(link);
    });
});
