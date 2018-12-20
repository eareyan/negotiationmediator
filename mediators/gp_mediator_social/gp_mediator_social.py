"""
Gaussian process mediator, welfare. Corresponds to distribution, social model.
"""
from mediators.base_mediator import BaseMediator
from mediators.surrogates.gp_surrogate import GPSurrogate
from mediators.gp_mediator_social.plot_gp_social import PlotGPSocial
import numpy as np


class GPMediatorSocial(BaseMediator):

    def __init__(self, num_issues, num_agents, u_funcs, lower_bounds, upper_bounds, num_init_random_points, num_random_restarts, plot_mediator=False, verbose=False):
        BaseMediator.__init__(self, num_issues, num_agents, u_funcs, lower_bounds, upper_bounds, num_init_random_points, num_random_restarts,
                              plot_mediator, PlotGPSocial.plot_gp_social, verbose)
        self.initial_random_points = np.array([point for point in zip(*[np.random.uniform(l, u, num_init_random_points) for l, u in zip(self.lower_bounds, self.upper_bounds)])])
        self.list_of_surrogates = [GPSurrogate(num_issues, self.initial_random_points, self.get_true_welfare)]

    def get_model_welfare(self, x):
        return -1.0 * self.list_of_surrogates[0].query(x)
