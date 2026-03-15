from mc_option_pricing.pricing import price_european_call

# Numerical approximation of Delta and Gamma using finite differences
def delta(
    start: float,
    strike: float,
    risk_free: float,
    sigma: float,
    maturity: float,
    n: int = 100_000,
    h: float = 1.0,
    seed: int = 42,
    ) -> float:
    params = dict(strike=strike, risk_free=risk_free, sigma=sigma, maturity=maturity, n=n, seed=seed)

    price_up = price_european_call(start + h, **params)["price"]
    price_down = price_european_call(start - h, **params)["price"]

    return (price_up - price_down) / (2 * h)

def gamma(
    start: float,
    strike: float,
    risk_free: float,
    sigma: float,
    maturity: float,
    n: int = 100_000,
    h: float = 1.0,
    seed: int = 42,
) -> float:
    params = dict(strike=strike, risk_free=risk_free, sigma=sigma, maturity=maturity, n=n, seed=seed)

    price_up = price_european_call(start + h, **params)["price"]
    price_mid = price_european_call(start, **params)["price"]
    price_down = price_european_call(start - h, **params)["price"]

    return (price_up - 2 * price_mid + price_down) / (h ** 2)
