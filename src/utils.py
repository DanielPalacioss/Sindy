def weighted_average(values, weights):
    return sum(v * w for v, w in zip(values, weights)) / sum(weights)