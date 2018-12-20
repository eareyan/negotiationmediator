"""
GP mediator individual. Corresponds to individual, distribution.
"""
from mediators.base_mediator import BaseMediator
from mediators.surrogates.gp_surrogate import GPSurrogate
from mediators.gp_mediator_individual.plot_gp_individual import PlotGPIndividual
import numpy as np


class GPMediatorIndividual(BaseMediator):

    def __init__(self, num_issues, num_agents, u_funcs, lower_bounds, upper_bounds, num_init_random_points, num_random_restarts, plot_mediator=False, verbose=False):
        BaseMediator.__init__(self, num_issues, num_agents, u_funcs, lower_bounds, upper_bounds, num_init_random_points, num_random_restarts,
                              plot_mediator, PlotGPIndividual.plot_gp_social, verbose)
        # For each agent, build an initial poly model with a random number of points.
        # Create an array of num_init_random_points many initial random points where each coordinate may potentially have different lower and upper bounds.
        initial_random_points = np.array([point for point in zip(*[np.random.uniform(l, u, num_init_random_points) for l, u in zip(self.lower_bounds, self.upper_bounds)])])
        self.list_of_surrogates = []
        for a in range(0, num_agents):
            self.list_of_surrogates.append(GPSurrogate(self.num_issues, initial_random_points, self.u_funcs[a]))

    def get_model_welfare(self, x):
        x = np.array(x).reshape(1, -1)
        return -1.0 * sum(a.query(x) for a in self.list_of_surrogates)
