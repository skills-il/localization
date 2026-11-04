#!/usr/bin/env python3
"""
Israeli Rental Budget Calculator

Calculates total monthly housing costs including rent, arnona (municipal tax),
vaad bayit (building committee), utilities, and optional insurance.

Usage:
    python scripts/rental-budget-calculator.py --rent 6000 --city tel-aviv --rooms 3
    python scripts/rental-budget-calculator.py --rent 4000 --city haifa --rooms 3 --oleh
    python scripts/rental-budget-calculator.py --rent 8000 --city herzliya --rooms 4 --parking
    python scripts/rental-budget-calculator.py --rent 5000 --city jerusalem --rooms 3 --lease-months 6 --broker
    python scripts/rental-budget-calculator.py --help
"""

import argparse
import sys


# Arnona rates per square meter per year (approximate, residential).
# Rough budgeting assumptions, not sourced figures. Each municipality sets its own rates per zone
# and building type in its annual arnona order (tzav arnona). Example: the Tel
# Aviv 2026 order charges apartments up to 140 sqm 46.64-112.99 NIS/sqm/year.
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

# Oleh arnona discount: up to 90% on the first 100 sqm, for 12 months chosen
# out of the first 24 months from population-registry registration.
# The actual rate is set by each municipality; after the discount period there
# is no universal rate, so we don't apply one.
OLEH_DISCOUNT = {
    "year_1": 0.90,  # up to 90% discount on the first 100 sqm portion only
    "description": "Olim may receive up to 90% arnona discount on the first 100 sqm for 12 months chosen within the first 24 months. The rate is set by each municipality; check locally.",
}

VAT_RATE = 0.18  # Israeli VAT, 18% since 1 January 2025

# Fair Rental Law (Rental and Loan Law s.25yod): securities that cost the
# tenant money are capped at the LOWER of 3 months' rent or the rent for 1/3 of
# the lease period. The chapter does not apply when monthly rent exceeds
# NIS 20,000 (a threshold the statute CPI-indexes every 1 January).
FAIR_RENT_THRESHOLD = 20000
SECURITY_CAP_MONTHS = 3

VALID_CITIES = list(ARNONA_RATES.keys())


def calculate_budget(rent, city, rooms, oleh=False, oleh_year=1, parking=False, insurance_opt=False,
                     lease_months=12, broker=False):
    """Calculate total monthly housing budget."""
    city_data = ARNONA_RATES.get(city)
    if not city_data:
        return None, f"Unknown city: {city}"

    sqm = ROOM_TO_SQM.get(rooms, round(70 + (rooms - 3) * 20))

    # Arnona calculation
    annual_arnona = city_data["rate_per_sqm"] * sqm
    if oleh:
        if oleh_year == 1:
            # 90% discount on the first 100 sqm portion only. Beyond 100 sqm
            # the full rate applies. Apportion accordingly.
            discounted_sqm = min(sqm, 100)
            full_rate_sqm = max(sqm - 100, 0)
            discounted_portion = city_data["rate_per_sqm"] * discounted_sqm * (1 - OLEH_DISCOUNT["year_1"])
            full_portion = city_data["rate_per_sqm"] * full_rate_sqm
            annual_arnona_after_discount = discounted_portion + full_portion
            arnona_discount = annual_arnona - annual_arnona_after_discount
        else:
            # Year-2+ rates vary by municipality; we don't apply an assumed
            # discount. Tell the user to check with the municipality.
            arnona_discount = 0
            annual_arnona_after_discount = annual_arnona
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
        "lease_months": lease_months,
        "broker": broker,
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
    lines.append(f"  Rooms:             {result['rooms']:g}")
    lines.append(f"  Est. size:         {result['sqm_estimate']} sqm")
    lines.append(f"  Monthly rent:      {result['rent']:,} NIS")
    if result["oleh"]:
        lines.append(f"  Oleh status:       Year {result['oleh_year']}")
        if result["oleh_year"] == 1:
            lines.append("    (Discount applies for 12 chosen months within the first 24;")
            lines.append("     shown here as a full-year estimate.)")
        else:
            lines.append("    (No discount applied. If you are still within 24 months of aliyah")
            lines.append("     and have not used all 12 discounted months, run with --oleh-year 1;")
            lines.append("     after that, the rate is set by each municipality.)")
    lines.append("")

    lines.append("-" * 60)
    lines.append("  MONTHLY COST BREAKDOWN")
    lines.append("-" * 60)
    lines.append("")

    lines.append(f"  {'Rent':<30} {result['rent']:>8,} NIS")

    # Arnona
    arnona_str = f"{result['monthly_arnona']:,.0f}"
    if result["oleh"] and result["arnona_discount"] > 0:
        lines.append(f"  {'Arnona (max oleh discount)':<30} {arnona_str:>8} NIS")
        lines.append("    (Assumes the maximum 90%; each municipality sets the actual rate.)")
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
    rent = result["rent"]
    lease_months = result["lease_months"]
    lines.append(f"    First month rent:             {rent:>8,} NIS")
    if rent > FAIR_RENT_THRESHOLD or lease_months <= 3:
        # Outside the Fair Rental chapter the statutory cap does not apply.
        deposit_low, deposit_high = rent, rent * SECURITY_CAP_MONTHS
        lines.append(f"    Security (typical 1-3 months): {deposit_low:>7,}-{deposit_high:,} NIS")
        if rent > FAIR_RENT_THRESHOLD:
            lines.append(f"      Rent above NIS {FAIR_RENT_THRESHOLD:,}/month: the Fair Rental Law security cap")
            lines.append("      may not apply to this lease (threshold is CPI-indexed each January).")
        else:
            lines.append("      Leases of 3 months or less are outside the Fair Rental Law unless")
            lines.append("      they carry an option to extend; with an option, the cap is 1/3 of the")
            lines.append("      lease (1 month for a 3-month lease).")
    else:
        cap_months = min(SECURITY_CAP_MONTHS, lease_months / 3)
        deposit_high = rent * cap_months
        deposit_low = min(rent, deposit_high)
        lines.append(f"    Security (1 month to cap):    {deposit_low:>8,.0f}-{deposit_high:,.0f} NIS")
        lines.append(f"      Statutory cap for a {lease_months}-month lease: lower of 3 months or 1/3")
        lines.append(f"      of the lease = {cap_months:.1f} months. Applies to bank guarantees and cash;")
        lines.append("      a security check or promissory note may be set higher.")
    move_in_low = rent + deposit_low
    move_in_high = rent + deposit_high
    if result["broker"]:
        broker_fee = rent * (1 + VAT_RATE)
        lines.append(f"    Broker fee (assumed):         {broker_fee:>8,.0f} NIS (1 month + {VAT_RATE:.0%} VAT;")
        lines.append("      use the amount in the written order you signed)")
        move_in_low += broker_fee
        move_in_high += broker_fee
    else:
        lines.append("    Broker fee:                          0 NIS (use --broker only if YOU signed")
        lines.append("      the broker's written order; a landlord's broker fee cannot be passed on)")
    lines.append(f"    Total move-in range:          {move_in_low:>7,.0f}-{move_in_high:,.0f} NIS")
    lines.append("    Not included: prepaid rent a landlord may ask for, bank-guarantee")
    lines.append("    commission, appliances or furniture, and moving costs.")
    lines.append("")
    lines.append("    Summer months with AC: electricity often runs "
                 f"{UTILITIES['electricity']['summer']['low']}-{UTILITIES['electricity']['summer']['high']} NIS.")

    lines.append("")
    lines.append("  Disclaimer: All figures are estimates. Actual costs vary")
    lines.append("  by specific apartment, building, and municipal zone.")
    lines.append("  Arnona rates are particularly variable within cities.")
    lines.append("  Vaad bayit, utilities, parking and insurance are rough")
    lines.append("  budgeting assumptions, not sourced figures.")
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
  %(prog)s --rent 5000 --city jerusalem --rooms 3.5 --lease-months 6 --broker

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
        type=float,
        required=True,
        help="Number of rooms (Israeli count, includes living room; halves like 3.5 allowed)",
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
    parser.add_argument(
        "--lease-months",
        type=int,
        default=12,
        help="Lease length in months, used for the statutory security cap (default: 12)",
    )
    parser.add_argument(
        "--broker",
        action="store_true",
        help="Include a broker fee (only if YOU signed the broker's written order)",
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

    if args.lease_months < 1 or args.lease_months > 120:
        print("Error: Lease length must be between 1 and 120 months.")
        sys.exit(1)

    result, error = calculate_budget(
        rent=args.rent,
        city=args.city,
        rooms=args.rooms,
        oleh=args.oleh,
        oleh_year=args.oleh_year,
        parking=args.parking,
        insurance_opt=args.insurance,
        lease_months=args.lease_months,
        broker=args.broker,
    )

    if error:
        print(f"Error: {error}")
        sys.exit(1)

    print(format_result(result))


if __name__ == "__main__":
    main()
