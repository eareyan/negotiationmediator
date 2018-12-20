import numpy as np
import matplotlib.pyplot as plt


class PlotGPSocial:

    @staticmethod
    def plot_gp_social(list_of_surrogates, f_true, f_model, lower_bound, upper_bound, omega_star, f_omega_star):
        welfare_surrogate_model = list_of_surrogates[0]
        gp = welfare_surrogate_model.getGP()
        X = welfare_surrogate_model.get_X()
        # Mesh the input space for evaluations of the real function, the prediction and its MSE
        x = np.atleast_2d(np.linspace(lower_bound, upper_bound, 1000)).T
        y = [f_true(x) for x in x]
        y_2 = [f_true(x) for x in X]
        # Make the prediction on the meshed x-axis (ask for MSE as well)
        y_pred, sigma = gp.predict(x, return_std=True)

        # Plot the GP model
        plt.plot(x, y, 'r:', label=u'$f(x) = W$')
        plt.plot(x, y_pred, 'b-', label=u'Prediction')
        plt.fill(np.concatenate([x, x[::-1]]), np.concatenate([y_pred - 1.9600 * sigma, (y_pred + 1.9600 * sigma)[::-1]]),
                 alpha=.5, fc='b', ec='None', label='95% confidence interval')
        # Plot the true welfare function.
        plt.plot(X, y_2, 'r.', markersize=10, label=u'Observations')
        plt.xlabel('$x$')
        plt.ylabel('$f(x)$')
        plt.scatter(omega_star, gp.predict(np.atleast_2d(omega_star)), c='black', s=100)
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=5)
        plt.tight_layout()
        plt.show()
