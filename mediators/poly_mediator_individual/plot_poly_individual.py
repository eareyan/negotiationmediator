import numpy as np
import matplotlib.pyplot as plt


class PlotPolyIndividual:

    @staticmethod
    def plot_poly_individual(list_of_surrogates, f_true, f_model, lower_bound, upper_bound, omega_star, f_omega_star):
        """
        Plotting the agent's surrogates vs. ground truth utility and the welfare function. Only works for 1D.
        """
        num_agents = len(list_of_surrogates)
        plot_grid = np.linspace(lower_bound, upper_bound, num=100)
        fig, axs = plt.subplots(1, num_agents + 1, figsize=(12, 8))
        for i, a in enumerate(list_of_surrogates):
            regr = a.get_current_surrogate()
            # One can either plot the points queried so far...
            # axs[i].step(a.get_X(), a.get_y(), where='post')
            # axs[i].plot(a.get_X(), [np.polyval(np.flip(regr.coef_), x) + regr.intercept_ for x in a.get_X()])

            # Or plot the true models, both utilities and poly regresor
            axs[i].step(plot_grid, [a.evaluate_u((x,)) for x in plot_grid], where='post')
            axs[i].plot(plot_grid, [a.query(np.array(x).reshape(-1, 1)) for x in plot_grid])
            axs[i].scatter(a.get_X(), a.get_y(), color='r')
            axs[i].plot(omega_star, a.evaluate_u((omega_star,)), 'ro', color='b')
            axs[i].set_ylim(bottom=0.0)
        # Plot welfare as last graph
        axs[num_agents].step(plot_grid, [f_true((x,)) for x in plot_grid], where='post')
        axs[num_agents].plot(plot_grid, [-1.0 * f_model(x) for x in plot_grid])
        axs[num_agents].plot(omega_star, -1.0 * f_omega_star, 'ro')
        axs[num_agents].set_ylim(bottom=0.0)
        plt.show()
