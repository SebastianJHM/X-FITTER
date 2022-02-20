import numpy as np
import pandas as pd
import scipy.stats as st
import matplotlib as mpl
import matplotlib.pyplot as plt
import math
import random
from measurements__ import MEASUREMENTS

mpl.style.use("ggplot")

def doanes_formula(data):
    """
    DONAE'S FORMULA
    https://en.wikipedia.org/wiki/Histogram#Doane's_formula
    """
    N = len(data)
    skewness = st.skew(data)
    sigma_g1 = math.sqrt((6*(N-2))/((N+1)*(N+3)))
    num_bins = 1 + math.log(N,2) + math.log(1+abs(skewness)/sigma_g1,2)
    num_bins = round(num_bins)
    return num_bins

def plot_histogram(data, results):
    ## Histogram of data
    plt.figure(figsize=(8, 4))
    plt.hist(data, bins=doanes_formula(data),density=True, ec='white', color=(168/235, 12/235, 12/235))
    plt.title('HISTOGRAM')
    plt.xlabel('Values')
    plt.ylabel('Frequencies')
    
    ll = min(data)
    ul = max(data)
    for distribution, sse in list(results.items())[:5]:
        if distribution.__class__.__name__ in ["LEVY", "CAUCHY", "FRECHET", "GENERALIZED_PARETO"]:
            ll = min(data) - 10
            ul = max(data) + 10
        x_plot = np.linspace(ll, ul, 1000)
        y_plot = [distribution.pdf(x) for x in x_plot]
        label_d = distribution.__class__.__name__ + ": " + str(round(sse, 4))
        color_d = [random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)]
        plt.plot(x_plot, y_plot, label=label_d, color=color_d)

    ## Plot n distributions
    # for distribution, p_value in results.items():
    #     if p_value > 0.05:
    #         x_plot = np.linspace(min(data), max(data), 1000)
    #         y_plot = [distribution.pdf(x) for x in x_plot]
    #         plt.plot(x_plot, y_plot, label=distribution.__class__.__name__ + ": " + str(round(p_value, 4)), color=(random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)))
    
    plt.legend(title='NOT REJECTED DISTRIBUTIONS', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.show()

def fit_data(data):
    from distributions.alpha import ALPHA
    from distributions.arcsine import ARCSINE
    from distributions.beta import BETA
    from distributions.bradford import BRADFORD
    from distributions.burr import BURR
    from distributions.burr_4p import BURR_4P
    from distributions.cauchy import CAUCHY
    from distributions.chi_square_3p import CHI_SQUARE_3P
    from distributions.chi_square import CHI_SQUARE
    from distributions.dagum import DAGUM
    from distributions.dagum_4p import DAGUM_4P
    from distributions.erlang import ERLANG
    from distributions.error_function import ERROR_FUNCTION
    from distributions.exponential import EXPONENTIAL
    from distributions.exponential_2p import EXPONENTIAL_2P
    from distributions.f import F
    from distributions.fatigue_life import FATIGUE_LIFE
    from distributions.frechet import FRECHET
    from distributions.folded_normal import FOLDED_NORMAL
    from distributions.gamma import GAMMA
    from distributions.gamma_3p import GAMMA_3P
    from distributions.generalized_extreme_value import GENERALIZED_EXTREME_VALUE
    from distributions.generalized_gamma import GENERALIZED_GAMMA
    from distributions.generalized_gamma_4p import GENERALIZED_GAMMA_4P
    from distributions.generalized_logistic import  GENERALIZED_LOGISTIC
    from distributions.generalized_normal import GENERALIZED_NORMAL
    from distributions.generalized_pareto import GENERALIZED_PARETO
    from distributions.gumbel_left import GUMBEL_LEFT
    from distributions.gumbel_right import GUMBEL_RIGHT
    from distributions.half_normal import HALF_NORMAL
    from distributions.hyperbolic_secant import HYPERBOLIC_SECANT
    from distributions.inverse_gamma import INVERSE_GAMMA
    from distributions.inverse_gaussian import INVERSE_GAUSSIAN
    from distributions.inverse_gamma_3p import INVERSE_GAMMA_3P
    from distributions.inverse_gaussian_3p import INVERSE_GAUSSIAN_3P
    from distributions.johnson_sb import JOHNSON_SB
    from distributions.johnson_su import JOHNSON_SU
    from distributions.kumaraswamy import KUMARASWAMY
    from distributions.laplace import LAPLACE
    from distributions.levy import LEVY
    from distributions.loggamma import LOGGAMMA
    from distributions.logistic import LOGISTIC
    from distributions.loglogistic import LOGLOGISTIC
    from distributions.loglogistic_3p import LOGLOGISTIC_3P
    from distributions.lognormal import LOGNORMAL
    from distributions.maxwell import MAXWELL
    from distributions.moyal import MOYAL
    from distributions.nakagami import NAKAGAMI
    from distributions.nc_chi_square import NC_CHI_SQUARE
    from distributions.nc_f import NC_F
    from distributions.nc_t_student import NC_T_STUDENT
    from distributions.normal import NORMAL
    from distributions.pareto_first_kind import PARETO_FIRST_KIND
    from distributions.pareto_second_kind import PARETO_SECOND_KIND
    from distributions.pearson_type_6 import PEARSON_TYPE_6
    from distributions.pearson_type_6_4p import PEARSON_TYPE_6_4P
    from distributions.pert import PERT
    from distributions.power_function import POWER_FUNCTION
    from distributions.rayleigh import RAYLEIGH
    from distributions.reciprocal import RECIPROCAL
    from distributions.rice import RICE
    from distributions.semicircular import SEMICIRCULAR
    from distributions.t_student import T_STUDENT
    from distributions.trapezoidal import TRAPEZOIDAL
    from distributions.triangular import TRIANGULAR
    from distributions.uniform import UNIFORM
    from distributions.weibull import WEIBULL
    
    from test_chi_square import test_chi_square
    from test_kolmogorov_smirnov import test_kolmogorov_smirnov
    from test_anderson_darling import test_anderson_darling
    
    _all_distributions = [
        BETA, BURR, CAUCHY, CHI_SQUARE, CHI_SQUARE_3P, DAGUM, ERLANG, ERROR_FUNCTION, 
        EXPONENTIAL, F, FATIGUE_LIFE, FRECHET, GAMMA, GENERALIZED_EXTREME_VALUE, 
        GENERALIZED_GAMMA, GENERALIZED_LOGISTIC, GENERALIZED_NORMAL, GUMBEL_LEFT, 
        GUMBEL_RIGHT, HYPERBOLIC_SECANT, INVERSE_GAMMA, INVERSE_GAUSSIAN, JOHNSON_SB, 
        JOHNSON_SU, KUMARASWAMY, LAPLACE, LEVY, LOGGAMMA, LOGISTIC, LOGLOGISTIC,
        LOGNORMAL,  NAKAGAMI, NORMAL, PARETO_FIRST_KIND, PARETO_SECOND_KIND, PEARSON_TYPE_6, 
        PERT, POWER_FUNCTION, RAYLEIGH, RECIPROCAL, RICE, T_STUDENT, TRAPEZOIDAL, TRIANGULAR,
        UNIFORM, WEIBULL
    ]

    _my_distributions = [ARCSINE]
    
    
    ## Calculae Histogram
    num_bins = doanes_formula(data)
    frequencies, bin_edges = np.histogram(data, num_bins, density=True)
    central_values = [(bin_edges[i] + bin_edges[i+1])/2 for i in range(len(bin_edges)-1)]
    
    measurements = MEASUREMENTS(data)
    
    results = {}
    for distribution_class in _my_distributions:
        try:
            distribution = distribution_class(measurements)
            # response = test_kolmogorov_smirnov(data, distribution)
            # p_value = response["p-value"]
            
            # if not math.isnan(p_value):
            #     results[distribution] = p_value
            
            
            
            ## Calculate fitted PDF and error with fit in distribution
            pdf_values = [distribution.pdf(c) for c in central_values]
            
            ## Calculate SSE (sum of squared estimate of errors)
            sse = np.sum(np.power(frequencies - pdf_values, 2.0))
            
            if not math.isnan(sse):
                results[distribution] = sse
            
        except:
            print(distribution_class.__name__)
            
    
    # results = {x:y for x,y in results.items() if y not in [0,1]}
    # results = {k: v for k, v in sorted(results.items(), key=lambda item: item[1], reverse=True)}
    
    results = {k: v for k, v in sorted(results.items(), key=lambda item: item[1])}
    print(results)
    return results
        
def main():
    ## Import data
    # data = pd.Series(sm.datasets.elnino.load_pandas().data.set_index('YEAR').values.ravel())
    def getData(direction):
        file  = open(direction,'r')
        data = [float(x.replace(",",".")) for x in file.read().splitlines()]
        return data
    
    path = "./data/data_arcsine.txt"
    data = getData(path)
    
    results = fit_data(data)
    plot_histogram(data, results)

if __name__ == "__main__":
    main()
    