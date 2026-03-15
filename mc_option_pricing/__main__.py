import argparse
from mc_option_pricing.pricing import price_european_call, price_european_put
from mc_option_pricing.black_scholes import black_scholes_call, black_scholes_delta, black_scholes_gamma
from mc_option_pricing.greeks import delta, gamma

# Main function to run the command-line interface for the Monte Carlo option pricing engine
def main():
    parser = argparse.ArgumentParser(
        description="Monte Carlo Option Pricing Engine (Rust-accelerated)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    # Parameter
    parser.add_argument("--start",     type=float, default=100.0, help="Current stock price")
    parser.add_argument("--strike",    type=float, default=100.0, help="Option strike price")
    parser.add_argument("--risk-free", type=float, default=0.05,  help="Risk-free rate (e.g. 0.05 for 5%%)")
    parser.add_argument("--sigma",     type=float, default=0.2,   help="Volatility (e.g. 0.2 for 20%%)")
    parser.add_argument("--maturity",  type=float, default=1.0,   help="Time to maturity in years")
    parser.add_argument("--n",   type=int,   default=100_000, help="Number of simulated paths")
    parser.add_argument("--seed",      type=int,   default=42,    help="Random seed for reproducibility")
    parser.add_argument("--type",      choices=["call", "put", "both"], default="call", help="Option type")

    args = parser.parse_args()

    params = dict(
        start     = args.start,
        strike    = args.strike,
        risk_free = args.risk_free,
        sigma     = args.sigma,
        maturity  = args.maturity,
        n   = args.n,
        seed      = args.seed,
    )

    greeks_params = dict(
        start     = args.start,
        strike    = args.strike,
        risk_free = args.risk_free,
        sigma     = args.sigma,
        maturity  = args.maturity,
        n   = args.n,
        seed      = args.seed,
    )

    # Header
    print("\n" + "=" * 50)
    print("  MC Option Pricing Engine")
    print("=" * 50)
    print(f"  Stock Price:   {args.start}")
    print(f"  Strike:        {args.strike}")
    print(f"  Risk-free:     {args.risk_free:.1%}")
    print(f"  Volatility:    {args.sigma:.1%}")
    print(f"  Maturity:      {args.maturity}yr")
    print(f"  Paths:         {args.n:,}")
    print("=" * 50)

    # Call
    if args.type in ("call", "both"):
        mc   = price_european_call(**params)
        bs   = black_scholes_call(args.start, args.strike, args.risk_free, args.sigma, args.maturity)
        d    = delta(**greeks_params)
        g    = gamma(**greeks_params)

        print("\n  CALL OPTION")
        print(f"  {'MC Price:':20} {mc['price']:.4f}  ± {mc['std_error']:.4f}")
        print(f"  {'Black-Scholes:':20} {bs:.4f}")
        print(f"  {'Difference:':20} {abs(mc['price'] - bs):.4f}")
        print(f"  {'95% CI:':20} ({mc['confidence_interval'][0]:.4f}, {mc['confidence_interval'][1]:.4f})")
        print(f"  {'Delta:':20} {d:.4f}  (BS: {black_scholes_delta(args.start, args.strike, args.risk_free, args.sigma, args.maturity):.4f})")
        print(f"  {'Gamma:':20} {g:.4f}  (BS: {black_scholes_gamma(args.start, args.strike, args.risk_free, args.sigma, args.maturity):.4f})")

    # Put
    if args.type in ("put", "both"):
        mc_put = price_european_put(**params)

        print("\n  PUT OPTION")
        print(f"  {'MC Price:':20} {mc_put['price']:.4f}")

    print("\n" + "=" * 50 + "\n")


if __name__ == "__main__":
    main()