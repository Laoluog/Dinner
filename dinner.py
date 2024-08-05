def find_dislikes(friends: dict)->set[tuple[str]]:
    """Given a dictionary-based adjacency list of String-based nodes,
       returns a set of all edges in the graph (ie. dislikes who can't be invited together).
    """
    myset = set()
    for key in friends.keys():
        x = key
        for seckey in friends.keys():
            if seckey != x:
                keyvals = friends.get(seckey)
                if x in keyvals:
                    ntuple = []
                    ntuple.append(seckey)
                    ntuple.append(x)
                    ntuple = sorted(ntuple)
                    myset.add(tuple(ntuple))
    return myset

def filter_no_dislikes(friends:dict)->tuple[list[str], dict]:
    '''An optimization that removes friends who are not in any dislikes relationships,
       prior to generating combinations and add them to the invite list.
    '''
    nodislikes = []
    dislist = friends
    newdict = {}
    nodislist = []
    for key in friends.keys():
        if friends.get(key) == []:
            nodislist.append(key)
    for keyy in friends.keys():
        if keyy not in nodislist:
            newdict[keyy] = friends[keyy]
    returner = ((nodislist, newdict))
    return returner

def filter_bad_invites(all_subsets:list, friends:dict)->list[list[str]]:
    '''Removes subsets from all_subsets that contain any pair of friends who
       are in a dislike relationship
    '''
    returner = []
    for sub in all_subsets:
        inv = True
        for friend in friends:
            for x in friends[friend]:
                if friend in sub and x in sub:
                    inv = False
                    break
        if inv == True:
            returner.append(sub)
    return returner

def invite_to_dinner_optimized(friends:dict)->list[str]:
    '''Finds the combination with the maximum number of guests without storing all subset combinations
    '''
    allsubs = generate_all_subsets(friends)
    badinvs = filter_bad_invites(allsubs, friends)          

    opti = []
    for y in allsubs:
        valid = True
        for z in badinvs:
            if y == z:
                valid = False
                break
        if valid:
            opti.append(y)
    returner = set()
    for x in opti:
        for i in x:
            returner.add(i)
    return list(returner)



def generate_all_subsets(friends: dict)->list[list[str]]:
    '''Converts each number from 0 to 2^n - 1 into binary and uses the binary representation
       to determine the combination of guests and returns all possible combinations
    '''
    friend_list = list(friends.keys())
    n = len(friends)
    
    all_subsets = []

    for i in range(2**n):
        num = i  #convert each number in the range to a binary string
        new_subset = []
        for j in range(n): # to_binary_division approach
            if (num % 2 == 1): # 1 indicates the guest is included
                new_subset = [friend_list[n-1-j]] + new_subset 
            num = num // 2
        all_subsets.append(new_subset)

    return all_subsets

def invite_to_dinner_slow(friends: dict)-> list[str]:
    '''Finds the invite combo with the maximum number of guests via the exhaustive approach:
            1. Generate every possible combination of guests
            2. Filter out the combinations that include dislike relationships
            3. Find the combination which give you the maximum number of invites
    '''
    all_subsets = generate_all_subsets(friends)
    only_good_subsets = filter_bad_invites(all_subsets, friends)

    #find the subset which maximizes number of invites
    invite_list = []
    for i in only_good_subsets:
        if len(i) > len(invite_list):
            invite_list = i

    return invite_list

def invite_to_dinner_better(friends: dict)-> list[str]:
    '''Finds the invite combo with the maximum number of guests
    '''
    definite_invites, problem_friends = filter_no_dislikes(friends)
    fewer_subsets = generate_all_subsets(problem_friends) #smaller graph
    only_good_subsets = filter_bad_invites(fewer_subsets, problem_friends)

    #find the subset which maximizes number of invites
    invite_list = []
    for i in only_good_subsets:
        if len(i) > len(invite_list):
            invite_list = i

    #recombine with definite invites in Pythonic fashion
    invite_list += definite_invites

    return invite_list



if __name__ == "__main__":
    friends={
        ##
    }
    print(invite_to_dinner_slow(friends))
    print(invite_to_dinner_better(friends))
    print(invite_to_dinner_optimized(friends))

    
    friends_2={
        ##
    }
    print(invite_to_dinner_slow(friends_2))
    print(invite_to_dinner_better(friends_2))
    print(invite_to_dinner_optimized(friends_2))

    friends_3={
        ##
    }
    print(invite_to_dinner_slow(friends_3))
    print(invite_to_dinner_better(friends_3))
    print(invite_to_dinner_optimized(friends_3))
    
