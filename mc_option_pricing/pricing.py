import rust_pathsim
import math

# Monte Carlo simulation for European option pricing using geometric Brownian motion
def price_european_call(
    start: float,
    strike: float,
    risk_free: float,
    sigma: float,
    maturity: float,
    n: int,
    seed: int = 42,
) -> dict:
    steps = int(maturity * 252)
    dt = maturity / steps

    # Simulate end prices using Rust for performance
    end_prices = rust_pathsim.rust_simulation(
        start,
        risk_free,
        sigma,
        dt,
        steps,
        seed,
        n,
    )

    # Calculate payoffs and discount to present value
    payoffs = [max(0, price - strike) for price in end_prices]
    discount = math.exp(-risk_free * maturity)
    price = discount * sum(payoffs) / n

    mean_payoff = sum(payoffs) / n
    variance = sum((payoff - mean_payoff) ** 2 for payoff in payoffs) / (n - 1)
    std_error = math.sqrt(variance / n)

    return {
        "price": price,
        "std_error": std_error,
        "confidence_interval": (price - 1.96 * std_error, price + 1.96 * std_error),
        "n": n,
    }

# Put-call parity to price European put option
def price_european_put(
    start: float,
    strike: float,
    risk_free: float,
    sigma: float,
    maturity: float,
    n: int,
    seed: int = 42,
) -> dict:
    call = price_european_call(
        start,
        strike,
        risk_free,
        sigma,
        maturity,
        n,
        seed,
    )
    put_price = call["price"] - start + strike * math.exp(-risk_free * maturity)
    return {
        "price": put_price,
        "n": n,
    }