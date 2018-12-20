import numpy as np
import matplotlib.pyplot as plt


class PlotPolySocial:
    @staticmethod
    def plot_poly_social(list_of_surrogates, f_true, f_model, lower_bound, upper_bound, omega_star, f_omega_star):
        plot_grid = np.linspace(lower_bound, upper_bound, num=100)
        plt.step(plot_grid, [f_true((x,)) for x in plot_grid], where='post')
        plt.plot(plot_grid, [list_of_surrogates[0].query(np.array(x).reshape(1, -1)) for x in plot_grid])
        plt.scatter(list_of_surrogates[0].get_X(), list_of_surrogates[0].get_y(), color='r')
        plt.plot(omega_star, list_of_surrogates[0].query(np.array(omega_star).reshape(1, -1)), 'ro', color='b')
        plt.xlabel("True Welfare and welfare model")
        plt.show()
