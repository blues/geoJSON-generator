import argparse
import json

def fetch_input_json(infile):
    with open(infile, encoding = 'utf-8') as input_file:
        return json.load(input_file)

def process_json(raw_json):
    processed_json = {
        "type": "FeatureCollection",
        "features": []
    }

    for event in raw_json:
        if event["file"] == "_track.qo":
            geo_point = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        event["value"]["best_lon"],
                        event["value"]["best_lat"]
                    ]
                },
                #"properties": {
                #    "device": event["device"]
                #}
                "properties": event
            }
            processed_json["features"].append(geo_point)

    return processed_json

def write_output(events, outfile):
    with open(outfile,'w',encoding = 'utf-8') as output_file:
        output_file.write(json.dumps(events))

def main():
    parser = argparse.ArgumentParser(description='Process a file of JSON data from Notehub and convert into the geoJSON format.')
    parser.add_argument("-v", "--verbose", help="Enable verbose output", action="store_true")
    parser.add_argument('--infile', metavar='infile.json', type=str, required=True,
                    help='a JSON file with events from Notehub.io')
    parser.add_argument('--outfile', metavar='outfile.json', default='geojson-out.json',
                    help='the name of a file to output with geoJSON data')
    args = parser.parse_args()

    raw_json = fetch_input_json(args.infile)
    processed_events = process_json(raw_json)
    write_output(processed_events, args.outfile)


if __name__ == "__main__":
    main()