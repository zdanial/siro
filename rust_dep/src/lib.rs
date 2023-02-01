use pyo3::prelude::*;
mod sir;

/// Formats the sum of two numbers as string.
#[pyfunction]
fn sir(runtime: f32, dt: f32, (S, I, R): (f32, f32, f32), (Beta, Gamma, Alpha): (Vec<f32>, Vec<f32>, Vec<f32>)) -> PyResult<String> {
    sir::run(
        runtime,
        dt.
        sir::SIR{S, I, R},
        sir::Parameters(Beta, Gamma, Alpha)
    )
}

/// A Python module implemented in Rust. The name of this function must match
/// the `lib.name` setting in the `Cargo.toml`, else Python will not be able to
/// import the module.
#[pymodule]
fn sirO(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sir, m)?)?;
    Ok(())
}