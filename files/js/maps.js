

var map = L.map('map').setView([49.8, 15.55], 7);

// http://wiki.openstreetmap.org/wiki/Tile_servers
// http://wiki.openstreetmap.org/wiki/WikiProject_Czech_Republic/freemap
// http://mapbox.com/
var layer = new L.StamenTileLayer('toner', {
    maxZoom: 18,
    detectRetina: true
})
map.addLayer(layer);

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
            if (feature.properties.pyvec) {
                color = 'rgb(54, 105, 147)';
            } else {
                color = '#888888';
            }
            return L.circleMarker(latlng, {
                'radius': 5,
                'fillColor': color,
                'color': '#000',
                'weight': 1,
                'opacity': 1,
                'fillOpacity': 1
            });
        },
        'onEachFeature': onEachFeature
    }).addTo(map);
});
