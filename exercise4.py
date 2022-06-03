import math

import numpy as np
from matplotlib import pyplot as plt
from sklearn.mixture import BayesianGaussianMixture


def sampling(gaussians, parameters, samples=1000):
    return [
        np.random.choice(gaussians, p=parameters, replace=False)()
        for _ in range(samples)
    ]


def sample_probability(x, mean, sd):
    var = float(sd) ** 2
    denom = (2 * math.pi * var) ** 0.5
    num = math.exp(-((float(x) - float(mean)) ** 2) / (2 * var))
    return num / denom


def compute_probabilities(sample, means, stds, pis, gamma=0.0):
    sample_probabilities = np.zeros((len(means)))
    accumulated_probabilities = 0.0
    for index, (mean, std, pi) in enumerate(zip(means, stds, pis)):
        probability = pi * sample_probability(sample, mean, std)
        accumulated_probabilities += probability
        sample_probabilities[index] = probability
    probabilities = sample_probabilities / accumulated_probabilities
    return probabilities * (1 + gamma * np.log(probabilities))


def em_step(samples, means, stds, pis, gamma=0.0):
    samples_probabilities = [
        compute_probabilities(sample, means, stds, pis, gamma) for sample in samples
    ]

    new_means = np.zeros((len(pis)))
    new_stds = np.zeros((len(pis)))
    new_pis = np.zeros((len(pis)))
    pi_denominator = 0.0
    for index, pi in enumerate(pis):
        base_denominator = 0.0
        mu_numerator = 0.0

        for index_sample, sample in enumerate(samples):
            sample_probability = samples_probabilities[index_sample][index]
            base_denominator += sample_probability
            mu_numerator += sample_probability * sample
            pi_denominator += sample_probability

        new_mu = mu_numerator / base_denominator
        std_numerator = 0.0
        for index_sample, sample in enumerate(samples):
            sample_difference = sample - new_mu
            std_numerator += (
                np.dot(sample_difference, sample_difference.T)
                * samples_probabilities[index_sample][index]
            )

        new_means[index] = new_mu
        new_stds[index] = std_numerator / base_denominator
        new_pis[index] = base_denominator
    return new_means, new_stds, new_pis / pi_denominator


def string_pis(pis):
    return " ".join([f"pi{index} = {pi:.3f}" for index, pi in enumerate(pis)])


if __name__ == "__main__":
    gaussians = [
        lambda: np.random.normal(-6, math.sqrt(4)),
        lambda: np.random.normal(2, math.sqrt(4)),
    ]
    gaussians_parameters = [0.4, 0.6]
    points = sampling(gaussians, gaussians_parameters, 1000)

    plt.hist(points, bins="fd")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.show()

    means = [-6, 2, 0]
    stds = [math.sqrt(4), math.sqrt(4), math.sqrt(4)]
    pis = [0.7, 0.1, 0.2]

    steps = 50
    print(f"Step 0/{steps}: theta0 = ({string_pis(pis)})")
    for i in range(1, 50 + 1):
        f_means, f_stds, pis = em_step(points, means, stds, pis, .1)
        if np.any(np.isnan(pis)) or np.any(pis < 0):
            break
        print(f"Step {i}/{steps}: theta0 = ({string_pis(pis)})", means, stds)
