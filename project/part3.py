# Modified Algorithm
# At each step of the viterbi aside from including a single parent, include top 5 parents
# Form 5 sequences corresponding to each different parent with some indexing
# Return the top 5 sequences
import utilities
import math
import sys
import part1
import part2

# Viterbi algorithm to predict output labels on each document.
# Note: should be called on EACH DOCUMENT of the VALIDATION/TEST set (data is a list of list containing strings)
# a(u,v) is t_params
# b(u,o) is e_params

def viterbi_5th(data, t_params, e_params, word_set):

    # print("Beginning viterbi for", data)
    n = len(data)
    # Includes only possible labels for the words in our dataset: ie. excludes 'START' and 'STOP'
    labels = ['O', 'B-positive', 'B-neutral', 'B-negative', 'I-positive', 'I-neutral', 'I-negative', 'START']

    # Initialization.
    # cache is a list, where the list index represents the current position in the data
    # each element consists of a dictionary of possible labels at that position
    #IMPORTANT
    # each possible label maps to a list of format [probability up to this point, parent label]
    # 0: START 1: 1st word ... n: nth word n+1: END --> size = n+2
    """
    n_inf = -math.inf
    cache = [[{'START':[n_inf, None], #store 1st, 2nd, 3rd, 4th, 5th maximum path
    'STOP': [n_inf, None], 
    'O':[n_inf, None],
    'B-positive':[n_inf, None],
    'B-neutral':[n_inf, None],
    'B-negative':[n_inf, None],
    'I-positive':[n_inf, None],
    'I-neutral':[n_inf, None],
    'I-negative':[n_inf, None]} for i in range(n+2)]
    for i in range(5)]
    """

    # DIFFERENT APPROACH
    n_inf = -math.inf
    cache = [{'START':[n_inf, None],
    'STOP': [n_inf, None], 
    'O':[n_inf, None],
    'B-positive':[n_inf, None],
    'B-neutral':[n_inf, None],
    'B-negative':[n_inf, None],
    'I-positive':[n_inf, None],
    'I-neutral':[n_inf, None],
    'I-negative':[n_inf, None]} for i in range(n+2)]

    cache[0]['START'][0] = 0 # Technically this should be 0

    #for i in range(5):
    #    print(i)
    #    print(cache)
    #quit()

# USE ANOTHER APPROACH KEEP A LIST OF 5 PARENTS IN EACH OF THE 
    #use a global list/heap to store all possible VITERBI scores for all the paths
    # global list of sequences, sequence score and keep all the parents up to that state # Separate List
    # Sequence will be START all the labels and then STOP
    all_viterbi_list = [
        [n_inf,['START']]
    ] #its the VITERBI score followed by the SEQUENCE/PATH
    # uses a sorted list, every time we got something append to the maximum list, sort it, then cut it to 5 

    for j in range(0, n):
        next_word = data[j]
        # print("\n\n Step", j+1, "current word is:", next_word)
        # Iterate over all of the current labels in this step.
        for u in labels:
            # print("\n Checking u: ", u)
            maximum = n_inf
            max_label = None #store 5 max labels
            # Because we want to find the maximum v
            for v in labels: # FOR EACH OF THE PREVIOUS STATE/LABELS
                # If any of the observed probabilities OF PREVIOUS STATE IS  0, we should skip because that is an impossible path
                if (cache[j][v][0] == n_inf or t_params[v][u] == 0):
                    # print(v, "to", u, "is impossible")
                    continue
                prev_cached_value = cache[j][v][0]
                if next_word in word_set:
                    if next_word not in e_params[u].keys(): #if word is in training set and not in emission
                        # print("impossible emission: word in training set yet not seen for this label.")
                        continue
                    else:
                        emission_prob = e_params[u][next_word]
                else:
                    # print("not in training set. using the #UNK# probability")
                    emission_prob = e_params[u]['#UNK#']
                transmission_prob = t_params[v][u]
                # print("cache:", prev_cached_value, "emiss:", emission_prob, "trans:", transmission_prob)
                # COUNT PROBABILITY OF PREVIOUS CACHE CALC
                prob = prev_cached_value + math.log(emission_prob) + math.log(transmission_prob)
                # print(v, 'to', u, 'emitting', next_word, 'has prob', prob)
                if maximum < prob: #IF THE MAX IS SMALLER and max labels still has 5 slots to fill
                    maximum = prob 
                    max_label = v
                
                # Adding prob, sequence to the global viterbi list
                sequence = all_viterbi_list[0][1]
                if len(sequence) == j+1: # J = 0 is step 1, where in step 1 the sequence will only include START, length 1
                    sequence.append(u) # 'O', 'u'
                elif len(sequence) > j+1:
                    sequence[-1] = u
                else:
                    raise Exception("The sequence length is too short")

                all_viterbi_list.append([prob, sequence])

                # reorder and strip off the ends:
                # https://www.geeksforgeeks.org/python-program-to-sort-a-list-of-tuples-by-second-item/
                all_viterbi_list.sort(key = lambda x: float(x[0]),reverse=True) #sort based on probability values
                if len(all_viterbi_list)>5: #IF MORE THAN 5 ENTRIES IN MAX LABELS THEN CHOP OFF
                    all_viterbi_list = all_viterbi_list[:5] #chop off until 5 elements remain, DELETE ALL AFTER INDEX 5
                #print(max_labels)

            # print('best v is', max_label, 'with prob', maximum)
            if maximum == n_inf:
                continue
            cache[j+1][u][0] = maximum
            cache[j+1][u][1] = max_label
    # print(len(cache))

    # Final Step (n+1)
    maximum = n_inf
    max_label = None
    for v in labels:
        prev_cached_value = cache[n][v][0]
        # print(cache[n][v][0]) #the MAX value(index 0)
        transmission_prob = t_params[v]['STOP']
        # print(t_params[v]['STOP'])
        if (prev_cached_value == 0 or transmission_prob == 0):
            continue
        prob = prev_cached_value + math.log(transmission_prob)
        # print(prob)
        if maximum < prob:
            maximum = prob
            max_label = v

        # AT LAST STEP THE SEQUENCE WILL HAVE LENGTH OF N + 2
        # WE ONLY APPEND IF THE SEQUENCE IS ONE LESS THAN THE MAXIMUM
        print("n", n)
        sequence = all_viterbi_list[0][1]
        # just append Os until you reach the LENGTH
        if len(sequence) == n+2: # J = 0 is step 1, where in step 1 the sequence will only include START, length 1
            sequence.append('STOP') # 'O', 'u'
        elif len(sequence) > n+2:
            sequence[-1] = 'STOP'
        else: #ONLY FOR THIS CASE - NEED TO EXTEND ALL BEST SEQUENCES
            sequence = sequence + ['O']*(n+1 - len(sequence)) + ["STOP"] #add Os until it reach the length and ensure the last thing is STOP
            print("seqlen", len(sequence))

        all_viterbi_list.append([prob, sequence])

        all_viterbi_list.sort(key = lambda x: float(x[0]),reverse=True) #sort based on probability values
        if len(all_viterbi_list)>5: #IF MORE THAN 5 ENTRIES IN MAX LABELS THEN CHOP OFF
            all_viterbi_list = all_viterbi_list[:5]
        # print(all_viterbi_list)
        
    output = all_viterbi_list[4][1] #5TH BEST OUTPUT SEQUENCE
    if len(output) < n+2:
        output = output + ['O']*(n+1 - len(output)) + ["STOP"]
    
    return output[1:-1] #access the 5TH BEST sequence

def viterbi_loop_5th(separated, t_params, e_params, word_set):
    final = []
    for doc in separated:
        final.append(viterbi_5th(doc, t_params, e_params, word_set))
    return final

def run_viterbi_5th(training_path, test_path, output_path):
    train = utilities.read_data_transmission(training_path)
    train_words = utilities.get_training_set_words(train)
    test = utilities.read_dev(test_path)
    tags = utilities.count_tags_transmission(train)
    tag_words = utilities.count_tag_words(train)
    transmission_counts = part2.count_transmissions(train)
    t_params =  part2.estimate_transmission_parameters(transmission_counts, tags)
    e_params = part1.estimate_emission_parameters_with_unk(tags, tag_words)
    prediction = viterbi_loop_5th(test, t_params, e_params, train_words)
    utilities.output_prediction(prediction, test, output_path)


## Actual viterbi calls
if __name__ == '__main__':
    n = len(sys.argv)

    if n == 1:
        run_viterbi_5th(r"ES/train", r"ES/dev.in", r"ES/dev.p3.out")
        run_viterbi_5th(r"RU/train", r"RU/dev.in", r"RU/dev.p3.out")
    else:
        if n == 4:
            run_viterbi_5th(sys.argv[1], sys.argv[2], sys.argv[3])
        else:
            print("usage: python part3.py [train_path] [test_path] [output_path]")

## Actual running code
#Outputs list (size n) of list (size 2) in this form: ['word', 'label']
# es_train = utilities.read_data_transmission(r"ES\train")
# train_words = get_training_set_words(es_train)
# es_dev = utilities.read_dev(r"ES\dev.in")
# # print(es_dev)
# # separated = separate_documents(es_train)
# tags = utilities.count_tags_transmission(es_train)
# tag_words = utilities.count_tag_words(es_train)
# transmission_counts = count_transmissions(es_train)
# t_params = estimate_transmission_parameters(transmission_counts, tags)
# e_params = estimate_emission_parameters_with_unk(tags, tag_words)

# file = open("e_params", "w", encoding="utf-8")
# file.write(str(e_params))

# ru_train = utilities.read_data_transmission(r"RU\train")

# # Testing viterbi
# test = ['Con', 'lo', 'cual', 'en', 'el', 'comedor', 'tienes', 'que', 'levantar', 'mas', 'la', 'voz', 
# 'para', 'oirte', 'y', 'se', 'forma', 'un', 'ambiente', 'que', 'no', 'lo', 'que', 'se', 'espera', 'de', 'una', 'estrella', 'michelin', '.']
# output_sequence = viterbi(test, t_params, e_params, train_words)
# print('\n')
# print(output_sequence)
# print(len(test))
# print(len(output_sequence))
## Actual viterbi
# prediction = viterbi_loop(es_dev, t_params, e_params, train_words)

## Output into dev.out
# output_prediction(prediction, es_dev, r"ES\dev.p2.out")
