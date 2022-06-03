import math


def compute_sum_c_by_P(Q, P, wt, j, c_prev):
    return sum([c_prev[i] * P.get(f"{i}-{wt}-{j}", 0.0) for i in Q])


def computation_step_step(Q, P, w, wt, c_prev, h_prev):
    denominator = [compute_sum_c_by_P(Q, P, w[wt], j, c_prev) for j in Q]
    total_denominator = sum(denominator)
    current_c = dict()
    current_h = dict()
    p = dict()

    for index, j in enumerate(Q):
        current_c[j] = denominator[index] / total_denominator

        for i in Q:
            if denominator[index] != .0:
                value = c_prev[i] * P.get(f"{i}-{w[wt]}-{j}", 0.0)
                if value != .0:
                    p[f"{i}|{j},{w[0:wt + 1]}"] = value / denominator[index]

        positive_part = 0.0
        negative_part = 0.0
        for i in Q:
            value = p.get(f"{i}|{j},{w[0:wt + 1]}", .0)
            if value == .0:
                continue
            positive_part += h_prev[i] * value
            negative_part += value * math.log2(value)
        current_h[j] = positive_part - negative_part
    return current_c, current_h, p


def compute(Q, P, I, word):
    h = dict()
    c = dict()
    p = dict()

    for j in Q:
        h[j] = 0.0
        c[j] = I.get(j, 0.0)
    for wt in range(len(word)):
        c, h, current_p = computation_step_step(Q, P, word, wt, c, h)
        print(f"Symbol {word[wt]}")
        print(f"\tc -> {c}")
        print(f"\th -> {h}")
        print(f"\tp -> {current_p}")
        p |= current_p
    return c, h, p


if __name__ == "__main__":
    Q = ["0", "1", "2", "3", "4"]
    S = {"a", "b"}
    I = {"0": 1}
    P = {
        "0-a-1": 0.2,
        "0-a-2": 0.8,
        "1-a-1": 0.3,
        "1-b-2": 0.4,
        "1-a-3": 0.3,
        "2-a-2": 0.3,
        "2-b-3": 0.5,
        "2-a-4": 0.2,
        "3-a-2": 0.6,
        "3-b-3": 0.2,
        "3-a-4": 0.2,
    }
    D = set(P.keys())
    F = {"4": 1}
    A = ()
    word = "aababa"
    p = compute(Q, P, I, word)
    print(f'H_A(theta|aababa) = {p[1]["4"]}')
