
var layer = L.tileLayer('https://a.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png', {
    maxZoom: 18,
    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
});


$(function() {
    var element = $('#map');

    var iconSize = parseInt(element.attr('data-icon-size'), 10) || 16;
    var icon = L.icon({
        iconUrl: element.attr('data-icon-src'),
        iconSize: [iconSize, iconSize],
        shadowSize: [0, 0],
        iconAnchor: [iconSize / 2, iconSize / 2],
        popupAnchor: [0, 0]
    });

    var zoom = element.attr('data-zoom') || 7;
    var lat = element.attr('data-lat') || 49.8;
    var lng = element.attr('data-lng') || 15.55;

    var map = L.map('map', {'scrollWheelZoom': false})
        .setView([lat, lng], zoom)
        .addLayer(layer);

    var dataUrl = element.attr('data-src');
    $.getJSON(dataUrl, function(data) {
        L.geoJson(data, {
            pointToLayer: function (feature, coordinates) {
                return L.marker(coordinates, {icon: icon});
            },
            onEachFeature: function (feature, marker) {
                if (feature.properties) {
                    text = '<h3>' + feature.properties.name + '<h3>'
                    marker.bindPopup(text);
                }
            }
        }).addTo(map);
    });
});
