#!/usr/bin/env python3
"""
Compound Interest Calculator

Calculate the future value of an investment with compound interest.

Usage:
    python compound_interest.py --principal 10000 --rate 0.05 --years 10
    python compound_interest.py -p 10000 -r 0.05 -y 10 -n 4  # quarterly compounding
"""

import argparse


def calculate_compound_interest(
    principal: float,
    annual_rate: float,
    years: int,
    compounds_per_year: int = 12,
) -> dict:
    """
    Calculate compound interest.

    Args:
        principal: Initial investment amount
        annual_rate: Annual interest rate (as decimal, e.g., 0.05 for 5%)
        years: Number of years
        compounds_per_year: How often interest compounds (default: 12 for monthly)

    Returns:
        Dictionary with final_amount, interest_earned, and effective_rate
    """
    # A = P(1 + r/n)^(nt)
    n = compounds_per_year
    t = years
    r = annual_rate

    final_amount = principal * (1 + r / n) ** (n * t)
    interest_earned = final_amount - principal
    effective_rate = (1 + r / n) ** n - 1

    return {
        "principal": principal,
        "final_amount": round(final_amount, 2),
        "interest_earned": round(interest_earned, 2),
        "effective_annual_rate": round(effective_rate * 100, 4),
        "years": years,
        "compounds_per_year": compounds_per_year,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate compound interest")
    parser.add_argument("-p", "--principal", type=float, required=True, help="Initial investment amount")
    parser.add_argument("-r", "--rate", type=float, required=True, help="Annual interest rate as decimal (e.g., 0.05 for 5%%)")
    parser.add_argument("-y", "--years", type=int, required=True, help="Number of years")
    parser.add_argument("-n", "--compounds", type=int, default=12, help="Compounds per year (default: 12 for monthly)")

    args = parser.parse_args()

    result = calculate_compound_interest(
        principal=args.principal,
        annual_rate=args.rate,
        years=args.years,
        compounds_per_year=args.compounds,
    )

    print(f"Principal: ${result['principal']:,.2f}")
    print(f"Final Amount: ${result['final_amount']:,.2f}")
    print(f"Interest Earned: ${result['interest_earned']:,.2f}")
    print(f"Effective Annual Rate: {result['effective_annual_rate']}%")
