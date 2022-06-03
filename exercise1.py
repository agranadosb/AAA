"""
    H(S | C, L)
    = sum(ci, li -> p(ci, li) * H(S| ci, li))                                       : ci <- C, li <- L
    = -sum(ci, li -> p(ci, li) * sum(si -> p(si | ci, li) * log(p(si | ci, li))))   : si <- S, ci <- C, li <- L
    = -sum(ci, li -> sum(si -> p(ci, li, si) * log(p(si | ci, li))))                : si <- S, ci <- C, li <- L
    
    p(si | ci, li)              : si <- S, ci <- C, li <- L
    = p(si, ci, li) / p(ci, li) : si <- S, ci <- C, li <- L
"""

# Order -> C-L-S
import math

INTERSECTIONS = {
    "DES-DIA-SEG": .3,
    "DES-DIA-ACC": .01,
    "DES-NOC-SEG": .13,
    "DES-NOC-ACC": .02,
    "NUB-DIA-SEG": .2,
    "NUB-DIA-ACC": .01,
    "NUB-NOC-SEG": .1,
    "NUB-NOC-ACC": .02,
    "LLU-DIA-SEG": .07,
    "LLU-DIA-ACC": .03,
    "LLU-NOC-SEG": .06,
    "LLU-NOC-ACC": .05,
    "DES-DIA": .31,
    "DES-NOC": .15,
    "NUB-DIA": .21,
    "NUB-NOC": .12,
    "LLU-DIA": .10,
    "LLU-NOC": .11,
}

C = {"DES", "NUB", "LLU"}
L = {"DIA", "NOC"}
S = {"SEG", "ACC"}


def intersection_sum(si):
    intersection_sum = .0
    for ci in C:
        for li in L:
            intersection_sum += INTERSECTIONS[f"{ci}-{li}-{si}"]
    return intersection_sum


if __name__ == "__main__":
    result = .0
    for si in S:
        total_intersection_si = intersection_sum(si)
        for ci in C:
            for li in L:
                intersection_ci_li_si = INTERSECTIONS[f"{ci}-{li}-{si}"]
                intersection_ci_li = INTERSECTIONS[f"{ci}-{li}"]
                p_si__ci_li = intersection_ci_li_si / intersection_ci_li

                partial_sum = intersection_ci_li_si * math.log2(p_si__ci_li)
                print(f"p(C={ci},L={li},S={si})*log(p(S={si}|C={ci},L={li})) = {partial_sum}")
                result += partial_sum
    print(f"H(S|C,L) = {result * -1}")
