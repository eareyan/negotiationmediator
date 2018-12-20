from mediators.base_mediator import BaseMediator
import itertools


class OptimalMediator(BaseMediator):

    def __init__(self, num_issues, num_agents, u_funcs, lower_bounds, upper_bounds, num_init_random_points, num_random_restarts, plot_mediator=False, verbose=False):
        BaseMediator.__init__(self, num_issues, num_agents, u_funcs, lower_bounds, upper_bounds, num_init_random_points, num_random_restarts, plot_mediator, None, verbose)

    def mediate(self, num_rounds):
        num_issues = self.num_issues
        L = self.lower_bounds
        U = self.upper_bounds
        max_contract = None
        welfare_max = 0
        for x in itertools.product(*[[i for i in range(int(L[j]), int(U[j]) + 1)] for j in range(0, num_issues)]):
            welfare_at_x = self.get_true_welfare(x)
            if welfare_at_x > welfare_max:
                max_contract = x
                welfare_max = welfare_at_x
        return [float(d) for d in max_contract], welfare_max
