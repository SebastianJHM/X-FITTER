import scipy.integrate
import math

class LOGNORMAL:
    """
    Lognormal distribution
    https://en.wikipedia.org/wiki/Log-normal_distribution          
    """
    def __init__(self, measurements):
        self.parameters = self.get_parameters(measurements)
        self.mean = self.parameters["mean"]
        self.desv = self.parameters["desv"]
        
    def cdf(self, x):
        """
        Cumulative distribution function.
        Calculated with quadrature integration method of scipy.
        """
        result, error = scipy.integrate.quad(self.pdf, 1e-15, x)
        return result
    
    def pdf(self, x):
        """
        Probability density function
        """
        return (1/(x * self.desv * math.sqrt(2 * math.pi))) * math.e ** (-(((math.log(x) - self.mean)**2) / (2*self.desv**2)))
    
    def get_num_parameters(self):
        """
        Number of parameters of the distribution
        """
        return len(self.parameters.keys())
    
    def parameter_restrictions(self):
        """
        Check parameters restrictions
        """
        v1 = self.mean > 0
        v2 = self.desv > 0
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
            {"mean": *, "desv": *}
        """
    
        
        μ = math.log(measurements.mean**2/math.sqrt(measurements.mean**2 + measurements.variance))
        σ = math.sqrt(math.log((measurements.mean**2 + measurements.variance)/(measurements.mean**2)))
        
        parameters = {"mean": μ, "desv": σ}
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
    path = "../data/data_lognormal.txt"
    data = get_data(path) 
    measurements = MEASUREMENTS(data)
    distribution = LOGNORMAL(measurements)
    
    print(distribution.get_parameters(measurements))
    print(distribution.cdf(measurements.mean))