#!/usr/bin/env npx tsx
/**
 * Compound Interest Calculator
 *
 * Calculate the future value of an investment with compound interest.
 *
 * Usage:
 *   npx tsx compound_interest.ts --principal 10000 --rate 0.05 --years 10
 *   npx tsx compound_interest.ts -p 10000 -r 0.05 -y 10 -n 4  # quarterly compounding
 */

interface CompoundInterestResult {
  principal: number;
  final_amount: number;
  interest_earned: number;
  effective_annual_rate: number;
  years: number;
  compounds_per_year: number;
}

/**
 * Calculate compound interest.
 *
 * @param principal - Initial investment amount
 * @param annualRate - Annual interest rate (as decimal, e.g., 0.05 for 5%)
 * @param years - Number of years
 * @param compoundsPerYear - How often interest compounds (default: 12 for monthly)
 * @returns Object with final_amount, interest_earned, and effective_rate
 */
function calculateCompoundInterest(
  principal: number,
  annualRate: number,
  years: number,
  compoundsPerYear: number = 12
): CompoundInterestResult {
  // A = P(1 + r/n)^(nt)
  const n = compoundsPerYear;
  const t = years;
  const r = annualRate;

  const finalAmount = principal * Math.pow(1 + r / n, n * t);
  const interestEarned = finalAmount - principal;
  const effectiveRate = Math.pow(1 + r / n, n) - 1;

  return {
    principal,
    final_amount: Math.round(finalAmount * 100) / 100,
    interest_earned: Math.round(interestEarned * 100) / 100,
    effective_annual_rate: Math.round(effectiveRate * 10000) / 100,
    years,
    compounds_per_year: compoundsPerYear,
  };
}

// Parse command line arguments
function parseArgs(): {
  principal: number;
  rate: number;
  years: number;
  compounds: number;
} {
  const args = process.argv.slice(2);
  let principal = 0;
  let rate = 0;
  let years = 0;
  let compounds = 12;

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    const nextArg = args[i + 1];

    if (arg === "-p" || arg === "--principal") {
      principal = parseFloat(nextArg);
      i++;
    } else if (arg === "-r" || arg === "--rate") {
      rate = parseFloat(nextArg);
      i++;
    } else if (arg === "-y" || arg === "--years") {
      years = parseInt(nextArg, 10);
      i++;
    } else if (arg === "-n" || arg === "--compounds") {
      compounds = parseInt(nextArg, 10);
      i++;
    }
  }

  if (!principal || !rate || !years) {
    console.error("Usage: npx tsx compound_interest.ts -p PRINCIPAL -r RATE -y YEARS [-n COMPOUNDS]");
    console.error("Example: npx tsx compound_interest.ts -p 10000 -r 0.05 -y 10");
    process.exit(1);
  }

  return { principal, rate, years, compounds };
}

// Main
const { principal, rate, years, compounds } = parseArgs();

const result = calculateCompoundInterest(principal, rate, years, compounds);

console.log(`Principal: $${result.principal.toLocaleString("en-US", { minimumFractionDigits: 2 })}`);
console.log(`Final Amount: $${result.final_amount.toLocaleString("en-US", { minimumFractionDigits: 2 })}`);
console.log(`Interest Earned: $${result.interest_earned.toLocaleString("en-US", { minimumFractionDigits: 2 })}`);
console.log(`Effective Annual Rate: ${result.effective_annual_rate}%`);
