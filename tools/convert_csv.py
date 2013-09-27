#!/usr/bin/env python

import csv
import json

known_city_state = {
    "TULSA, OK": (36.1539816, -95.992775),
    "TULSA OK": (36.1539816, -95.992775),
    "TULSA,OK": (36.1539816, -95.992775),
    "TULSA": (36.1539816, -95.992775),
    "TULSA  OK": (36.1539816, -95.992775),
    "TULSA, OKLAHOMA": (36.1539816, -95.992775),
    "AUSTIN, TX": (30.267153, -97.7430608),
    "BARTLESVILLE, OK": (36.7473114, -95.9808179),
    "BETHANY, OK": (35.5186678, -97.6322639),
    "BROKEN ARROW OK": (36.0565606, -95.7835194),
    "BROKEN ARROW, OK": (36.0565606, -95.7835194),
    "BROOKLYN, NY": (40.65, -73.95),
    "DALLAS, TX": (32.7801399, -96.8004511),
    "DENVER, CO": (39.737567, -104.9847179),
    "EDMOND": (35.6528323, -97.4780954),
    "EDMOND, OK": (35.6528323, -97.4780954),
    "FAYETTEVILLE, AR": (36.0625795, -94.1574263),
    "JERSEY CITY, NJ": (40.7281575, -74.0776417),
    "LAFAYETTE, LA": (30.2240897, -92.0198427),
    "LITTLE ROCK, AR": (34.7464809, -92.2895948),
    "MADISON, WI": (43.0730517, -89.4012302),
    "MOORE, OK": (35.3395079, -97.4867028),
    "NORMAN, OK": (35.2225668, -97.4394777),
    "OKC": (35.4675602, -97.5164276),
    "OKC, OK": (35.4675602, -97.5164276),
    "OKLAHOMA CITY": (35.4675602, -97.5164276),
    "OKLAHOMA CITY, OK": (35.4675602, -97.5164276),
    "OWASSO, OK": (36.2695388, -95.8547119),
    "OWASSO,OK": (36.2695388, -95.8547119),
    "PO BOX 150035 TULSA, OK  74115": (36.1539816, -95.992775),
    "PRAUGE, OKLAHOMA": (35.4867368, -96.6850174),
    "STILLWATER, OK": (36.1156071, -97.0583681),
    "SUMMIT, NJ": (40.716111, -74.3625),
    "TAHLEQUAH, OK": (35.91537, -94.969956),
    "TUTTLE, OKLAHOMA": (35.2908947, -97.8122658),
    "WICHITA, KS": (37.6888889, -97.3361111),
}
seen_city_state = set()

extra_data = {
    'Luke Crouch': {
        "twitter" : "groovecoder",
        "github" : "groovecoder",
        "web" : "http://groovecoder.com"
    },
    'Jeremy Satterfield': {
        "github" : "jsatt"
    },
    "Patrick Forringer": {
        "twitter" : "destos",
        "github" : "destos",
        "awesome":"still",
        "web": "http://patrick.forringer.com"
    },
    "John Dungan": {
        "github" : "jdungan"
    },
    "Buddy Lindsey": {
        "github" : "buddylindsey",
        "twitter": "buddylindsey",
        "web": "http://buddylindsey.com",
    },
    "Blaine Blaine": {
        "name": "Blaine Schmeisser",
        "github" : "BlaineSch",
        "twitter": "BlaineSch",
        "web": "http://blainesch.com"
    },
    "Josh Mize": {
        "github" : "jgmize",
        "twitter": "jgmize",
        "web": "http://mozilla.org"
    },
}

def geocode(city_state):
    global known_city_state, seen_city_state
    cs = city_state.upper().strip()
    try:
        return known_city_state[cs]
    except KeyError:
        seen_city_state.add(cs)
        return -95.904638, 36.118914

def row_to_record(row):
    global extra_data
    num, date, last_name, first_name, email, reg_type, city_state, title, company = row
    lat, lon = geocode(city_state)
    full_name = ' '.join((first_name, last_name))
    record = {
        "type" : "Feature",
        "geometry" : {
            "type" : "Point",
            "coordinates" : [lon, lat]
        },
        "properties" :
            { "name" : full_name,
              "eventbrite_id": num,
              "email": email,
              "company": company,
              "location": city_state
            }
    }
    extra = extra_data.get(full_name, {})
    for key, val in extra.items():
        record['properties'][key] = val
    return record


def to_geo_json(csv_file):
    reader = csv.reader(csv_file)

    features = []
    collection = {
        "type": "FeatureCollection",
        "features": features
    }

    for row_count, row in enumerate(reader):
        if row_count == 0:
            continue
        else:
            record = row_to_record(row)
            features.append(record)
    return json.dumps(collection, indent=2)

if __name__ == '__main__':
    with open('attendees.csv', 'rU') as csv_file:
        out = to_geo_json(csv_file)
    if seen_city_state:
        for x in sorted(seen_city_state):
            print x
        print len(seen_city_state)
    else:
        print out
