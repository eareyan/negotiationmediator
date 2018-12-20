"""
Polynomial mediator for welfare. Corresponds to point estimate of social welfare.
"""
from mediators.base_mediator import BaseMediator
from mediators.surrogates.poly_surrogate import PolySurrogate
from mediators.poly_mediator_social.plot_poly_social import PlotPolySocial
import numpy as np


class PolyMediatorSocial(BaseMediator):
    degree = None

    def __init__(self, num_issues, num_agents, u_funcs, lower_bounds, upper_bounds, degree, num_init_random_points, num_random_restarts, plot_mediator=False, verbose=False):
        BaseMediator.__init__(self, num_issues, num_agents, u_funcs, lower_bounds, upper_bounds, num_init_random_points, num_random_restarts,
                              plot_mediator, PlotPolySocial.plot_poly_social, verbose)
        self.degree = degree
        initial_random_points = np.array([point for point in zip(*[np.random.uniform(l, u, num_init_random_points) for l, u in zip(self.lower_bounds, self.upper_bounds)])])
        self.list_of_surrogates = [PolySurrogate(self.num_issues, initial_random_points, self.get_true_welfare, self.degree)]

    def get_model_welfare(self, x):
        return -1.0 * self.list_of_surrogates[0].query(np.array(x).reshape(1, -1))
