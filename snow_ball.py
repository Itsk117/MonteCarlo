import numpy as np
from math import exp, sqrt
from time import *
def SnowBall(Su, Sd, sigma, rf, q, T, N, R, S0 = 100):
    
    S = np.random.randn(N, T+1)
    dt = 1/360
    S[:, 0] = S0
    pay_off = 0
    for i in range(T):
        S[:, i+1] = S[:, i] * np.exp((rf-q-0.5*sigma**2)*dt \
        + sigma*sqrt(dt) * S[:, i+1])
    month = list(range(0, T, 30))
    knock_out = S[:, month] >= Su
    knock_out = knock_out.any(axis=1)
    S_ko = S[knock_out]
    S_rest = S[knock_out == False]
    
    for i in month:
        n = len(S_ko)
        judge = S_ko[:, [i]] < Su
        S_ko = S_ko[judge.all(axis = 1)]
        pay_off += (n - len(S_ko)) * ((1 + R*i/360) / exp(rf*i/360) - 1)
    
    knock_in = S_rest.min(axis = 1) <= Sd
    S_ki = S_rest[knock_in]
    S_rest = S_rest[knock_in == False]
    knock_in_loss = S_ki[:, [-1]] < S0
    knock_in_loss = knock_in_loss.all(axis = 1)
    S_ki1 = S_ki[knock_in_loss]
    S_ki2 = S_ki[knock_in_loss == False]
    
    pay_off += len(S_rest) * ((1 + R*T/360)/exp(rf*T/360) - 1) \
        + np.sum((S_ki1[:, [-1]] - S0)/(S0*exp(rf*T/360)) - 1) \
        + len(S_ki2) * (1 / exp(rf*T/360) - 1)
    pay_off /= N
    return pay_off
  
begin = time()        
S = SnowBall(105, 75, 0.15, 0.03, 0, 360, 100000, 0.2) 
end = time()
print('pay off为%s'%S,'用时:',end-begin,'秒')   