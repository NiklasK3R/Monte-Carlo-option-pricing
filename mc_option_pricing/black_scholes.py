import math

# Black-Scholes formula for European call option pricing
def black_scholes_call(
    start: float,
    strike: float,
    risk_free: float,
    sigma: float,
    maturity: float,
) -> float:
    d1 = (math.log(start / strike) + (risk_free + 0.5 * sigma ** 2) * maturity) / (sigma * math.sqrt(maturity))
    d2 = d1 - sigma * math.sqrt(maturity)

    call_price = start * _norm_cdf(d1) - strike * math.exp(-risk_free * maturity) * _norm_cdf(d2)
    return call_price


# Black-Scholes formula for Delta of a European call option
def black_scholes_delta(
    start: float,
    strike: float,
    risk_free: float,
    sigma: float,
    maturity: float,
) -> float:
    d1 = (math.log(start / strike) + (risk_free + 0.5 * sigma ** 2) * maturity) / (sigma * math.sqrt(maturity))
    return _norm_cdf(d1)

# Black-Scholes formula for Gamma of a European call option
def black_scholes_gamma(
    start: float,
    strike: float,
    risk_free: float,
    sigma: float,
    maturity: float,
) -> float:
    d1 = (math.log(start / strike) + (risk_free + 0.5 * sigma ** 2) * maturity) / (sigma * math.sqrt(maturity))
    return math.exp(-0.5 * d1 ** 2) / (start * sigma * math.sqrt(2 * math.pi * maturity))

def _norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2)))