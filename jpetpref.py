import numpy as np
import itertools
import time
from GIP import *
import json
import sys
import signal


def main():
    if (len(sys.argv) > 1):
        filename = sys.argv[1]
    else:
        filename = None
    result_dict = {}

    def handler(signum, frame):
        """
        Function to ensure data is still written when program
        is forcefully terminated
        """
        with open(filename, "w") as file:
            json.dump(result_dict, file)
        exit(1)

    signal.signal(signal.SIGINT, handler)

    manipulable_dict = {most_popular_cif: manipulable_try_all,
                        k_most_popular_cif: manipulable_through_winners,
                        inductive_consensus_cif: manipulable_try_all,
                        only_self_cif: manipulable_only_self}
    max_agents = 350
    sim_length = 10000
    prefers_fun = prefers_hamming
    # Number of agents for which to check all possible profiles
    max_check_all = 4
    cif = most_popular_cif

    # Generate random profile
    rng = np.random.default_rng()

    for agents in range(2, max_check_all + 1):
        manipulable_count = 0
        for profile in all_profiles(agents):
            if manipulable_dict[cif](profile, cif, prefers_fun, verbose=False):
                manipulable_count += 1
        print("agents: ", agents, "frequency: ",
              manipulable_count / 2 ** (agents ** 2))
        result_dict[agents] = manipulable_count / 2 ** (agents ** 2)

    for agents in range(max_check_all + 1, max_agents + 1):
        manipulable_count = 0

        for i in range(sim_length):
            profile = rng.integers(0, 2, (agents, agents))
            if manipulable_dict[cif](profile, cif, prefers_fun, verbose=False):
                manipulable_count += 1
        print("agents: ", agents, "frequency: ",
              manipulable_count / sim_length)
        result_dict[agents] = manipulable_count / sim_length

    with open(filename, "w") as file:
        json.dump(result_dict, file)


if __name__ == '__main__':
    main()
