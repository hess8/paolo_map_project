const href = "https://www.openstreetmap.org/copyright";
const link = `© <a href='${href}'>OpenStreetMap</a>`;
const tiles = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";
const layer = L.tileLayer(tiles, { attribution: link });
const map = L.map("map", { layers: [layer] });
//map.fitWorld();

// locate user
map
  .locate()
  .on("locationfound", (e) =>
    map.setView(e.latlng, 8)
  )
  .on("locationerror", () =>
    map.setView([0, 0], 5)
  );

//render markers

const layerGroup = L.layerGroup().addTo(map);

async function load_markers() {
  const markers_url = `/api/markers/?in_bbox=${map
    .getBounds()
    .toBBoxString()}`;
  const response = await fetch(
    markers_url
  );
  const geojson = await response.json();
  return geojson;
}

async function render_markers() {
  const markers = await load_markers();
  layerGroup.clearLayers();
  L.geoJSON(markers)
    .bindPopup(
      (layer) =>
        layer.feature.properties.name
    )
    .addTo(layerGroup);
}

map.on("moveend", render_markers);

