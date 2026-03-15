import math
import random

# Pure Python implementation of path simulation for testing and benchmarking
def python_pathsim(
    start: float,
    ex_yield: float,
    sigma: float,
    dt: float,
    steps: int,
    n: int,
    seed: int = 42, 
) -> list[float]:
    rng = random.Random(seed)
    end_prices = []
    drift = (ex_yield - 0.5 * sigma ** 2) * dt
    diffusion = sigma * math.sqrt(dt)

    for _ in range(n):
        price = start
        for _ in range(steps):
            z = rng.gauss(0, 1)
            price *= math.exp(drift + diffusion * z)
        end_prices.append(price)
    return end_prices
