import math

class HYPERBOLIC_SECANT:
    """
    Hyperbolic Secant distribution
    https://www.vosesoftware.com/riskwiki/Hyperbolic-Secantdistribution.php         
    """
    def __init__(self, measurements):
        self.parameters = self.get_parameters(measurements)
        self.miu = self.parameters["miu"]
        self.sigma = self.parameters["sigma"]

    def cdf(self, x):
        """
        Cumulative distribution function.
        Calculated with quadrature integration method of scipy.
        """
        z = lambda x: math.pi * (x - self.miu) / (2 * self.sigma)
        return (2/math.pi) * math.atan(math.exp((z(x))))
    
    def pdf(self, x):
        """
        Probability density function
        """
        z = lambda x: math.pi * (x - self.miu) / (2 * self.sigma)
        return (1/math.cosh(z(x)))/ (2 * self.sigma)
    
    def get_num_parameters(self):
        """
        Number of parameters of the distribution
        """
        return len(self.parameters.keys())
    
    def parameter_restrictions(self):
        """
        Check parameters restrictions
        """
        v1 = self.sigma > 0
        return v1

    def get_parameters(self, measurements):
        """
        Calculate proper parameters of the distribution from sample measurements.
        The parameters are calculated by formula.
        
        Parameters
        ----------
        measurements : dict
            {"miu": *, "variance": *, "skewness": *, "kurtosis": *, "data": *}

        Returns
        -------
        parameters : dict
            {"miu": *, "sigma": *}
        """
        
        miu = measurements.mean
        sigma = math.sqrt(measurements.variance)
        
        parameters = {"miu": miu, "sigma": sigma}
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
    path = "..\\data\\data_hyperbolic_secant.txt"
    data = get_data(path) 
    measurements = MEASUREMENTS(data)
    distribution = HYPERBOLIC_SECANT(measurements)
    
    print(distribution.get_parameters(measurements))
    print(distribution.cdf(measurements.mean))
    print(distribution.pdf(953.72))