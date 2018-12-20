from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from mediators.base_surrogate import BaseSurrogate


class PolySurrogate(BaseSurrogate):
    """
    Implements a Poly Surrogate.
    """
    degree = None

    def __init__(self, num_issues, X, u, degree=2):
        BaseSurrogate.__init__(self, num_issues, X, u)
        self.degree = degree
        self.poly_features = PolynomialFeatures(degree=self.degree)

    def update_surrogate(self):
        the_regressor = LinearRegression()
        T = self.poly_features.fit_transform(self.X)
        self.current_surrogate = the_regressor.fit(T, self.y)

    def query(self, x):
        # TODO: This evaluation is very expensive. How to optimize it? Maybe evaluate the polynomials directly?
        return self.current_surrogate.predict(self.poly_features.fit_transform(x))
