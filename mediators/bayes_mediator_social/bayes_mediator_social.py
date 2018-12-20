"""
Bayes Mediator.
"""
from skopt import gp_minimize
from mediators.bayes_mediator_social.plot_bayes_social import PlotBayesSocial
from mediators.base_mediator import BaseMediator
import numpy as np


class BayesMediatorSocial(BaseMediator):
    base_estimator = None

    def __init__(self, num_issues, num_agents, u_funcs, lower_bounds, upper_bounds, num_init_random_points, num_random_restarts,
                 base_estimator=None, plot_mediator=False, verbose=False):
        BaseMediator.__init__(self, num_issues, num_agents, u_funcs, lower_bounds, upper_bounds, num_init_random_points, num_random_restarts, plot_mediator, None, verbose)
        self.base_estimator = base_estimator

    def get_true_welfare(self, x):
        return -1.0 * BaseMediator.get_true_welfare(self, x)

    def mediate(self, num_rounds):
        """
        Implements the mediator
        """
        # Perform Bayesian optimization
        # print(self.base_estimator)
        res = gp_minimize(func=self.get_true_welfare,  # the function to minimize
                          dimensions=self.bounds,  # the bounds on each dimension of x
                          acq_func="EI",  # the acquisition function
                          n_calls=num_rounds + self.num_init_random_points,  # the number of evaluations of f TODO: I think includes random initial points.
                          n_random_starts=self.num_init_random_points,  # the number of random initialization points
                          n_restarts_optimizer=self.num_random_restarts,  # The number of restarts of the optimizer when acq_optimizer is "lbfgs".
                          noise=0.000000001,  # A very small noise number is equivalent to no noise, according to the documentation.
                          # random_state=123, # We are going to allow the mediator to randomize
                          verbose=self.verbose,
                          base_estimator=self.base_estimator)
        if self.verbose:
            print("Welfare maximizing contract: ", res['x'], ", value of welfare max maximizing: ", res['fun'])
            print("Minimums = ", [np.min(res.func_vals[:i]) for i in range(1, num_rounds + 1)])
        if self.plot_mediator:
            PlotBayesSocial.plot_bayes_social(f=self.get_true_welfare, res=res, num_plots=min(num_rounds - self.num_init_random_points, 5),
                                              lower_bound=self.bounds[0][0],
                                              upper_bound=self.bounds[0][1])
        return res['x'], -1.0 * res['fun']
