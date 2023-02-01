###########################
# 6.00.2x Problem Set 1: Space Cows 

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """

    cow_dict = dict()

    f = open(filename, 'r')
    
    for line in f:
        line_data = line.split(',')
        cow_dict[line_data[0]] = int(line_data[1])
    return cow_dict


# Problem 1
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # list of cow weights, descending order
    cowsWeightsSorted = sorted(cows.values(), reverse=True)
    #list of cow names
    cowsNames = [i for i in cows.keys()]
    # list of cow names, sorted by corresponding weights
    cowsNamesSorted = sorted(cowsNames, key=lambda cow: cows[cow], reverse=True)

    # result is a list containing trip lists
    result = []
    # gone is a dict that tells us whether a cow is sent yet
    gone = {k: False for k, v in cows.items()}
    # allGone flagged True once we've sent all cows via some number of trips
    allGone = False

    # while cows remain to be sent:
    while not allGone:
        # each trip runs up a cost that must remain <= limit
        totalCost = 0
        # trip is a list of cows' names to be sent on a trip together
        trip = []
        # iterate over all cows
        for i in range(len(cows)):
            # if cow is yet to be sent and does not put trip over weight, add cow to trip
            if (totalCost + cowsWeightsSorted[i]) <= limit \
                and gone[cowsNamesSorted[i]] == False:

                trip.append(cowsNamesSorted[i])
                totalCost += cowsWeightsSorted[i]
                # update gone as we've handled this cow
                gone[cowsNamesSorted[i]] = True
        # add trip list to result list
        result.append(trip)
        # test whether we've sent all cows yet
        allGone = True if all(gone.values()) else False

    return result



# Problem 2
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # copy cows dict
    cowsCopy = cows.copy()
    #list of cow names
    cowsNames = [i for i in cowsCopy.keys()]
    result = []
    
    # iterate over all partitions using unique cowNames strings
    for iter_ in (get_partitions(cowsNames)):
        # appender flag True if all lists (trips) in partition are under limit
        appender = True
        # for every list in partition...
        for ls in iter_:
            # if trip weight is over limit...
            if sum([cowsCopy[i] for i in ls]) > limit:
                # don't add that partition to result
                appender = False
        # if no interior lists flagged, add the partition to the result list
        if appender == True:
            result.append(iter_)
    # optimal solution is solution with least number of interior lists
    return min(result, key=len)

        
# Problem 3
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    # time greedy implementation
    startG = time.time()
    runGreedy = greedy_cow_transport(cows, limit=10)
    endG = time.time()

    # time brute force implementation
    startB = time.time()
    runBruteForce = brute_force_cow_transport(cows, limit=10)
    endB = time.time()

    # formatting
    double = '===================================================================================================================================='
    single = '--------------------------------'

    # print time and solution for each implementation
    print(double, '\n~ Greedy implementation ~      |', '\n'+single, '\n' + str(endG-startG) + ' SECONDS\n' + str(len(runGreedy)) + ' TRIPS')
    print(str(runGreedy))
    print(double, '\n~ Brute Force implementation ~ |', '\n'+single, '\n' + str(endB-startB) + ' SECONDS\n' + str(len(runBruteForce)) + ' TRIPS')
    print(str(runBruteForce), '\n' + double + '\n')


"""
TEST DATA
"""

cows = load_cows("ps1_cow_data.txt")
limit=100
#print(cows)

compare_cow_transport_algorithms()

#print(greedy_cow_transport(cows, limit))
#print(brute_force_cow_transport(cows, limit))