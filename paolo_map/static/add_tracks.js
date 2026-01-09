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

function handleFileSelect(event) {
    var files = event.target.files; // FileList object

    // Clear previous layers if needed
    geoJsonLayers.clearLayers();

    for (var i = 0; i < files.length; i++) {
        var file = files[i];
        var reader = new FileReader();

        // Closure to capture the file information
        reader.onload = (function(theFile) {
            return function(e) {
                try {
                    // Parse the GeoJSON data
                    var geojsonData = JSON.parse(e.target.result);

                    // Add GeoJSON layer to the map
                    var layer = L.geoJSON(geojsonData, {
                        onEachFeature: function (feature, layer) {
                            // Optional: Bind a popup with properties
                            if (feature.properties) {
                                var popupContent = "<h3>" + (feature.properties.name || theFile.name) + "</h3>";
                                for (var key in feature.properties) {
                                    popupContent += "<b>" + key + "</b>: " + feature.properties[key] + "<br/>";
                                }
                                layer.bindPopup(popupContent);
                            }
                        }
                    });

                    geoJsonLayers.addLayer(layer); // Add to the layer group

                    // Optional: Fit map bounds to the newly added layers
                    // Note: This will fit to all current layers in geoJsonLayers group
                    map.fitBounds(geoJsonLayers.getBounds());

                } catch (err) {
                    alert("Error parsing " + theFile.name + ": " + err);
                }
            };
        })(file);

        // Read the file as text
        reader.readAsText(file);
    }
}
