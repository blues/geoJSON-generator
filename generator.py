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
    journey_map = {}

    for event in raw_json:
        if event["file"] == "_track.qo":
            body = event["body"]
            geo_point = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        event["value"]["best_lon"],
                        event["value"]["best_lat"]
                    ]
                },
                "properties": {
                    "serial": event["serial"],
                    "combinedwhen": event["combinedwhen"],
                    "when": event["when"],
                    "modified": event["modified"],
                    "where": event["where"],
                    "device": event["device"],
                    "body": body,
                    "value": event["value"]
                }
            }
            if body["journey"] not in journey_map:
                journey_map[body["journey"]] = []
            journey_map[body["journey"]].append({
                "jcount": body["jcount"],
                "coordinates": [
                    event["value"]["best_lon"],
                    event["value"]["best_lat"]
                ]
            })
            processed_json["features"].append(geo_point)

    # order journey_map
    for journey in journey_map:
        journey_map[journey] = sorted(journey_map[journey], key=lambda d: d["jcount"])
        journey_map[journey] = {
            "type": "LineString",
            "coordinates": [d["coordinates"] for d in journey_map[journey]]
        }
    return processed_json, journey_map

def write_output(events, journies, outfile):
    with open(outfile,'w',encoding = 'utf-8') as output_file:
        output_file.write(json.dumps(events))
    for journey in journies:
        with open(f'geojson-journey-{journey}.json','w',encoding = 'utf-8') as output_file:
            output_file.write(json.dumps(journies[journey]))

def main():
    parser = argparse.ArgumentParser(description='Process a file of JSON data from Notehub and convert into the geoJSON format.')
    parser.add_argument("-v", "--verbose", help="Enable verbose output", action="store_true")
    parser.add_argument('--infile', metavar='infile.json', type=str, required=True,
                    help='a JSON file with events from Notehub.io')
    parser.add_argument('--outfile', metavar='outfile.json', default='geojson-points.json',
                    help='the name of a file to output with geoJSON data')
    args = parser.parse_args()

    raw_json = fetch_input_json(args.infile)
    processed_events, processed_journies = process_json(raw_json)
    write_output(processed_events, processed_journies, args.outfile)


if __name__ == "__main__":
    main()