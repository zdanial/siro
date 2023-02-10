import sirO

runtime = 100.0
dt = 0.1
out = sirO.sir(runtime, dt, 1000.0, 1.0, 0.0, 
    [1.0 for i in range(int(runtime//dt)+1)], 
    [1/14 for i in range(int(runtime//dt)+1)],
    [0.005 for i in range(int(runtime//dt)+1)] )
print(out[0][::100], out[1][::100], out[2][::100])