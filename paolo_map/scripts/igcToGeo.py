import os
from libigc import Flight
from geojson import Feature, LineString, FeatureCollection
from common import writeJSON

def igcToGeoJSON(igc_path,saveDir):
    flight = Flight.create_from_file(igc_path)
    coordinates = []
    for fix in flight.fixes:
        coordinates.append([fix.lon, fix.lat]) # GeoJSON uses [longitude, latitude, elevation] order
    # Create a GeoJSON LineString geometry
    line_string = LineString(coordinates)
    # Create a GeoJSON Feature
    # You can add properties from the IGC file header (e.g., pilot name, glider type)
    feature = Feature(
        geometry=line_string,
        properties={
            "pilot": 'test pilot',
            "glider_type": 'test glider',
            "flight_date": '2025-01-01',
            "score": 350
        }
    )
    writeJSON(igc_path.replace('.igc','json'),feature)
    # Wrap the feature in a FeatureCollection
    # feature_collection = FeatureCollection([feature])

igc_path = '/home/bret/soardata/soardataApp/lib/igcs/wg_582753.igc'
saveDir = '/home/bret/soardata/soardataApp/lib/geoJSON'
if not os.path.exists(saveDir): os.mkdir(saveDir)
igcToGeoJSON(igc_path,saveDir)
