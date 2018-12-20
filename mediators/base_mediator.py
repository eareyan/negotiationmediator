"""
Base Mediator class for the case of hyper-rectangle valuations.
"""
from scipy.optimize import minimize
import numpy as np
import warnings
import math


class BaseMediator:
    num_issues = None
    num_agents = None
    u_funcs = None
    lower_bounds = None
    upper_bounds = None
    num_init_random_points = None
    num_random_restarts = None
    plot_mediator = None
    plotter = None
    verbose = None
    bounds = None
    list_of_surrogates = None

    def __init__(self, num_issues, num_agents, u_funcs, lower_bounds, upper_bounds, num_init_random_points, num_random_restarts, plot_mediator, plotter, verbose):
        self.num_issues = num_issues
        self.num_agents = num_agents
        self.u_funcs = u_funcs
        self.lower_bounds = lower_bounds
        self.upper_bounds = upper_bounds
        self.num_init_random_points = num_init_random_points
        self.num_random_restarts = num_random_restarts
        self.plot_mediator = plot_mediator
        self.plotter = plotter
        self.verbose = verbose
        self.bounds = [(l, u) for l, u in zip(self.lower_bounds, self.upper_bounds)]

    def get_true_welfare(self, x):
        """
        Implements the true welfare function.
        """
        return sum(self.u_funcs[a](x) for a in range(0, self.num_agents))

    def optimize_welfare(self):
        """
        This function optimizes the welfare function as the mediator currently understands it, i.e., the model of the welfare.
        """
        best_welfare_value = math.inf
        best_welfare_point = None
        # We try some number of different random starting points.
        for i in range(0, self.num_random_restarts):
            x0 = np.concatenate([np.random.uniform(l, u, 1) for l, u in zip(self.lower_bounds, self.upper_bounds)])
            r = minimize(fun=self.get_model_welfare, x0=x0, method='L-BFGS-B', bounds=tuple((x, y) for x, y in zip(self.lower_bounds, self.upper_bounds)))
            if self.get_model_welfare(r['x']) < best_welfare_value:
                best_welfare_value = self.get_model_welfare(r['x'])
                best_welfare_point = r['x']
        return best_welfare_point, best_welfare_value

    def mediate(self, num_rounds):
        """
        Implements the mediation for a given number of rounds.
        """
        # TODO. Here I am ignoring warnings so that I can run experiments better. But, should be careful with this, some warnings might be important.
        warnings.simplefilter("ignore")
        res = [0.0]
        maximizer = None
        maximum = -1.0  # Is enough to start with any negative number under the assumption that welfare is at least 0
        # The next two lines define stuff for making nice printing in the command line, which is seen in case self.verbose = True
        print_formatting = "{:5}{:" + str(14 * self.num_issues) + "}{:" + str(25) + "}{:" + str(25) + "}"
        if self.verbose:
            print(print_formatting.format("t", "omega^*", "w^hat(omega^*)", "w(omega^*)"))
        for t in range(0, num_rounds):
            for a in self.list_of_surrogates:
                a.update_surrogate()
            # Optimize the welfare model and obtain \omega^* and the value of the model at \omega^*
            omega_star, model_welfare_omega_star = self.optimize_welfare()
            true_welfare_omega_star = self.get_true_welfare(omega_star)
            res += [max(self.get_true_welfare(omega_star), max(res))]
            # Record the welfare in case this was the best seen so far
            if true_welfare_omega_star > maximum:
                maximum = true_welfare_omega_star
                maximizer = omega_star
            # A different strategy is to just get a random number for \omega^*
            # omega_star = np.random.random_sample() * self.upper_bound
            for a in self.list_of_surrogates:
                a.add_observation((omega_star,))
            # Output information and/or plot.
            if self.verbose:
                print(print_formatting.format(str(t), str(omega_star), str(model_welfare_omega_star[0]), str(true_welfare_omega_star)))
            if self.plot_mediator and t % 1 == 0:
                self.plotter(self.list_of_surrogates, self.get_true_welfare, self.get_model_welfare,
                             self.lower_bounds[0], self.upper_bounds[0], omega_star, model_welfare_omega_star)
        if self.verbose:
            print("Welfare maximizing contract: ", maximizer, ", value of welfare max maximizing: ", maximum)
            print("Maxima = ", res[1:])
        return [v for v in maximizer], maximum
