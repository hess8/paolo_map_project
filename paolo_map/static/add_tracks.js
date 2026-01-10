// Initialize the map
var map = L.map('map').setView([51.505, -0.09], 2); // Initial center and zoom

// Add a tile layer
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Create a LayerGroup to hold all GeoJSON layers for easy management
var geoJsonLayers = L.layerGroup().addTo(map);

// Get the file input element
document.getElementById('fileInput').addEventListener('change', handleFileSelect, false);

function addPolylinesFromFile(filename) {
    fetch(filename)
        .then(response => response.json())
        .then(data => {
            // L.geoJSON automatically handles multiple LineStrings in a FeatureCollection
            L.geoJSON(data, {
                style: function(feature) {
                    // Use properties from the GeoJSON to style each polyline
                    return {
                        color: feature.properties.color || 'black', // Default to black
                        weight: 4,
                        opacity: 0.7
                    };
                },
                onEachFeature: function(feature, layer) {
                    // Add a popup with the name property
                    if (feature.properties && feature.properties.name) {
                        layer.bindPopup(feature.properties.name);
                    }
                }
            }).addTo(map);
        })
        .catch(error => console.error('Error loading GeoJSON file:', error));
}

// Load multiple files
addPolylinesFromFile('routes_group_a.geojson');
addPolylinesFromFile('routes_group_b.geojson');
// ... continue for each file
