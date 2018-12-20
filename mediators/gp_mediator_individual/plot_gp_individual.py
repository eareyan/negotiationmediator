import numpy as np
import matplotlib.pyplot as plt


class PlotGPIndividual:

    @staticmethod
    def plot_gp_social(list_of_surrogates, f_true, f_model, lower_bound, upper_bound, omega_star, f_omega_star):
        num_agents = len(list_of_surrogates)
        plot_grid = np.linspace(lower_bound, upper_bound, num=100)
        fig, axs = plt.subplots(1, num_agents + 1, figsize=(12, 8))
        x = np.atleast_2d(np.linspace(lower_bound, upper_bound, 1000)).T
        for i, a in enumerate(list_of_surrogates):
            i_surrogate = list_of_surrogates[i]
            X = i_surrogate.get_X()

            # Plot the actual utility function of each agent
            y = [i_surrogate.evaluate_u(x) for x in x]
            axs[i].plot(X, [i_surrogate.evaluate_u(x) for x in X], 'r.', markersize=10, label=u'Observations')
            axs[i].plot(x, y, 'r:', label=u'$f(x) = W$')

            # Plot the GP prediction for each agent. Make the prediction on the meshed x-axis (ask for MSE as well)
            y_pred, sigma = i_surrogate.getGP().predict(x, return_std=True)
            axs[i].plot(x, y_pred, 'b-', label=u'Prediction')
            axs[i].fill(np.concatenate([x, x[::-1]]), np.concatenate([y_pred - 1.9600 * sigma, (y_pred + 1.9600 * sigma)[::-1]]),
                        alpha=.5, fc='b', ec='None', label='95% confidence interval')

            # Plot the next query point
            axs[i].scatter(omega_star, i_surrogate.evaluate_u(omega_star), c='black', s=100)

        # Plot welfare as last graph
        axs[num_agents].step(plot_grid, [f_true((x,)) for x in plot_grid], where='post')
        axs[num_agents].plot(plot_grid, [-1.0 * f_model(x) for x in plot_grid])
        axs[num_agents].plot(omega_star, -1.0 * f_omega_star, 'ro')
        axs[num_agents].set_ylim(bottom=0.0)
        plt.show()
