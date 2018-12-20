from mediators.base_surrogate import BaseSurrogate
from skopt.learning.gaussian_process.kernels import ConstantKernel
from skopt.learning.gaussian_process.kernels import Matern
from skopt.learning.gaussian_process import GaussianProcessRegressor
import numpy as np


class GPSurrogate(BaseSurrogate):
    gp = None

    def __init__(self, num_issues, X, y):
        BaseSurrogate.__init__(self, num_issues, X, y)
        # Instantiate a Gaussian Process model.
        # TODO. A question we need to investigate is what kernel we should be using?
        # TODO. For now, to have a valid comparison, I am using the same kernel used by the bayesian optimization.
        # TODO. Note that I am using the Kernels as given by the skopt library, with the same parameters.
        cov_amplitude = ConstantKernel(1.0, (0.01, 1000.0))
        other_kernel = Matern(length_scale=np.ones(num_issues), length_scale_bounds=[(0.01, 100)] * num_issues, nu=2.5)
        self.gp = GaussianProcessRegressor(kernel=cov_amplitude * other_kernel,
                                           normalize_y=True,
                                           n_restarts_optimizer=2,
                                           noise=0.000000001,
                                           random_state=np.random.mtrand._rand.randint(0, np.iinfo(np.int32).max))
        # Another option for gaussian process is using The default kernel here, i.e., RBF.
        # self.gp = GaussianProcessRegressor(kernel=None, n_restarts_optimizer=9)

    def update_surrogate(self):
        self.gp.fit(self.X, self.y)

    def query(self, x):
        x = np.array(x).reshape(1, -1)
        return self.gp.predict(np.atleast_2d(x))

    def getGP(self):
        return self.gp
