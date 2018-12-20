from scipy.optimize import minimize

r = minimize(fun=lambda x: x**3 - x**2, x0=1.0, method='L-BFGS-B', bounds=((0.0, 1.0),))

print(r)