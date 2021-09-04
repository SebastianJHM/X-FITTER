import scipy.special as sc
import math
import scipy.stats
import numpy as np
from scipy.optimize import least_squares

class RICE:
    """
    Rice distribution
    https://en.wikipedia.org/wiki/Rice_distribution     
    """
    def __init__(self, measurements):
        self.parameters = self.get_parameters(measurements)
        self.v = self.parameters["v"]
        self.sigma = self.parameters["sigma"]

    def cdf(self, x):
        """
        Cumulative distribution function
        Calculated with quadrature integration method of scipy
        """
        def Q(M, a, b):
            """
            Marcum Q-function
            https://en.wikipedia.org/wiki/Marcum_Q-function
            """
            k = 1 - M
            x = (a/b)**k * sc.iv(k, a*b)
            suma = 0
            while(x > 1e-20):
                suma += x
                k += 1
                x = (a/b)**k * sc.iv(k, a*b)
            resultado  = suma * math.exp(-(a**2+b**2)/2)
            return resultado

        result = scipy.stats.rice.cdf(x, self.v/self.sigma, scale = self.sigma)
        # result, error = scipy.integrate.quad(self.pdf, 0, x)
        result = 1 - Q(1, self.v/self.sigma, x/self.sigma)
        return result
    
    def pdf(self, x):
        """
        Probability density function
        """
        # result = scipy.stats.rice.pdf(x, self.v/self.sigma, scale = self.sigma)
        result = (x/(self.sigma**2)) * math.exp(-(x**2+self.v**2)/(2*self.sigma**2)) * sc.i0(x * self.v / (self.sigma**2))
        return result

    def get_num_parameters(self):
        """
        Number of parameters of the distribution
        """
        return len(self.parameters.keys())
    
    def parameter_restrictions(self):
        """
        Check parameters restrictions
        """
        v1 = self.v >= 0
        v2 = self.sigma >= 0
        return v1 and v2
    
    def get_parameters(self, measurements):
        """
        Calculate proper parameters of the distribution from sample measurements.
        The parameters are calculated by solving the equations of the measures expected 
        for this distribution.The number of equations to consider is equal to the number 
        of parameters.
        
        Parameters
        ----------
        measurements : dict
            {"mean": *, "variance": *, "skewness": *, "kurtosis": *, "data": *}

        Returns
        -------
        parameters : dict
            {"alpha": *, "beta": *, "min": *, "max": *}
        """
        def equations(sol_i, measurements):
            v, sigma = sol_i
            
            E = lambda k: sigma**k * 2**(k/2) * math.gamma(1+k/2) * sc.eval_laguerre(k/2,-v*v/(2*sigma*sigma))

            ## Parametric expected expressions
            parametric_mean = E(1)
            parametric_variance = (E(2) - E(1)**2)
            # parametric_skewness = (E(3) - 3*E(2)*E(1) + 2*E(1)**3) / ((E(2)-E(1)**2))**1.5
            # parametric_kurtosis = (E(4) - 4 * E(1) * E(3) + 6 * E(1)**2 * E(2) - 3 * E(1)**4)/ ((E(2)-E(1)**2))**2
            
            ## System Equations
            eq1 = parametric_mean - measurements.mean
            eq2 = parametric_variance - measurements.variance
            # eq3 = parametric_skewness - measurements.skewness
            # eq4 = parametric_kurtosis  - measurements.kurtosis
            
            
            return (eq1, eq2)
        
        bnds = ((0, 0), (np.inf, np.inf))
        x0 = (measurements.mean, math.sqrt(measurements.variance))
        args = ([measurements])
        solution = least_squares(equations, x0, bounds = bnds, args=args)
        parameters = {"v": solution.x[0], "sigma": solution.x[1]}
        
        
        return parameters


if __name__ == "__main__":   
    ## Import function to get measurements
    from measurements.measurements import MEASUREMENTS
    
    ## Import function to get measurements
    def get_data(direction):
        file  = open(direction,'r')
        data = [float(x.replace(",",".")) for x in file.read().splitlines()]
        return data
    
    ## Distribution class
    path = "..\\data\\data_rice.txt"
    data = get_data(path) 
    measurements = MEASUREMENTS(data)
    distribution = RICE(measurements)
    
    print(distribution.get_parameters(measurements))
    print(distribution.cdf(measurements.mean))
    print(distribution.pdf(measurements.mean))