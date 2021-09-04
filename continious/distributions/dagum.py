import math
from scipy.optimize import least_squares
import numpy as np
import scipy.special


class DAGUM:
    """
    Dagum distribution
    https://en.wikipedia.org/wiki/Dagum_distribution
    """

    def __init__(self, measurements):
        self.parameters = self.get_parameters(measurements)
        self.a = self.parameters["a"]
        self.b = self.parameters["b"]
        self.p = self.parameters["p"]

    def cdf(self, x):
        """
        Cumulative distribution function.
        Calculated with quadrature integration method of scipy.
        """
        return (1 + (x/self.b) ** (-self.a)) ** (-self.p)

    def pdf(self, x):
        """
        Probability density function
        """
        return (self.a * self.p / x) * (((x/self.b) ** (self.a*self.p))/((((x/self.b) ** (self.a))+1)**(self.p+1)))

    def get_num_parameters(self):
        """
        Number of parameters of the distribution
        """
        return len(self.parameters.keys())

    def parameter_restrictions(self):
        """
        Check parameters restrictions
        """
        v1 = self.p > 0
        v2 = self.a > 0
        v3 = self.b > 0
        return v1 and v2 and v3

    def get_parameters(self, measurements):
        """
        Calculate proper parameters of the distribution from sample measurements.
        The parameters are calculated by formula.
        
        Parameters
        ----------
        measurements : dict
            {"mean": *, "variance": *, "skewness": *, "kurtosis": *, "data": *}

        Returns
        -------
        parameters : dict
            {"a": * , "b": *, "c": *}
        """
        frequencies, bin_edges = np.histogram(measurements.data, density=True)
        def sse(parameters):
            def __pdf(x, params): return (params["a"] * params["p"] / x) * (((x/params["b"]) ** (
                params["a"]*params["p"]))/((((x/params["b"]) ** (params["a"]))+1)**(params["p"]+1)))

            central_values = [(bin_edges[i] + bin_edges[i+1]) /
                              2 for i in range(len(bin_edges)-1)]

            ## Calculate fitted PDF and error with fit in distribution
            pdf_values = [__pdf(c, parameters) for c in central_values]

            ## Calculate SSE (sum of squared estimate of errors)
            sse = np.sum(np.power(frequencies - pdf_values, 2))

            return sse

        def equations(sol_i, measurements):
            ## Variables declaration
            a, b, p = sol_i

            ## Generatred moments function (not-centered)
            def miu(k): return (b**k) * p * \
                scipy.special.beta((a*p+k)/a, (a-k)/a)

            ## Parametric expected expressions
            parametric_mean = miu(1)
            parametric_variance = -(miu(1)**2) + miu(2)
            # parametric_skewness = (2*miu(1)**3 - 3*miu(1)*miu(2) + miu(3)) / (-(miu(1)**2) + miu(2))**1.5
            # parametric_kurtosis = (-3*miu(1)**4 + 6*miu(1)**2 * miu(2) -4 * miu(1) * miu(3) + miu(4)) / (-(miu(1)**2) + miu(2))**2
            parametric_median = b * ((2**(1/p))-1) ** (-1/a)
            # parametric_mode = b * ((a*p-1)/(a+1)) ** (1/a)

            ## System Equations
            eq1 = parametric_mean - measurements.mean
            eq2 = parametric_variance - measurements.variance
            eq3 = parametric_median - measurements.median

            return (eq1, eq2, eq3)

        ## Scipy Burr3 = Dagum parameter
        s0_burr3_sc = scipy.stats.burr.fit(measurements.data)
        parameters_sc = {"a": s0_burr3_sc[0],
                         "b": s0_burr3_sc[3], "p": s0_burr3_sc[1]}

        ##  Least Square Method
        a0 = s0_burr3_sc[0]
        b0 = s0_burr3_sc[3]
        x0 = [a0, b0, 1]
        b = ((1e-5, 1e-5, 1e-5), (np.inf, np.inf, np.inf))
        solution = least_squares(
            equations, x0, bounds=b, args=([measurements]))
        parameters_ls = {"a": solution.x[0],
                         "b": solution.x[1], "p": solution.x[2]}

        sse_sc = sse(parameters_sc)
        sse_ls = sse(parameters_ls)

        # print("*", sse_sc)
        # print("-", sse_ls)

        if a0 <= 2:
            return(parameters_sc)
        else:
            if sse_sc < sse_ls:
                return(parameters_sc)
            else:
                return(parameters_ls)


if __name__ == '__main__':
    ## Import function to get measurements
    from measurements.measurements import MEASUREMENTS

    ## Import function to get measurements
    def get_data(direction):
        file = open(direction, 'r')
        data = [float(x.replace(",", ".")) for x in file.read().splitlines()]
        return data

    ## Distribution class
    path = "..\\data\\data_dagum.txt"
    data = get_data(path)
    measurements = MEASUREMENTS(data)
    distribution = DAGUM(measurements)

    print(distribution.get_parameters(measurements))
    print(distribution.cdf(measurements.mean))

    print(scipy.stats.burr.fit(data))
