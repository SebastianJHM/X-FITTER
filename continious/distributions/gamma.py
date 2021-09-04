import scipy.integrate
import math
import scipy.stats
import scipy.special as sc

class GAMMA:
    """
    Gamma distribution
    https://www.vosesoftware.com/riskwiki/Gammadistribution.php        
    """
    def __init__(self, measurements):
        self.parameters = self.get_parameters(measurements)
        self.alpha = self.parameters["alpha"]
        self.beta = self.parameters["beta"]
        
    def cdf(self, x):
        """
        Cumulative distribution function.
        Calculated with quadrature integration method of scipy.
        """
        ## Method 1: Integrate PDF function
        # result, error = scipy.integrate.quad(self.pdf, 0, x)
        # print(result)
        
        ## Method 2: Scipy Gamma Distribution class
        # result = scipy.stats.gamma.cdf(x, a=self.alpha, scale=self.beta)
        # print(result)
        
        lower_inc_gamma = lambda a, x: sc.gammainc(a, x) * math.gamma(a)
        result = lower_inc_gamma(self.alpha, x/self.beta)/math.gamma(self.alpha)
        return result
    
    def pdf(self, x):
        """
        Probability density function
        """
        return ((self.beta ** -self.alpha) * (x**(self.alpha-1)) * math.e ** (-(x / self.beta))) / math.gamma(self.alpha)
    
    def get_num_parameters(self):
        """
        Number of parameters of the distribution
        """
        return len(self.parameters.keys())
    
    def parameter_restrictions(self):
        """
        Check parameters restrictions
        """
        v1 = self.alpha > 0
        v2 = self.beta > 0
        return v1 and v2
    
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
            {"alpha": *, "beta": *}
        """
        mean = measurements.mean
        variance = measurements.variance
        
        alpha = mean ** 2 / variance
        beta = variance / mean
        parameters = {"alpha": alpha , "beta": beta}
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
    path = "..\\data\\data_gamma.txt"
    data = get_data(path) 
    measurements = MEASUREMENTS(data)
    distribution = GAMMA(measurements)
    
    print(distribution.get_parameters(measurements))
    print(distribution.cdf(measurements.mean))