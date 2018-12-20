"""
Polynomial, individual model mediator.
"""
from mediators.base_mediator import BaseMediator
from mediators.surrogates.poly_surrogate import PolySurrogate
from mediators.poly_mediator_individual.plot_poly_individual import PlotPolyIndividual
import numpy as np


class PolyMediatorIndividual(BaseMediator):
    degree = None

    def __init__(self, num_issues, num_agents, u_funcs, lower_bounds, upper_bounds, degree, num_init_random_points, num_random_restarts, plot_mediator=False, verbose=False):
        BaseMediator.__init__(self, num_issues, num_agents, u_funcs, lower_bounds, upper_bounds, num_init_random_points, num_random_restarts,
                              plot_mediator, PlotPolyIndividual.plot_poly_individual, verbose)
        self.degree = degree
        # For each agent, build an initial poly model with a random number of points.
        # Create an array of num_init_random_points many initial random points where each coordinate may potentially have different lower and upper bounds.
        initial_random_points = np.array([point for point in zip(*[np.random.uniform(l, u, num_init_random_points) for l, u in zip(self.lower_bounds, self.upper_bounds)])])
        self.list_of_surrogates = []
        for a in range(0, num_agents):
            self.list_of_surrogates.append(PolySurrogate(self.num_issues, initial_random_points, self.u_funcs[a], self.degree))

    def get_model_welfare(self, x):
        # TODO: the next two lines work for any dimensions but is slow. The third line is fast but works only for 1D.
        x = np.array(x).reshape(1, -1)
        return -1.0 * sum(a.query(x) for a in self.list_of_surrogates)
        # TODO: could be optimize to compute the sum of the coefficients just once.
        # return -1.0 * (np.polyval(sum(np.flip(surrogate.get_current_surrogate().coef_) for surrogate in self.list_of_surrogates), x) + \
        #               sum(surrogate.get_current_surrogate().intercept_ for surrogate in self.list_of_surrogates))
