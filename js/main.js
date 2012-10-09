
(function($){
     $.extend(
         {
            escape: function (str) {
                return str.replace(/"/g, '\'');
            },
            scrape: function (url, xpath, successCallback, errorCallback) {
                var query = 'SELECT * FROM html WHERE url="' +
                    this.escape(url) + '" AND xpath="' +
                    this.escape(xpath) + '"';

                var ajaxSettings = {
                    'url': 'http://query.yahooapis.com/v1/public/yql',
                    'dataType': 'jsonp',
                    'success': successCallback,
                    'async': true,
                    'data': {
                        'q': query,
                        'format': 'json',
                        'env': 'store://datatables.org/alltableswithkeys',
                        'callback': '?'
                    }
                };

                if (errorCallback) {
                    ajaxSettings.error = errorCallback;
                }

                $.ajax(ajaxSettings);
            }
         }
     );
 })(jQuery);

$(function() {
    var $prague = $('.prague');
    var pragueSrc = 'http://lanyrd.com/series/django-cs/';

    $.scrape(pragueSrc, '//*[contains(@class, "conference-listing")]//h4', function (data) {
        var url = 'http://lanyrd.com' + data.query.results.h4[0].a.href;
        $('h3 a', $prague).attr('href', url);
    });

    $.scrape(pragueSrc, '//*[contains(@class, "dtstart")]', function (data) {
        var date = data.query.results.abbr[0].title;
        date = date.split('-');
        date = date[2] + '. ' + date[1] + '.';

        $('.date', $prague).text(date);
    });
});
