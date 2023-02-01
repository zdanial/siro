

pub struct Parameters {
    pub Beta: Vec<f32>,
    pub Gamma: Vec<f32>,
    pub Alpha: Vec<f32>,
}

pub struct SIR {
    pub S: f32,
    pub I: f32,
    pub R: f32,
}

pub struct Results {
    pub S: Vec<f32>,
    pub I: Vec<f32>,
    pub R: Vec<f32>,
}

impl Results {
    fn new() -> Self {
        return Results {
            S: Vec::new(),
            I: Vec::new(),
            R: Vec::new()
        }
    }
}

fn Sdot(state: &SIR, params: &Parameters , i: &usize) -> f32 {
    - params.Beta[*i] * (( (state.S * state.I) / (state.S + state.I + state.R) ) as f32) +
    params.Alpha[*i] * (state.R as f32)
}

fn Idot(state: &SIR, params: &Parameters , i: &usize) -> f32 {
    params.Beta[*i] * (( (state.S * state.I) / (state.S + state.I + state.R) ) as f32) -
    params.Gamma[*i] * ( state.I as f32)
}

fn Rdot(state: &SIR, params: &Parameters , i: &usize) -> f32 {
    params.Gamma[*i] * ( state.I as f32) - params.Alpha[*i] * (state.R as f32)
}

fn step(state: &SIR, params: &Parameters, i: &usize, dt: &f32) -> SIR {
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


pub fn run(runtime: f32, dt: f32, initial_state: SIR, params: Parameters) -> Results {
    let mut i = 0 as usize;
    let mut t = 0 as f32;
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

