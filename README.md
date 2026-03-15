# mc-option-pricing

A Monte Carlo option pricing engine with path simulation written in **Rust** and a **Python** interface for pricing, Greeks, and visualization.

Built as a learning project to explore the intersection of quantitative finance and systems programming.

---

## Features

- **Path simulation in Rust** – fast, parallelized Monte Carlo simulation using Geometric Brownian Motion
- **European Call & Put pricing** – with discounted payoff averaging
- **Greeks** – Delta and Gamma via central finite differences
- **Black-Scholes validation** – analytical benchmark to verify MC results
- **Visualizations** – simulated paths, end-price distribution, payoff distribution, Delta curve
- **Benchmark** – 16x speedup over pure Python (using 4 threads, Rayon)

---

## Project Structure

```
mc-option-pricing/
├── src/
│   └── lib.rs                  # Rust: Path simulation (PyO3 + Rayon)
├── mc_option_pricing/
│   ├── pricing.py              # European Call & Put pricing
│   ├── black_scholes.py        # Analytical Black-Scholes formulas
│   ├── greeks.py               # Delta & Gamma via finite differences
│   └── python_sim.py        # Pure Python simulation (benchmark baseline)
├── notebooks/
│   └── demo.ipynb              # Visualizations & examples
├── Cargo.toml
└── pyproject.toml
```

---

## Methodology

### Geometric Brownian Motion

Stock prices are simulated using GBM:

$$S_{t+\Delta t} = S_t \cdot \exp\left(\left(\mu - \frac{\sigma^2}{2}\right)\Delta t + \sigma\sqrt{\Delta t}\, Z\right)$$

where $Z \sim \mathcal{N}(0, 1)$ is a standard normal random variable.

### Monte Carlo Pricing

The fair price of a European Call option is the discounted expected payoff under the risk-neutral measure:

$$C = e^{-rT} \cdot \frac{1}{N} \sum_{i=1}^{N} \max(S_T^{(i)} - K,\, 0)$$

### Greeks via Finite Differences

Delta and Gamma are estimated numerically:

$$\Delta = \frac{C(S_0 + h) - C(S_0 - h)}{2h}$$

$$\Gamma = \frac{C(S_0 + h) - 2C(S_0) + C(S_0 - h)}{h^2}$$

---

## Installation

**Requirements:** Python 3.8+, Rust toolchain

```bash
# Clone the repository
git clone https://github.com/NiklasK3R/mc-option-pricing.git
cd mc-option-pricing

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install Python dependencies
pip install maturin matplotlib numpy jupyter

# Compile Rust extension and install package
maturin develop
```

---

## Usage

### CLI
```bash
# Price an at-the-money call option
python -m mc_option_pricing

# Custom parameters
python -m mc_option_pricing --start 100 --strike 110 --sigma 0.3 --maturity 0.5 --type both

# All options
python -m mc_option_pricing --help
```

## Benchmark

Simulating 50,000 GBM paths (252 steps each):

| Implementation         | Time    | Speedup |
|------------------------|---------|---------|
| Pure Python            | ~9.0s   | 1x      |
| Rust (single-threaded) | ~1.0s   | ~9x     |
| Rust (4 threads)       | ~0.56s  | ~16x    |

Parallelization is handled transparently via [Rayon](https://github.com/rayon-rs/rayon).

---

## Example Results

At-the-money call option (`S=100, K=100, r=5%, σ=20%, T=1yr`):

| Method        | Price   |
|---------------|---------|
| Black-Scholes | 10.4506 |
| Monte Carlo   | 10.4281 |
| Difference    | 0.0225  |

---

## Tech Stack

- **Rust** – path simulation engine
- **PyO3** – Rust/Python bindings
- **Rayon** – data parallelism in Rust
- **maturin** – build system for Rust Python extensions
- **Python** – pricing logic, Greeks, visualization
- **matplotlib / numpy** – plots and numerical utilities

---

## License

MIT