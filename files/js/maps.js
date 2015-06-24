

var map = L.map('map').setView([49.8, 15.55], 7);


var layer = L.tileLayer('http://a.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png', {
    maxZoom: 18,
    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
});
map.addLayer(layer);


var icon = L.icon({
    iconUrl: '/images/icon.png',
    iconSize: [16, 16],
    shadowSize: [0, 0],
    iconAnchor: [8, 8],
    popupAnchor: [0, 0]
});


function onEachFeature(feature, marker) {
    if (feature.properties) {
        text = '<h3>' + feature.properties.name + '<h3><p>'
        if (feature.properties.venue) {
            text += '<span class="venue"><a href="#'
                + feature.geometry.coordinates + '">'
                + feature.properties.venue + '</a></span>'
        }
        marker.bindPopup(text);
    }
}

$.getJSON($('#map').attr('data-src'), function(data) {
    L.geoJson(data, {
        pointToLayer: function (feature, latlng) {
            return L.marker(latlng, {icon: icon});
        },
        'onEachFeature': onEachFeature
    }).addTo(map);
});
