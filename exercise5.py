import os


if __name__ == "__main__":
    n = 1000
    instructions = [
        f"scfg-toolkit/genFig -F 0 -c {n} -l 2 -L 14 > DATA/Tr-right-{n}",
        f"scfg-toolkit/genFig -F 1 -c {n} -l 2 -L 14 > DATA/Tr-equil-{n}",
        f"scfg-toolkit/genFig -F 2 -c {n} -l 2 -L 14 > DATA/Tr-isosc-{n}",
        f"scfg-toolkit/genFig -F 1 -c {n} -l 2 -L 14 > DATA/Tr-right-neg-{n}",
        f"scfg-toolkit/genFig -F 0 -c {int(n / 2)} -l 2 -L 14 > DATA/Tr-equil-neg-{n}",
        f"scfg-toolkit/genFig -F 2 -c {int(n / 2)} -l 2 -L 14 >> DATA/Tr-equil-neg-{n}",
        f"scfg-toolkit/genFig -F 1 -c {n} -l 2 -L 14 > DATA/Tr-isosc-neg-{n}",
        f"""scfg-toolkit/scfg_learn_mmi -g MODELS/G-1 -f MODELS/right-0.10 -p DATA/Tr-right-{n} -n DATA/Tr-right-neg-{n} -H 0.1 -i 1""",
        f"""scfg-toolkit/scfg_learn_mmi -g MODELS/G-1 -f MODELS/equil-0.10 -p DATA/Tr-equil-{n} -n DATA/Tr-equil-neg-{n} -H 0.1 -i 1""",
        f"""scfg-toolkit/scfg_learn_mmi -g MODELS/G-1 -f MODELS/isosc-0.10 -p DATA/Tr-isosc-{n} -n DATA/Tr-isosc-neg-{n} -H 0.1 -i 1""",
        r"""scfg-toolkit/scfg_prob -g MODELS/right-0.10 -m DATA/Ts-right > r""",
        r"""scfg-toolkit/scfg_prob -g MODELS/equil-0.10 -m DATA/Ts-right > e""",
        r"""scfg-toolkit/scfg_prob -g MODELS/isosc-0.10 -m DATA/Ts-right > i""",
        r"""paste r e i | awk '{m=$1;argm="right"; if ($2>m) {m=$2;argm="equil";} if ($3>m) {m=$3;argm="isosc";}printf("right %s\n",argm);}' > results""",
        r"""scfg-toolkit/scfg_prob -g MODELS/right-0.10 -m DATA/Ts-equil > r""",
        r"""scfg-toolkit/scfg_prob -g MODELS/equil-0.10 -m DATA/Ts-equil > e""",
        r"""scfg-toolkit/scfg_prob -g MODELS/isosc-0.10 -m DATA/Ts-equil > i""",
        r"""paste r e i | awk '{m=$2;argm="equil"; if ($1>m) {m=$1;argm="right";} if ($3>m) {m=$3;argm="isosc";} printf("equil %s\n",argm);}' >> results""",
        r"""scfg-toolkit/scfg_prob -g MODELS/right-0.10 -m DATA/Ts-isosc > r""",
        r"""scfg-toolkit/scfg_prob -g MODELS/equil-0.10 -m DATA/Ts-isosc > e""",
        r"""scfg-toolkit/scfg_prob -g MODELS/isosc-0.10 -m DATA/Ts-isosc > i""",
        r"""paste r e i | awk '{m=$3;argm="isosc"; if ($1>m) {m=$1;argm="right";} if ($2>m) {m=$2;argm="equil";} printf("isosc %s\n",argm);}' >> results""",
        r"""cat results | scfg-toolkit/confus""",
    ]
    
    for instruction in instructions:
        print(instruction)
        os.system(instruction)
