mod sir;

fn main() {
    let initial_state = sir::SIR{S: 1000.0, I: 1.0, R: 0.0};
    let runtime = 100.0;
    let dt = 0.1;
    let params = sir::Parameters{
        Beta: vec![1.0; (runtime/dt) as usize],
        Gamma: vec![1.0/14.0; (runtime/dt) as usize],
        Alpha: vec![0.005; (runtime/dt) as usize]
    };
    let out = sir::run(runtime, dt, initial_state, params);
    println!("{:?}", out.R);
}
