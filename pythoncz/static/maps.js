
var layer = L.tileLayer('https://a.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png', {
    maxZoom: 18,
    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
});


var icon = L.icon({
    iconUrl: '/static/images/icon.png',
    iconSize: [16, 16],
    shadowSize: [0, 0],
    iconAnchor: [8, 8],
    popupAnchor: [0, 0]
});


$(function() {
    var element = $('#map');

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
