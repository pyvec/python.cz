
(function($){
     $.extend(
         {
            _escape: function (str) {
                return str.replace(/"/g, '\'');
            },
            scrape: function (url, xpath, successCallback, errorCallback) {
                var query = 'SELECT * FROM html WHERE url="' +
                    this._escape(url) + '" AND xpath="' +
                    this._escape(xpath) + '"';

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

$(document).ready(function() {
    // Prague
    var $prague = $('.prague');
    var pragueSrc = 'http://lanyrd.com/series/django-cs/';

    $.scrape(pragueSrc, '//*[contains(@class, "conference-listing")]//h4', function (response) {
        var url = 'http://lanyrd.com' + response.query.results.h4[0].a.href;
        $('h3 a', $prague).attr('href', url);
    });

    $.scrape(pragueSrc, '//*[contains(@class, "dtstart")]', function (response) {
        var date = response.query.results.abbr[0].title;
        date = date.split('-');
        date = date[2] + '. ' + date[1] + '.';

        $('.date', $prague).text(date);
    });

    // Brno
    /*

        TODO

    */
});

$(document).on('fbload', function() {
    // Bratislava
    // var uid = 666004183; // Ján Suchal
    var uid = 721972706; // Honza Javorek
    var fql = 'SELECT name FROM event WHERE eid IN ' +
        '(SELECT eid FROM event_member WHERE uid = ' + uid + ')';

    FB.api('/fql?q=' + encodeURIComponent(fql), function(response) {
        console.log(response);
    });

    FB.api('/721972706', function(response) {
        console.log(response);
    });
});
