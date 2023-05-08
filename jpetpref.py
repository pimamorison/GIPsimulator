import numpy as np
import itertools
import time


def prefers_outcome(a: np.ndarray, b: np.ndarray, honest_opinion: np.ndarray):
    """
    Function that computes if outcome a is preferred to outcome b according
    to the Separability preference relation defined by Cho and Saporiti. If this
    function returns true, a is preferred to b. If it returns false, then either
    b is preferred to a or a and b are not comparable.
    """
    if np.array_equal(a, b):
        return False
    for i in range(len(honest_opinion)):
        if a[i] != b[i]:
            if a[i] == honest_opinion[i] and b[i] != honest_opinion[i]:
                pass
            else:
                return False

    return True


def inductive_consensus_cif(profile: np.ndarray):
    profile_sum = profile.sum(axis=0)
    new_agents = (profile_sum == len(profile_sum)).astype(int)
    result = new_agents

    # TODO: add condition that agent votes for itself
    while(sum(new_agents) and not all(result)):
        member_profile = profile[np.argwhere(new_agents == 1).flatten(), :]
        profile_sum = member_profile.sum(axis=0)
        new_agents = np.array(
            (profile_sum == member_profile.shape[0]).astype(int))
        # logical and to assure that we take only new agents and not all agents in result
        new_agents = np.logical_and(new_agents, np.logical_not(result))
        result = np.logical_or(result, new_agents).astype(int)
    return result


def most_popular_cif(profile: np.ndarray):
    profile = profile.sum(axis=0)
    result = (profile == profile.max()).astype(int)
    return result


def to_bitarray(integer: int, array_length: int):
    """
    Convert integer to array of bits representing the integer value.
    Big endian.
    """
    bitstring = format(integer, '0' + str(array_length) + 'b')
    bitarray = np.array([int(bit) for bit in bitstring])
    return bitarray


def all_opinions(agents: int):
    """"
    Returns list of all possible opinions that can be made with given
    number of agents.
    """
    return np.array(list(itertools.product([0, 1], repeat=agents)))


def all_profiles(agents: int):
    """
    Returns list of all possible profiles that can be made with given
    number of agents.
    """
    return np.array(list(itertools.product(all_opinions(agents), repeat=agents)))
    # return np.array(list(itertools.combinations_with_replacement(all_opinions(agents), agents)))


def manipulable(profile: np.ndarray, agents: int, cif: np.ndarray, verbose=False):
    """
    Function that looks at a profile and determines if it is manipulable by
    letting all agents try all possible opinions. If an agent is found
    that can manipulate, return True. If all agents are tried without any
    manipulation, return False.
    """
    original_outcome = cif(profile)
    new_profile = np.copy(profile)
    # manip_agents = np.unique(profile, axis=0, return_index=True)[1]
    manip_agents = range(agents)

    # Loop through all unique agents
    for manip_agent in manip_agents:
        honest_opinion = profile[manip_agent]
        # Generate all possible opinions
        for new_opinion in all_opinions(agents):
            start_time = time.time()
            new_profile[manip_agent] = new_opinion
            new_outcome = cif(new_profile)

            if (prefers_outcome(new_outcome, original_outcome, honest_opinion)):
                print("agents:", agents, time.time() - start_time)
                if verbose:
                    print("original profile: \n", profile)
                    print("new profile:\n", new_profile)
                    print("new outcome:", new_outcome)
                    print("old outcome:", original_outcome)
                    print("honest opin:", honest_opinion)
                    print("Manip agent:", manip_agent)
                    print(prefers_outcome(new_outcome,
                                          original_outcome, honest_opinion), "\n")
                return True
            print("agents:", agents, time.time() - start_time)
        new_profile[manip_agent] = honest_opinion

    return False


max_agents = 20

sim_length = 1

cif = most_popular_cif

# Generate random profile
rng = np.random.default_rng()


for agents in range(2, 4):
    manipulable_count = 0
    for profile in all_profiles(agents):
        if manipulable(profile, agents, cif):
            manipulable_count += 1
    print("agents: ", agents, "frequency: ",
          manipulable_count / 2 ** (agents ** 2))

for agents in range(4, max_agents + 1):
    manipulable_count = 0

    for i in range(sim_length):
        profile = rng.integers(0, 2, (agents, agents))

        if manipulable(profile, agents, cif):
            manipulable_count += 1
    print("agents: ", agents, "frequency: ", manipulable_count / sim_length)


profile = np.array([[0, 1, 1, 0], [1, 1, 1, 1], [1, 1, 1, 0], [1, 0, 0, 0]])
