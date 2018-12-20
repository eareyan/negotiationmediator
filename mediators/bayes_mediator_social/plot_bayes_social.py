import matplotlib.pyplot as plt
import numpy as np
from skopt.acquisition import gaussian_ei
from skopt.plots import plot_convergence


class PlotBayesSocial:

    @staticmethod
    def plot_bayes_social(f, res, num_plots, lower_bound, upper_bound):
        print("Plot Bayes")
        plot_convergence(res)
        plt.show()
        initial_num_true_func_samples = 4000
        x = np.linspace(lower_bound, upper_bound, initial_num_true_func_samples).reshape(-1, 1)
        x_gp = res.space.transform(x.tolist())
        for n_iter in range(num_plots):
            # Print some dubg info.
            gp = res.models[n_iter]
            curr_x_iters = res.x_iters[:num_plots + n_iter]
            curr_func_vals = res.func_vals[:num_plots + n_iter]
            #print('Iteration', n_iter, ', curr_x_iters = ', curr_x_iters, ', curr_func_vals = ', curr_func_vals)

            # Plot true function.
            plt.subplot(num_plots, 2, 2 * n_iter + 1)
            # fx = np.array([f(x_i) for x_i in range(int(lower_bound), int(upper_bound) + 1)])
            true_x = np.linspace(lower_bound, upper_bound, num=100)
            plt.step(true_x, [f((i,)) for i in true_x], "r--", label="True (unknown)", where='post')

            # Plot GP(x) + contours
            y_pred, sigma = gp.predict(x_gp, return_std=True)
            plt.plot(x, y_pred, "g--", label=r"$\mu_{GP}(x)$")
            plt.fill(np.concatenate([x, x[::-1]]), np.concatenate([y_pred - 1.9600 * sigma, (y_pred + 1.9600 * sigma)[::-1]]), alpha=.2, fc="g", ec="None")

            # Plot sampled points
            plt.plot(curr_x_iters, curr_func_vals, "r.", markersize=8, label="Observations")

            # Adjust plot layout
            plt.grid()

            if n_iter == 0:
                plt.legend(loc="best", prop={'size': 6}, numpoints=1)

            if n_iter != num_plots - 1:
                plt.tick_params(axis='x', which='both', bottom='off', top='off', labelbottom='off')

            # Plot EI(x)
            plt.subplot(num_plots, 2, 2 * n_iter + 2)
            acq = gaussian_ei(x_gp, gp, y_opt=np.min(curr_func_vals))
            plt.plot(x, acq, "b", label="EI(x)")
            plt.fill_between(x.ravel(), -2.0, acq.ravel(), alpha=0.3, color='blue')

            next_x = res.x_iters[num_plots + n_iter]
            next_acq = gaussian_ei(res.space.transform([next_x]), gp, y_opt=np.min(curr_func_vals))
            plt.plot(next_x, next_acq, "bo", markersize=6, label="Next query point")

            # Adjust plot layout
            plt.ylim(lower_bound, upper_bound)
            plt.grid()

            if n_iter == 0:
                plt.legend(loc="best", prop={'size': 6}, numpoints=1)

            if n_iter != num_plots - 1:
                plt.tick_params(axis='x', which='both', bottom='off', top='off', labelbottom='off')

        plt.show()
