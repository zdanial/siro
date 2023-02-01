use pyo3::prelude::*;
mod sir;

/// Formats the sum of two numbers as string.
#[pyfunction]
#[pyo3(name = "sir")]
fn sir_rs(runtime: f32, dt: f32, S:f32, I:f32, R:f32, Beta:Vec<f32>, Gamma:Vec<f32>, Alpha:Vec<f32>) -> PyResult<(Vec<f32>, Vec<f32>, Vec<f32>)> {
    let initial_state = sir::SIR::new(S, I, R);
    let params = sir::Parameters::new(Beta, Gamma, Alpha);
    let res = sir::run(
        runtime,
        dt,
        initial_state,
        params
    );
    Ok((res.S, res.I, res.R))
}

/// A Python module implemented in Rust. The name of this function must match
/// the `lib.name` setting in the `Cargo.toml`, else Python will not be able to
/// import the module.
#[pymodule]
fn sirO(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_class::<sir::Results>()?;
    m.add_function(wrap_pyfunction!(sir_rs, m)?)?;
    Ok(())
}