import numpy as np
import time

def data_generator():
    interval = 0.2
    x = 1
    while True:
        mu = np.sin(x)
        sigma = np.cos(x) + 1.1
        observations = np.random.normal(loc=mu, scale=sigma, size=500) + np.random.normal(loc=0.01, scale=0.01, size=500)
        yield observations
        sleep_t = np.random.uniform(low=1, high=3)
        time.sleep(sleep_t)
        x += interval * sleep_t
