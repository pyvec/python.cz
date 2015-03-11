

var map = L.map('map').setView([49.8, 15.55], 7);

L.tileLayer('http://129.206.74.245:8001/tms_r.ashx?x={x}&y={y}&z={z}', {
    maxZoom: 18,
    attribution: '<a href="http://openmapsurfer.uni-hd.de/contact.html">GIScience</a> | &copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

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
