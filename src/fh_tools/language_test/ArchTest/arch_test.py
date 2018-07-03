# GARCH(1,1) Model in Python
#   uses maximum likelihood method to estimate (omega,alpha,beta)
# (c) 2014 QuantAtRisk, by Pawel Lachowicz; tested with Python 3.5 only

from arch import arch_model
import numpy as np
import statsmodels.api as sm  # 统计相关的库
import arch

r = np.array([0.945532630498276,
              0.614772790142383,
              0.834417758890680,
              0.862344782601800,
              0.555858715401929,
              0.641058419842652,
              0.720118656981704,
              0.643948007732270,
              0.138790608092353,
              0.279264178231250,
              0.993836948076485,
              0.531967023876420,
              0.964455754192395,
              0.873171802181126,
              0.937828816793698])


# garch11 = arch_model(r, p=1, q=1)
# res = garch11.fit(update_freq=10)
# print(res.summary())

arma_mod20 = sm.tsa.ARMA(r, (2, 0)).fit()
print('*'*8)
# print(arma_mod20.aic,arma_mod20.bic,arma_mod20.hqic)
print(arma_mod20.fittedvalues)

def fhs_garch(data):
    arma_mod20 = sm.tsa.ARMA(r, (2, 0)).fit()
    am = arch.arch_model(arma_mod20.fittedvalues, mean='AR', lags=8, vol='GARCH')
    res = am.fit()
    print(res)

#fhs_garch(r)
