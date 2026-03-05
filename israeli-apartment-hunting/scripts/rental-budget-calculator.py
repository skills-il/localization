#!/usr/bin/env python3
"""
Israeli Rental Budget Calculator

Calculates total monthly housing costs including rent, arnona (municipal tax),
vaad bayit (building committee), utilities, and optional insurance.

Usage:
    python scripts/rental-budget-calculator.py --rent 6000 --city tel-aviv --rooms 3
    python scripts/rental-budget-calculator.py --rent 4000 --city haifa --rooms 3 --oleh
    python scripts/rental-budget-calculator.py --rent 8000 --city herzliya --rooms 4 --parking
    python scripts/rental-budget-calculator.py --help
"""

import argparse
import sys


# Arnona rates per square meter per year (approximate, residential)
# These are rough averages; actual rates depend on zone within each city
ARNONA_RATES = {
    "tel-aviv": {"rate_per_sqm": 90, "label": "Tel Aviv"},
    "jerusalem": {"rate_per_sqm": 65, "label": "Jerusalem"},
    "haifa": {"rate_per_sqm": 48, "label": "Haifa"},
    "beer-sheva": {"rate_per_sqm": 38, "label": "Be'er Sheva"},
    "herzliya": {"rate_per_sqm": 78, "label": "Herzliya"},
    "raanana": {"rate_per_sqm": 72, "label": "Ra'anana"},
    "netanya": {"rate_per_sqm": 55, "label": "Netanya"},
    "rishon": {"rate_per_sqm": 60, "label": "Rishon LeZion"},
    "petah-tikva": {"rate_per_sqm": 58, "label": "Petah Tikva"},
    "rehovot": {"rate_per_sqm": 55, "label": "Rehovot"},
    "ashdod": {"rate_per_sqm": 45, "label": "Ashdod"},
    "other": {"rate_per_sqm": 55, "label": "Other city"},
}

# Approximate sqm by room count
ROOM_TO_SQM = {
    2: 50,
    3: 70,
    4: 90,
    5: 110,
    6: 130,
}

# Vaad bayit ranges by city (monthly)
VAAD_BAYIT = {
    "tel-aviv": {"low": 200, "high": 500},
    "jerusalem": {"low": 150, "high": 350},
    "haifa": {"low": 100, "high": 300},
    "beer-sheva": {"low": 80, "high": 250},
    "herzliya": {"low": 200, "high": 500},
    "raanana": {"low": 200, "high": 450},
    "netanya": {"low": 150, "high": 350},
    "rishon": {"low": 150, "high": 350},
    "petah-tikva": {"low": 150, "high": 350},
    "rehovot": {"low": 130, "high": 300},
    "ashdod": {"low": 100, "high": 300},
    "other": {"low": 150, "high": 350},
}

# Utility estimates (monthly)
UTILITIES = {
    "electricity": {"summer": {"low": 300, "high": 600}, "average": {"low": 200, "high": 400}},
    "water": {"low": 80, "high": 200},
    "gas": {"low": 50, "high": 120},
    "internet": {"low": 100, "high": 200},
}

# Insurance (optional)
INSURANCE = {
    "contents": {"low": 50, "high": 150},
    "third_party": {"low": 30, "high": 80},
}

# Parking costs (if not included)
PARKING_COSTS = {
    "tel-aviv": {"low": 400, "high": 800},
    "jerusalem": {"low": 200, "high": 500},
    "haifa": {"low": 150, "high": 350},
    "beer-sheva": {"low": 100, "high": 250},
    "herzliya": {"low": 300, "high": 600},
    "raanana": {"low": 250, "high": 500},
    "netanya": {"low": 150, "high": 350},
    "rishon": {"low": 200, "high": 400},
    "petah-tikva": {"low": 200, "high": 400},
    "rehovot": {"low": 150, "high": 350},
    "ashdod": {"low": 100, "high": 300},
    "other": {"low": 200, "high": 400},
}

# Oleh arnona discount
OLEH_DISCOUNT = {
    "year_1": 0.90,  # 90% discount
    "year_2": 0.70,  # 70% discount (varies by municipality)
    "description": "New olim may receive up to 90% arnona discount in year 1",
}

VALID_CITIES = list(ARNONA_RATES.keys())


def calculate_budget(rent, city, rooms, oleh=False, oleh_year=1, parking=False, insurance_opt=False):
    """Calculate total monthly housing budget."""
    city_data = ARNONA_RATES.get(city)
    if not city_data:
        return None, f"Unknown city: {city}"

    sqm = ROOM_TO_SQM.get(rooms, 70 + (rooms - 3) * 20)

    # Arnona calculation
    annual_arnona = city_data["rate_per_sqm"] * sqm
    if oleh:
        if oleh_year == 1:
            discount = OLEH_DISCOUNT["year_1"]
        elif oleh_year == 2:
            discount = OLEH_DISCOUNT["year_2"]
        else:
            discount = 0
        arnona_discount = annual_arnona * discount
        annual_arnona_after_discount = annual_arnona - arnona_discount
    else:
        arnona_discount = 0
        annual_arnona_after_discount = annual_arnona

    monthly_arnona = annual_arnona_after_discount / 12

    # Vaad bayit
    vaad = VAAD_BAYIT.get(city, VAAD_BAYIT["other"])

    # Utilities
    elec = UTILITIES["electricity"]["average"]
    water = UTILITIES["water"]
    gas = UTILITIES["gas"]
    internet = UTILITIES["internet"]

    utilities_low = elec["low"] + water["low"] + gas["low"] + internet["low"]
    utilities_high = elec["high"] + water["high"] + gas["high"] + internet["high"]

    # Insurance
    if insurance_opt:
        ins_low = INSURANCE["contents"]["low"] + INSURANCE["third_party"]["low"]
        ins_high = INSURANCE["contents"]["high"] + INSURANCE["third_party"]["high"]
    else:
        ins_low = 0
        ins_high = 0

    # Parking
    if parking:
        park = PARKING_COSTS.get(city, PARKING_COSTS["other"])
        park_low = park["low"]
        park_high = park["high"]
    else:
        park_low = 0
        park_high = 0

    # Totals
    total_low = rent + monthly_arnona + vaad["low"] + utilities_low + ins_low + park_low
    total_high = rent + monthly_arnona + vaad["high"] + utilities_high + ins_high + park_high

    return {
        "rent": rent,
        "city": city_data["label"],
        "rooms": rooms,
        "sqm_estimate": sqm,
        "monthly_arnona": monthly_arnona,
        "annual_arnona": annual_arnona_after_discount,
        "arnona_before_discount": annual_arnona,
        "oleh": oleh,
        "oleh_year": oleh_year if oleh else None,
        "arnona_discount": arnona_discount,
        "vaad_low": vaad["low"],
        "vaad_high": vaad["high"],
        "utilities_low": utilities_low,
        "utilities_high": utilities_high,
        "utilities_breakdown": {
            "electricity": elec,
            "water": water,
            "gas": gas,
            "internet": internet,
        },
        "insurance_low": ins_low,
        "insurance_high": ins_high,
        "insurance_included": insurance_opt,
        "parking_low": park_low,
        "parking_high": park_high,
        "parking_included": parking,
        "total_low": total_low,
        "total_high": total_high,
    }, None


def format_result(result):
    """Format the budget calculation for display."""
    lines = []
    lines.append("")
    lines.append("=" * 60)
    lines.append("  ISRAELI RENTAL BUDGET CALCULATOR")
    lines.append("=" * 60)
    lines.append("")
    lines.append(f"  City:              {result['city']}")
    lines.append(f"  Rooms:             {result['rooms']}")
    lines.append(f"  Est. size:         {result['sqm_estimate']} sqm")
    lines.append(f"  Monthly rent:      {result['rent']:,} NIS")
    if result["oleh"]:
        lines.append(f"  Oleh status:       Year {result['oleh_year']}")
    lines.append("")

    lines.append("-" * 60)
    lines.append("  MONTHLY COST BREAKDOWN")
    lines.append("-" * 60)
    lines.append("")

    lines.append(f"  {'Rent':<30} {result['rent']:>8,} NIS")

    # Arnona
    arnona_str = f"{result['monthly_arnona']:,.0f}"
    if result["oleh"] and result["arnona_discount"] > 0:
        lines.append(f"  {'Arnona (with oleh discount)':<30} {arnona_str:>8} NIS")
        lines.append(f"    (Before discount: {result['arnona_before_discount']:,.0f} NIS/year)")
        lines.append(f"    (Discount: {result['arnona_discount']:,.0f} NIS/year)")
    else:
        lines.append(f"  {'Arnona (municipal tax)':<30} {arnona_str:>8} NIS")

    # Vaad bayit
    lines.append(f"  {'Vaad bayit':<30} {result['vaad_low']:>4,}-{result['vaad_high']:,} NIS")

    # Utilities
    lines.append(f"  {'Utilities (total)':<30} {result['utilities_low']:>4,}-{result['utilities_high']:,} NIS")
    for name, vals in result["utilities_breakdown"].items():
        if isinstance(vals, dict) and "low" in vals:
            label = name.replace("_", " ").title()
            lines.append(f"    {label:<28} {vals['low']:>4,}-{vals['high']:,}")

    # Insurance
    if result["insurance_included"]:
        lines.append(f"  {'Insurance (contents + 3rd party)':<30} {result['insurance_low']:>4,}-{result['insurance_high']:,} NIS")

    # Parking
    if result["parking_included"]:
        lines.append(f"  {'Parking (rental)':<30} {result['parking_low']:>4,}-{result['parking_high']:,} NIS")

    lines.append("")
    lines.append("-" * 60)
    lines.append(f"  {'TOTAL MONTHLY COST':<30} {result['total_low']:>7,.0f}-{result['total_high']:,.0f} NIS")
    lines.append(f"  {'TOTAL ANNUAL COST':<30} {result['total_low'] * 12:>7,.0f}-{result['total_high'] * 12:,.0f} NIS")
    lines.append("-" * 60)

    # One-time costs section
    lines.append("")
    lines.append("  ONE-TIME MOVE-IN COSTS (estimated):")
    broker_fee = result["rent"] * 1.17  # rent + VAT
    lines.append(f"    Broker fee (if applicable):   {broker_fee:>8,.0f} NIS (1 month + 17% VAT)")
    lines.append(f"    Security deposit (1-3 months): {result['rent']:>7,}-{result['rent'] * 3:,} NIS")
    lines.append(f"    First month rent:             {result['rent']:>8,} NIS")
    move_in_low = result["rent"] * 2  # first month + 1 month deposit (no broker)
    move_in_high = result["rent"] * 3 + broker_fee  # first month + 3 month deposit + broker
    lines.append(f"    Total move-in range:          {move_in_low:>7,}-{move_in_high:,.0f} NIS")

    # Income recommendation
    lines.append("")
    lines.append("  INCOME RECOMMENDATION:")
    recommended_income_low = result["total_low"] * 3
    recommended_income_high = result["total_high"] * 3
    lines.append(f"    Suggested gross salary:       {recommended_income_low:>7,.0f}-{recommended_income_high:,.0f} NIS/month")
    lines.append("    (Rule of thumb: housing should be ~30% of gross income)")

    lines.append("")
    lines.append("  Disclaimer: All figures are estimates. Actual costs vary")
    lines.append("  by specific apartment, building, and municipal zone.")
    lines.append("  Arnona rates are particularly variable within cities.")
    lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Calculate total monthly housing costs for renting in Israel.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --rent 6000 --city tel-aviv --rooms 3
  %(prog)s --rent 4000 --city haifa --rooms 3 --oleh
  %(prog)s --rent 8000 --city herzliya --rooms 4 --parking --insurance
  %(prog)s --rent 3000 --city beer-sheva --rooms 3 --oleh --oleh-year 2

Cities: tel-aviv, jerusalem, haifa, beer-sheva, herzliya, raanana,
        netanya, rishon, petah-tikva, rehovot, ashdod, other
        """,
    )

    parser.add_argument(
        "--rent",
        type=int,
        required=True,
        help="Monthly rent in NIS",
    )
    parser.add_argument(
        "--city",
        required=True,
        choices=VALID_CITIES,
        help="City where the apartment is located",
    )
    parser.add_argument(
        "--rooms",
        type=int,
        required=True,
        help="Number of rooms (Israeli count, includes living room)",
    )
    parser.add_argument(
        "--oleh",
        action="store_true",
        help="Apply oleh chadash (new immigrant) arnona discount",
    )
    parser.add_argument(
        "--oleh-year",
        type=int,
        default=1,
        choices=[1, 2],
        help="Year of aliyah for arnona discount (1 or 2, default: 1)",
    )
    parser.add_argument(
        "--parking",
        action="store_true",
        help="Include separate parking rental cost",
    )
    parser.add_argument(
        "--insurance",
        action="store_true",
        help="Include apartment insurance (contents + third-party)",
    )

    args = parser.parse_args()

    # Validate rent
    if args.rent < 500 or args.rent > 50000:
        print("Error: Rent must be between 500 and 50,000 NIS.")
        sys.exit(1)

    # Validate rooms
    if args.rooms < 1 or args.rooms > 8:
        print("Error: Rooms must be between 1 and 8.")
        sys.exit(1)

    result, error = calculate_budget(
        rent=args.rent,
        city=args.city,
        rooms=args.rooms,
        oleh=args.oleh,
        oleh_year=args.oleh_year,
        parking=args.parking,
        insurance_opt=args.insurance,
    )

    if error:
        print(f"Error: {error}")
        sys.exit(1)

    print(format_result(result))


if __name__ == "__main__":
    main()
