function parseConferenceList(response) {
    var $html = $(response);

    var dates = [];
    $('.dtstart', $html).each(function() {
        dates.push($(this).attr('title'));
    });
    dates.sort();

    var latest = dates.pop();
    var selector = '.dtstart[title="' + latest + '"]';

    var $container = $(selector, $html).closest('.conference');
    var url = 'http://lanyrd.com' + $('h4 a', $container).attr('href');

    return {
        'date': latest,
        'url': url
    };
}


function parseConferenceDetail(response) {
    var $html = $(response);
    var $venue = $('.venue', $html);

    return {
        'venue': $.trim($('h3', $venue).text()),
        'map': $('.map-icon', $venue).attr('href')
    };
}


function ajaxSettingsFactory(url, xpath, callback) {
    var query = 'SELECT * FROM html WHERE url="' + url +
        '" AND xpath="' + xpath + '"';
    return {
        'url': 'http://query.yahooapis.com/v1/public/yql',
        'dataType': 'xml',
        'success': callback,
        'async': true,
        'data': {
            'q': query,
            'format': 'xml'
        }
    };
}


function scrape(url, callback) {

    // ask conference listing for some basic info
    var xpath = '//*[contains(@class, \'conference-listing\')]';
    $.ajax(ajaxSettingsFactory(url, xpath, function(response) {
        var data = parseConferenceList(response);

        // ask detail page about some further info
        var xpath = '//*[contains(@class, \'venue\')]';
        $.ajax(ajaxSettingsFactory(data.url, xpath, function(response) {
            var moreData = parseConferenceDetail(response);

            // merge data
            for (var attr in moreData) {
                data[attr] = moreData[attr];
            }

            callback(data);
        }));
    }));
}


function formatDate(date) {
    date = date.split('-');

    day = date[2].replace(/^0+/, '');
    month = date[1].replace(/^0+/, '');

    date = day + '. ' + month + '.';
    return date;
}


$(function() {
    var venue_prefix = $('.map').attr('data-venue-prefix') || '';
    $('.map li').each(function() {
        var $city = $(this);

        var url = $('.lanyrd_link', $city).attr('href');
        scrape(url, function (data) {
            if (data.date) {
                $('h3 a', $city).attr('href', data.url);
                $('.date', $city).text(formatDate(data.date));
                $('.venue', $city).replaceWith(
                    $('<span>', {
                        text: venue_prefix + ' ',
                        class: 'venue'
                    }).append($('<a>', {
                        'href': data.map,
                        'text': data.venue
                    }))
                );

                if (new Date(Date.parse(data.date)) < new Date) {
                    $city.addClass('in-past');
                }
            }
        });
    });
});
