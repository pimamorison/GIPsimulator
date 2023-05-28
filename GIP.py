import numpy as np
import itertools
import math


def secondmax(arr: np.ndarray):
    partition = np.partition(arr, -2)
    return partition[-2]


def prefers_outcome(a: np.ndarray, b: np.ndarray, honest_opinion: np.ndarray):
    """
    Function that computes if outcome a is preferred to outcome b according
    to the Separability preference relation defined by Cho and Saporiti. If this
    function returns true, a is preferred to b, or if a and b are not
    comparable. If it returns false, then b is preferred to a.
    """
    if np.array_equal(a, b):
        return False
    a_better = False
    b_better = False
    for i in range(len(honest_opinion)):
        if a[i] != b[i]:
            if a[i] == honest_opinion[i] and b[i] != honest_opinion[i]:
                a_better = True
            else:
                b_better = True
        if a_better and b_better:
            return True

    if b_better and not a_better:
        return False
    return True


def prefers_hamming(a: np.ndarray, b: np.ndarray, honest_opinion: np.ndarray):
    if np.array_equal(a, b):
        return False
    dist_a = np.count_nonzero(a != honest_opinion)
    dist_b = np.count_nonzero(b != honest_opinion)
    if dist_a <= dist_b:
        return True
    return False


def prefers_intersection(a: np.ndarray, b: np.ndarray, honest_opinion: np.ndarray):
    if np.array_equal(a, b):
        return False
    inter_a = np.sum(np.logical_and(a, b))
    inter_b = np.sum(np.logical_and(a, b))
    if inter_a >= inter_b:
        return True
    return False


def only_self_cif(profile: np.ndarray):
    result = np.zeros(len(profile[0]))
    for i, opinion in enumerate(profile):
        if sum(opinion) == 1 and opinion[i] == 1:
            result[i] = 1
    return result


def inductive_consensus_cif(profile: np.ndarray):
    profile_sum = profile.sum(axis=0)
    new_agents = (profile_sum == len(profile_sum)).astype(int)
    result = new_agents

    while(sum(new_agents) and not all(result)):
        member_profile = profile[np.argwhere(new_agents == 1).flatten(), :]
        profile_sum = member_profile.sum(axis=0)

        # Set number of votes to 0 if agent does vote for themselves.
        for i in range(len(profile)):
            if profile[i, i] == 0:
                profile_sum[i] = 0
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


def k_most_popular_cif(profile: np.ndarray):
    """
    Computes social decision. Output is a list of 0s and 1s
    where the element at index i is 1 if agent i is selected.
    """
    profile = profile.sum(axis=0)
    k = math.ceil(len(profile) / 5)
    k_highest_votes = np.partition(profile, -k)[-2]
    result = (profile >= k_highest_votes).astype(int)
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


def manipulable_try_all(profile: np.ndarray, cif, prefers_fun, verbose=False):
    """
    Function that looks at a profile and determines if it is manipulable by
    letting all agents try all possible opinions. If an agent is found
    that can manipulate, return True. If all agents are tried without any
    manipulation, return False.
    """
    agents = profile.shape[0]
    original_outcome = cif(profile)
    new_profile = np.copy(profile)
    # manip_agents = np.unique(profile, axis=0, return_index=True)[1]
    manip_agents = range(agents)

    # Loop through all agents
    for manip_agent in manip_agents:
        honest_opinion = profile[manip_agent]
        # Generate all possible opinions
        for new_opinion in all_opinions(agents):
            new_profile[manip_agent] = new_opinion
            new_outcome = cif(new_profile)

            if (prefers_fun(new_outcome, original_outcome, honest_opinion)):
                if verbose:
                    print("original profile: \n", profile)
                    print("new profile:\n", new_profile)
                    print("new outcome:", new_outcome)
                    print("old outcome:", original_outcome)
                    print("honest opin:", honest_opinion)
                    print("Manip agent:", manip_agent)
                    print(prefers_fun(new_outcome,
                                      original_outcome, honest_opinion), "\n")
                return True
        new_profile[manip_agent] = honest_opinion

    return False


def manipulable_through_winners(profile: np.ndarray, cif, prefers_fun, verbose=False):
    """
    Function that looks at a profile and determines if it is manipulable by
    letting all agents try all possible opinions. If an agent is found
    that can manipulate, return True. If all agents are tried without any
    manipulation, return False.
    """
    original_outcome = cif(profile)
    new_profile = np.copy(profile)
    # manip_agents = np.unique(profile, axis=0, return_index=True)[1]
    manip_agents = range(profile.shape[0])
    winners = np.argwhere(original_outcome == 1).flatten()

    # Loop through all agents
    for manip_agent in manip_agents:
        honest_opinion = profile[manip_agent]
        # Generate all possible opinions

        for changed_votes in all_opinions(len(winners)):
            np.put(new_profile[manip_agent], winners, changed_votes)
            new_outcome = cif(new_profile)

            if (prefers_fun(new_outcome, original_outcome, honest_opinion)):
                if verbose:
                    print("original profile: \n", profile)
                    print("new profile:\n", new_profile)
                    print("new outcome:", new_outcome)
                    print("old outcome:", original_outcome)
                    print("honest opin:", honest_opinion)
                    print("Manip agent:", manip_agent)
                    print(prefers_fun(new_outcome,
                                      original_outcome, honest_opinion), "\n")
                return True
        new_profile[manip_agent] = honest_opinion

    return False


def manipulable_only_self(profile: np.ndarray, cif, prefers_fun, verbose=False):
    """
    Function that looks at a profile and determines if it is manipulable by
    letting all agents try all possible opinions. If an agent is found
    that can manipulate, return True. If all agents are tried without any
    manipulation, return False.
    """
    agents = profile.shape[0]
    original_outcome = cif(profile)
    new_profile = np.copy(profile)
    # manip_agents = np.unique(profile, axis=0, return_index=True)[1]
    manip_agents = range(agents)

    # Loop through all agents
    for manip_agent in manip_agents:
        honest_opinion = profile[manip_agent]

        new_opinion = np.zeros(agents)
        new_opinion[manip_agent] = 1
        new_profile[manip_agent] = new_opinion
        new_outcome = cif(new_profile)

        if (prefers_fun(new_outcome, original_outcome, honest_opinion)):
            if verbose:
                print("original profile: \n", profile)
                print("new profile:\n", new_profile)
                print("new outcome:", new_outcome)
                print("old outcome:", original_outcome)
                print("honest opin:", honest_opinion)
                print("Manip agent:", manip_agent)
                print(prefers_fun(new_outcome,
                                  original_outcome, honest_opinion), "\n")
            return True
        new_profile[manip_agent] = honest_opinion

    return False
