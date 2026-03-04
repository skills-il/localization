#!/usr/bin/env python3
"""Plan routes between Israeli cities with transport options.

Calculates distances and suggests transportation modes between
major Israeli cities and tourist destinations.

Usage:
    python plan_route.py --from "tel-aviv" --to "jerusalem"
    python plan_route.py --from "haifa" --to "eilat"
    python plan_route.py --help

Requirements:
    Python 3.9+ (no external dependencies)
"""

import argparse
import sys


# Distance matrix (km) between major cities
DISTANCES = {
    ("tel-aviv", "jerusalem"): 60,
    ("tel-aviv", "haifa"): 95,
    ("tel-aviv", "beer-sheva"): 115,
    ("tel-aviv", "eilat"): 350,
    ("tel-aviv", "tiberias"): 130,
    ("tel-aviv", "netanya"): 30,
    ("tel-aviv", "ashdod"): 35,
    ("jerusalem", "haifa"): 155,
    ("jerusalem", "beer-sheva"): 80,
    ("jerusalem", "eilat"): 310,
    ("jerusalem", "dead-sea"): 40,
    ("jerusalem", "tiberias"): 165,
    ("haifa", "tiberias"): 65,
    ("haifa", "nazareth"): 35,
    ("haifa", "akko"): 25,
    ("haifa", "nahariya"): 35,
    ("beer-sheva", "eilat"): 240,
    ("beer-sheva", "dead-sea"): 100,
}

# Transport options with estimated times
TRANSPORT = {
    "train": {"name": "רכבת ישראל", "speed_kmh": 90, "note": "Sunday-Thursday + Friday morning"},
    "bus": {"name": "אוטובוס", "speed_kmh": 60, "note": "Egged/Dan/Kavim -- no Shabbat service"},
    "car": {"name": "רכב פרטי", "speed_kmh": 80, "note": "Toll roads: Highway 6, Carmel Tunnels"},
    "sherut": {"name": "מונית שירות", "speed_kmh": 70, "note": "Shared taxi -- runs on Shabbat"},
}

# Train routes (city pairs served by Israel Railways)
TRAIN_ROUTES = {
    ("tel-aviv", "jerusalem"), ("tel-aviv", "haifa"), ("tel-aviv", "beer-sheva"),
    ("tel-aviv", "netanya"), ("tel-aviv", "ashdod"), ("haifa", "nahariya"),
    ("haifa", "akko"),
}

CITY_NAMES_HE = {
    "tel-aviv": "תל אביב",
    "jerusalem": "ירושלים",
    "haifa": "חיפה",
    "beer-sheva": "באר שבע",
    "eilat": "אילת",
    "tiberias": "טבריה",
    "netanya": "נתניה",
    "ashdod": "אשדוד",
    "dead-sea": "ים המלח",
    "nazareth": "נצרת",
    "akko": "עכו",
    "nahariya": "נהריה",
}


def get_distance(city_a, city_b):
    """Get distance between two cities."""
    key = (city_a, city_b)
    if key in DISTANCES:
        return DISTANCES[key]
    key = (city_b, city_a)
    if key in DISTANCES:
        return DISTANCES[key]
    return None


def has_train(city_a, city_b):
    """Check if train service exists between cities."""
    return (city_a, city_b) in TRAIN_ROUTES or (city_b, city_a) in TRAIN_ROUTES


def plan_route(origin, destination):
    """Plan a route between two cities."""
    distance = get_distance(origin, destination)
    if distance is None:
        print(f"No route data for {origin} -> {destination}")
        return

    origin_he = CITY_NAMES_HE.get(origin, origin)
    dest_he = CITY_NAMES_HE.get(destination, destination)

    print(f"\nRoute: {origin_he} -> {dest_he}")
    print(f"Distance: {distance} km\n")
    print("Transport options:")
    print("-" * 60)

    for mode, info in TRANSPORT.items():
        if mode == "train" and not has_train(origin, destination):
            print(f"  {info['name']}: No direct train service")
            continue

        hours = distance / info["speed_kmh"]
        mins = int(hours * 60)
        print(f"  {info['name']}: ~{mins} min ({info['note']})")

    print()


def main():
    cities = list(CITY_NAMES_HE.keys())
    parser = argparse.ArgumentParser(description="Plan routes between Israeli cities")
    parser.add_argument("--from", dest="origin", required=True, choices=cities)
    parser.add_argument("--to", dest="destination", required=True, choices=cities)
    args = parser.parse_args()

    plan_route(args.origin, args.destination)


if __name__ == "__main__":
    main()
