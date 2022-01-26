import scipy.stats
import math
from scipy.optimize import fsolve

class FATIGUE_LIFE:
    """
    Fatigue life distribution
    """
    def __init__(self, measurements):
        self.parameters = self.get_parameters(measurements)
        
        self.gamma = self.parameters["gamma"]
        self.loc = self.parameters["loc"]
        self.scale = self.parameters["scale"]
        
    def cdf(self, x):
        """
        Cumulative distribution function
        Calculated using the definition of the function
        Alternative: quadrature integration method
        """
        return scipy.stats.fatiguelife.cdf(x, self.gamma, loc=self.loc, scale=self.scale)
    
    def pdf(self, x):
        """
        Probability density function
        Calculated using definition of the function in the documentation
        """
        return scipy.stats.fatiguelife.pdf(x, self.gamma, loc=self.loc, scale=self.scale)
    
    def get_num_parameters(self):
        """
        Number of parameters of the distribution
        """
        return len(self.parameters.keys())
    
    def parameter_restrictions(self):
        """
        Check parameters restrictions
        """
        v1 = self.scale > 0
        v2 = self.gamma > 0
        return v1 and v2
        
    def get_parameters(self, measurements):
        """
        Calculate proper parameters of the distribution from sample measurements.
        The parameters are calculated by formula.
        
        Parameters
        ----------
        measurements : dict
            {"mean": *, "variance": *, "skewness": *, "kurtosis": *, "median": *, "mode": *}

        Returns
        -------
        parameters : dict
            {"gamma": *, "loc": *, "scale": *}
        """
        ## NO SE ESTÁN RESOLVIENDO LAS ECUACIONES PARA GAMMA = 5, scale = 10, loc = 5
        # def equations(sol_i, measurements):
        #     ## Variables declaration
        #     loc, scale, gamma = sol_i
            
        #     ## Parametric expected expressions
        #     parametric_mean = loc + scale * (1 + gamma**2/2)
        #     parametric_variance = scale**2 * gamma**2 * (1 + 5 * gamma**2/4)
        #     parametric_skewness = 4 * gamma**2 * (11*gamma**2 + 6) / ((4+5*gamma**2)*math.sqrt(gamma**2 * (4+5*gamma**2)))
        
        #     ## System Equations
        #     eq1 = parametric_mean - measurements.mean
        #     eq2 = parametric_variance - measurements.variance
        #     eq3 = parametric_skewness - measurements.skewness
            
        #     return (eq1, eq2, eq3)
        
        # solution =  fsolve(equations, (1, 1, 1), measurements)
        # print(solution)
        scipy_params = scipy.stats.fatiguelife.fit(measurements.data)
        parameters = {"gamma": scipy_params[0], "loc": scipy_params[1], "scale": scipy_params[2]}
        return parameters
    
if __name__ == '__main__':
    ## Import function to get measurements
    from measurements.measurements import MEASUREMENTS

    ## Import function to get measurements
    def get_data(direction):
        file  = open(direction,'r')
        data = [float(x.replace(",",".")) for x in file.read().splitlines()]
        return data
    
    ## Distribution class
    path = "../data/data_fatigue_life.txt"
    data = get_data(path) 
    measurements = MEASUREMENTS(data)
    distribution = FATIGUE_LIFE(measurements)
    
    print(distribution.get_parameters(measurements))
    print(distribution.cdf(measurements.mean))
    print(distribution.pdf(measurements.mean))
    
    print(scipy.stats.fatiguelife.pdf(20, 0.5, loc=15, scale=10))
    print(scipy.stats.fatiguelife.ppf(0.55, 0.5, loc=15, scale=10))