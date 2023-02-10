use pyo3::prelude::*;
mod sir;

/// Formats the sum of two numbers as string.
#[pyfunction]
#[pyo3(name = "sir")]
fn sir_rs(runtime: f64, dt: f64, S:f64, I:f64, R:f64, Beta:Vec<f64>, Gamma:Vec<f64>, Alpha:Vec<f64>) -> PyResult<(Vec<f64>, Vec<f64>, Vec<f64>)> {
    // !println(&Beta[0], &Gamma[0])
    let initial_state = sir::SIR::new(S, I, R);
    let params = sir::Parameters{Beta, Gamma, Alpha};
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