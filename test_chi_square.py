import scipy.stats
import math
import numpy as np

def danoes_formula(data):
    """
    DANOE'S FORMULA
    https://en.wikipedia.org/wiki/Histogram#Doane's_formula
    
    Parameters
    ----------
    data : iterable 
        data set
    Returns
    -------
    num_bins : int
        Cumulative distribution function evaluated at `x`
    """
    N = len(data)
    skewness = scipy.stats.skew(data)
    sigma_g1 = math.sqrt((6*(N-2))/((N+1)*(N+3)))
    num_bins = 1 + math.log(N,2) + math.log(1+abs(skewness)/sigma_g1,2)
    num_bins = round(num_bins)
    return num_bins
   
def test_chi_square(data, distribution):
    """
    Chi Square test to evaluate that a sample is distributed according to a probability 
    distribution.
    
    The hypothesis that the sample is distributed following the probability distribution
    is not rejected if the test statistic is less than the critical value or equivalently
    if the p-value is less than 0.05
    
    Parameters
    ----------
    data: iterable
        data set
    distribution: class
        distribution class initialized whit parameters of distribution and methods
        cdf() and get_num_parameters()
        
    Return
    ------
    result_test_chi2: dict
        1. test_statistic(float):
            sum over all classes of the value (expected - observed) ^ 2 / expected 
        2. critical_value(float):
            inverse of the distribution chi square to 0.95 with freedom degrees
            n - 1 minus the number of parameters of the distribution.
        3. p-value[0,1]:
            right-tailed probability of the test statistic for the chi-square distribution
            with the same degrees of freedom as for the critical value calculation.
        4. rejected(bool):
            decision if the null hypothesis is rejected. If it is false, it can be 
            considered that the sample is distributed according to the probability 
            distribution. If it's true, no.
    """
    ## Parameters and preparations
    num_bins = danoes_formula(data)
    N = len(data)
    frequencies, bin_edges = np.histogram(data, num_bins)
    freedom_degrees = num_bins - 1 - distribution.get_num_parameters()
    
    ## Calculation of errors
    errors = []
    for i, obs in enumerate(frequencies):
        lower = bin_edges[i]
        upper = bin_edges[i+1]
        exp = N * (distribution.cdf(upper) - distribution.cdf(lower))
        errors.append(((obs - exp)**2) / exp)
    
    ## Calculation of indicators
    statistic_chi2 = sum(errors)
    critical_value = scipy.stats.chi2.ppf(0.95, freedom_degrees)
    p_value = 1 -  scipy.stats.chi2.cdf(statistic_chi2, freedom_degrees)
    rejected = statistic_chi2 >= critical_value
    
    ## Construction of answer
    result_test_chi2 = {
        "test_statistic": statistic_chi2, 
        "critical_value": critical_value, 
        "p-value": p_value,
        "rejected": rejected
        }
    
    return result_test_chi2
    
if __name__ == "__main__":
    from utilities.data_measurements import get_measurements
    from distributions.beta import BETA
    from distributions.burr import BURR
    from distributions.cauchy import CAUCHY
    from distributions.chi_square import CHI_SQUARE
    from distributions.dagum import DAGUM
    from distributions.erlang import ERLANG
    from distributions.error_function import ERROR_FUNCTION
    from distributions.exponencial import EXPONENCIAL
    from distributions.f import F
    from distributions.fatigue_life import FATIGUE_LIFE
    from distributions.frechet import FRECHET
    from distributions.gamma import GAMMA
    from distributions.generalized_extreme_value import GENERALIZED_EXTREME_VALUE
    from distributions.generalized_gamma import GENERALIZED_GAMMA
    from distributions.generalized_normal import GENERALIZED_NORMAL
    from distributions.johnson_SB import JOHNSON_SB
    from distributions.johnson_SU import JOHNSON_SU
    from distributions.lognormal import LOGNORMAL
    from distributions.normal import NORMAL
    from distributions.triangular import TRIANGULAR
    from distributions.uniform import UNIFORM
    from distributions.weibull import WEIBULL
    
    
    def getData(direction):
        file  = open(direction,'r')
        data = [float(x.replace(",",".")) for x in file.read().splitlines()]
        return data
    
    _all_distributions = [BETA, BURR, CAUCHY, CHI_SQUARE, DAGUM, ERLANG, ERROR_FUNCTION, 
                          EXPONENCIAL, F, FATIGUE_LIFE, FRECHET, GAMMA, GENERALIZED_EXTREME_VALUE, 
                          GENERALIZED_GAMMA, GENERALIZED_NORMAL, JOHNSON_SB, JOHNSON_SU, 
                          LOGNORMAL, NORMAL, TRIANGULAR,UNIFORM,  WEIBULL]
    _my_distributions = [NORMAL]
    
    for distribution_class in _all_distributions:
        print(distribution_class.__name__)
        path = "C:\\Users\\USUARIO1\\Desktop\\Fitter\\data\\data_" + distribution_class.__name__.lower() + ".txt"
        data = getData(path)
                
        measurements = get_measurements(data)
        distribution = distribution_class(measurements)
        print(distribution.pa)
        print(test_chi_square(data, distribution))