import numpy as np
import pandas as pd


def get_lambda(contact_matrix, pop):
    M_diag_p = np.matmul( contact_matrix, (np.diag(pop)/pop.sum()).astype(float) )
    lambda_ = np.linalg.eig(M_diag_p)[0].max() # dominant eigenvalue
    return lambda_


class SIR_arr:
    def __init__(self, S0, I0, R0, Beta, Gamma, dt, group_labels=None):
        if not isinstance(S0, list):
            S0 = [S0]
        if not isinstance(I0, list):
            I0 = [I0]
        if not isinstance(R0, list):
            R0 = [R0]
        assert all([Sg >= 0 for Sg in S0]) and all([Rg >= 0 for Rg in R0]) and all([Ig >= 0 for Ig in I0]), 'Starting population must be greater than or equal to zero for all compartments.'
        
        if group_labels is not None:
            self.group_labels = group_labels
        else:
            self.group_labels = [str(i) for i in range(len(S0))]
            
        assert len(self.group_labels) == len(S0) and \
            len(self.group_labels) == len(I0) and \
            len(self.group_labels) == len(R0), 'Initial population values must align with (age) groups.'
        
        self.St = [S0]
        self.It = [I0]
        self.Rt = [R0]
        
        if not isinstance(Beta, list):
            self.Beta = [[Beta]*self.n_groups]*self.n_groups
        elif len(Beta) == len(Beta[0]) and len(Beta) == self.n_groups:
            self.Beta = Beta
        else:
            raise Exception("Beta must be a square matrix or constant.")
            
        if not isinstance(Gamma, list):
            self.Gamma = [Gamma]*self.n_groups
        elif len(Gamma) == self.n_groups:
            self.Gamma = Gamma
        else:
            raise Exception(f"Gamma must be a or constant or a list of size (n_groups == {self.n_groups}).")
        
        
        self.time = 0
        self.dt = dt
        self.N = sum(S0) + sum(I0) + sum(R0)
        
    @property
    def time_vector(self):
        return np.arange(0, self.time + self.dt, self.dt)[:len(self.S_timecourse())]
    
    @property
    def n_groups(self):
        return len(self.group_labels)
    
    def S_timecourse(self, group=None):
        if group is None:
            return [sum(S) for S in self.St]
        else:
            return [S[group] for S in self.St]
        
    def I_timecourse(self, group=None):
        if group is None:
            return [sum(I) for I in self.It]
        else:
            return [I[group] for I in self.It]
        
    def R_timecourse(self, group=None):
        if group is None:
            return [sum(R) for R in self.Rt]
        else:
            return [R[group] for R in self.Rt]

    def run(self, runtime):
        for _ in np.arange(self.time, self.time+runtime, self.dt):
            self.step()

    def step(self):
        S_new = [self.St[-1][i] + self.dt*self.Sdot(group=i) for i in range(self.n_groups)]
        I_new = [self.It[-1][i] + self.dt*self.Idot(group=i) for i in range(self.n_groups)]
        R_new = [self.Rt[-1][i] + self.dt*self.Rdot(group=i) for i in range(self.n_groups)]

        self.St.append(S_new)
        self.It.append(I_new)
        self.Rt.append(R_new)

        self.time += self.dt

    def Sdot(self, group=0):
        return - self.St[-1][group] * sum([self.Beta[group][j] * self.It[-1][j] for j in range(self.n_groups)]) / self.N

    def Idot(self, group=0):
        return self.St[-1][group] * sum([self.Beta[group][j] * self.It[-1][j] for j in range(self.n_groups)]) / self.N \
            - self.Gamma[group] * self.It[-1][group]

    def Rdot(self, group=0):
        return self.Gamma[group] * self.It[-1][group]