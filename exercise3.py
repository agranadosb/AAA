import math
import random

import numpy as np


class MaximumEntropyModel:
    def __init__(self, S, features, lambdas, threshold=0.001):
        self.S = S
        self.features = features
        self.lambdas = lambdas
        self.labels = set([label for _, label in S])
        self.empirical_distribution = None
        self.p_lambda_distribution = None
        self.threshold = threshold
        self.compute_empirical_distribution().compute_p_lambda_distribution()

    def compute_empirical_distribution(self):
        result = {"prior": {}, "intersection": {}}
        samples = []
        labels = []
        intersections = []
        for sample, label in self.S:
            samples.append(sample)
            labels.append(label)
            intersections.append(f"{sample}-{label}")

        for sample in samples:
            result["prior"][sample] = samples.count(sample) / len(samples)
            for label in labels:
                value = intersections.count(f"{sample}-{label}") / len(samples)
                if value != 0.0:
                    result["intersection"][f"{sample}-{label}"] = value
        self.empirical_distribution = result
        return self

    def compute_sample_lambda(self, sample, label):
        return sum(
            [
                lambda_value * self.features[lambda_name](sample, label)
                for lambda_name, lambda_value in self.lambdas.items()
            ]
        )

    def compute_p_lambda_distribution(self):
        p_lambda_distribution = {}
        for sample, _ in S:
            p_lambda_distribution[sample] = {}
            z_x_list = [
                math.e ** self.compute_sample_lambda(sample, label) for label in self.labels
            ]
            z_x = sum(z_x_list)

            for index, label in enumerate(self.labels):
                sample_lambdas = z_x_list[index]
                value = sample_lambdas / z_x

                p_lambda_distribution[sample][label] = value

        self.p_lambda_distribution = p_lambda_distribution
        return self

    def compute_delta_i(self, lambda_name):
        empirical_p_fi = 0.0
        lambda_p_fi = 0.0
        for sample, label in S:
            sample_feature = self.features[lambda_name](sample, label)
            empirical_p_fi += (
                self.empirical_distribution["intersection"][f"{sample}-{label}"]
                * sample_feature
            )
            lambda_p_fi += (
                self.empirical_distribution["prior"][sample]
                * self.p_lambda_distribution[sample][label]
                * self.features[lambda_name](sample, label)
            )
        return (1 / len(features)) * np.log(empirical_p_fi / lambda_p_fi)

    def step_lambdas(self):
        for lambda_name, lambda_value in self.lambdas.items():
            self.lambdas[lambda_name] = lambda_value + self.compute_delta_i(lambda_name)
        self.lambdas = lambdas
        return self

    def compute_error(self):
        errors = 0
        for sample, real_label in self.S:
            labels = []
            score = []
            for label in self.labels:
                labels.append(label)
                score.append(self.p_lambda_distribution[sample][label])
            errors += labels[np.argmax(score)] != real_label
        return errors / len(S)

    def is_optimum(self):
        optimum_value = 0.0

        for feature in self.features:
            sample_sum = 0.0
            features_sum = 0.0
            for sample, label in S:
                sample_sum += sum(
                    [
                        self.p_lambda_distribution[sample].get(label_2, 0.0)
                        * self.features[feature](sample, label_2)
                        for label_2 in self.labels
                    ]
                )
                features_sum += self.features[feature](sample, label)
            optimum_value += abs(features_sum - sample_sum) < self.threshold

        return optimum_value == len(S)

    def fit(self, steps=10):
        error = self.compute_error()
        print(f"Step {0}/{steps} error {error:.2%} lambdas {self.lambdas}")
    
        for step in range(1, steps + 1):
            if self.is_optimum():
                return
        
            self.step_lambdas().compute_p_lambda_distribution()
            error = self.compute_error()

            print(f"Step {step}/{steps} error {error:.2%} lambdas {self.lambdas}")


if __name__ == "__main__":
    # Compute maximum entropy model
    S = (
        ("aa", "C0"),
        ("bb", "C0"),
        ("ab", "C1"),
        ("ba", "C1"),
    )

    features = {
        "C1-a": lambda word, label: 1 if word[0] == "a" and word.count("a") == 1 and label == "C1" else 0,
        "C1-b": lambda word, label: 1 if word[0] == "b" and word.count("b") == 1 and label == "C1" else 0,
        "C2-a": lambda word, label: 1 if word[0] == "a" and label == "C0" else 0,
        "C2-b": lambda word, label: 1 if word[0] == "b" and label == "C0" else 0,
    }

    lambdas = {
        "C1-a": random.random(),
        "C1-b": random.random(),
        "C2-a": random.random(),
        "C2-b": random.random()
    }
    # features = {
    #     "C1": lambda word, label: 1 if (word.count("a") == 2 or word.count("b") == 2) and label == "C0" else 0,
    #     "C2": lambda word, label: 1 if word.count("a") == 1 and word.count("b") == 1 and label == "C1" else 0,
    # }
    # lambdas = {
    #     "C1": random.random(),
    #     "C2": random.random(),
    # }

    model = MaximumEntropyModel(S, features, lambdas)
    model.fit(10)
