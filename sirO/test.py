import sirO

runtime = 1000
dt = 0.1
print(sirO.sir(runtime, dt, 1000, 1, 0, 
    [1 for i in range(int(runtime//dt)+1)], 
    [1/14 for i in range(int(runtime//dt)+1)],
    [0.005 for i in range(int(runtime//dt)+1)] )[1])