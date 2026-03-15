use pyo3::prelude::*;
use rand::SeedableRng;
use rand_distr::{Distribution, Normal};
use rayon::prelude::*;


// Simulate a single path of the geometric Brownian motion model
fn simulate_path(
    start: f64,
    ex_yield: f64,
    sigma: f64,
    dt: f64,
    steps: usize,
    rng: &mut impl rand::Rng,
) -> f64 {
    let normal = Normal::new(0.0, 1.0).unwrap();
    let mut price = start;

    for _ in 0..steps {
        let z = normal.sample(rng);
        price *= ((ex_yield - 0.5 * sigma * sigma) * dt + (sigma * dt.sqrt() * z)).exp();
    }

    price

}


// Python wrapper for the Rust simulation function + parallelization using Rayon
#[pyfunction]
fn rust_simulation(
    start: f64,
    ex_yield: f64,
    sigma: f64,
    dt: f64,
    steps: usize,
    seed: u64,
    n: usize,
) -> Vec<f64> {

    (0..n)
        .into_par_iter()
        .map(|i| {
            let mut rng = rand_pcg::Pcg64::seed_from_u64(seed + i as u64);
            simulate_path(start, ex_yield, sigma, dt, steps, &mut rng)
        })
        .collect()
}


// Defining the Python module
#[pymodule]
fn rust_pathsim(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(rust_simulation, m)?)?;
    Ok(())
}
