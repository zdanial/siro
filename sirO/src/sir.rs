use pyo3::prelude::*;

pub struct Parameters {
    pub Beta: Vec<f64>,
    pub Gamma: Vec<f64>,
    pub Alpha: Vec<f64>,
}

pub struct SIR {
    pub S: f64,
    pub I: f64,
    pub R: f64,
}

#[pyclass]
pub struct Results {
    pub S: Vec<f64>,
    pub I: Vec<f64>,
    pub R: Vec<f64>,
}

impl Parameters {
    pub fn new(Alpha: Vec<f64>, Beta:Vec<f64>, Gamma:Vec<f64>) -> Self {
        return Parameters {
            Alpha, Beta, Gamma
        }
    }
}

#[pymethods]
impl Results {
    #[new]
    pub fn new() -> Self {
        return Results {
            S: Vec::new(),
            I: Vec::new(),
            R: Vec::new()
        }
    }
}

impl SIR {
    pub fn new(S: f64, I: f64, R: f64) -> Self {
        return SIR {
            S,
            I,
            R
        }
    }
}

fn Sdot(state: &SIR, params: &Parameters , i: &usize) -> f64 {
    (- params.Beta[*i] * ( (state.S * state.I) / (state.S + state.I + state.R) ) + params.Alpha[*i] * state.R)
}

fn Idot(state: &SIR, params: &Parameters , i: &usize) -> f64 {
    (params.Beta[*i] * ( (state.S * state.I) / (state.S + state.I + state.R) ) - params.Gamma[*i] * ( state.I))
}

fn Rdot(state: &SIR, params: &Parameters , i: &usize) -> f64 {
    (params.Gamma[*i] * state.I - params.Alpha[*i] * state.R)
}

fn step(state: &SIR, params: &Parameters, i: &usize, dt: &f64) -> SIR {
    let S = state.S + Sdot(state, params, i) * dt;
    let I = state.I + Idot(state, params, i) * dt;
    let R = state.R + Rdot(state, params, i) * dt;
    return SIR {S, I, R}

}

fn capture_state(state: &SIR, results: &mut Results) {
    results.S.push(state.S);
    results.I.push(state.I);
    results.R.push(state.R);
}


pub fn run(runtime: f64, dt: f64, initial_state: SIR, params: Parameters) -> Results {
    let mut i = 0 as usize;
    let mut t = 0 as f64;
    let mut state = initial_state;
    let mut res = Results::new();
    while t < runtime - dt {
        state = step(&state, &params, &i, &dt);
        capture_state(&state, &mut res);
        i += 1;
        t += dt;
    }
    res
}

