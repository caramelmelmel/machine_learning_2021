# Modified Algorithm
# At each step of the viterbi aside from including a single parent, include top 5 parents
# Form 5 sequences corresponding to each different parent with some indexing
# Return the top 5 sequences
"""
cache = [{'START':[0, []], => convert from None, to an empty list/dictionary to store multiple entries, with dictionary we can use the orders 1st 2nd 3rd 4th 5th as the keys
    'STOP': [0, []], 
    'O':[0, None],
    'B-positive':[0, None],
    'B-neutral':[0, None],
    'B-negative':[0, None],
    'I-positive':[0, None],
    'I-neutral':[0, None],
    'I-negative':[0, None]} for i in range(n+2)]

In each iteration
for j in range(1, n):
        for every one node
        add a list/dictionary = [], append each of the calculater probabilities to this list, then in the end reorder/arrange from max to min and take the 5th index
        find top 5 from the collected list
        
        next_word = data[j][0]
        for u in labels:
            maximum = -999
            max_label = ''
            for v in labels:
                # If any of the observed probabilities are 0, we should skip because that is an impossible path
                if (cache[j][u][0] == 0) or (t_params[v][u] == 0):
                    continue
                
                # print('now logging cache', cache[j][u][0], t_params[v][u])
                prev_cached_value = cache[j][u][0]
                if next_word not in e_params[u].keys():
                    emission_prob = math.log(e_params[u]['#UNK#'])
                else:
                    emission_prob = math.log(e_params[u][next_word])
                transmission_prob = math.log(t_params[v][u])
                prob = prev_cached_value + emission_prob + transmission_prob
                # print(u, 'to', v, 'word:', next_word, 'has prob', prob)
                if maximum < prob:
                    maximum = prob
                    max_label = u

            cache[j+1][u][0] = maximum
            cache[j+1][u][1] = max_label

"""