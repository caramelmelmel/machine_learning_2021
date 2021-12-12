# Modified Algorithm
# At each step of the viterbi aside from including a single parent, include top 5 parents
# Form 5 sequences corresponding to each different parent with some indexing
# Return the top 5 sequences
import utilities
import math
import sys

## This is code to obtain the transmission parameters

# Outputs a dictionary {'label1': {'label1': count of label1->label1, 'label2': count of label1->label2...}...}
def count_transmissions(data):
    transmissions = {'START':{}, 'O':{},'B-positive':{},'B-neutral':{},'B-negative':{},'I-positive':{},'I-neutral':{},'I-negative':{}}
    for label in transmissions.keys():
        transmissions[label] = {'O':0,'B-positive':0,'B-neutral':0,'B-negative':0,'I-positive':0,'I-neutral':0,'I-negative':0, 'STOP':0}
    last_position = 'START'
    for line in data:
        if line =="\n": #if line is a slash n - need to concern, rewrite processing script to include \n
            transmissions[last_position]["STOP"] += 1 #add transmission from last read label to STOP state
            last_position = 'START' #reset state back to start
        else:
            transmissions[last_position][line[1]] += 1 #for transmission from the Label/State at LAST POSITION to the state read from the line
            last_position = line[1] #move/transit to the next state read from the line
    #transmissions[last_position]['STOP'] += 1 #add +1 for each transmission from label/state read to STOP
    return transmissions

# Outputs a dictionary {'label1': {'label1': probability of label1->label1, 'label2': probability of label1->label2...}...}
def estimate_transmission_parameters(transmission_count, tags_count):
    transmission_prob = {'START':{}, 'O':{},'B-positive':{},'B-neutral':{},'B-negative':{},'I-positive':{},'I-neutral':{},'I-negative':{},'STOP':{}}
    for label in transmission_prob.keys():
        transmission_prob[label] = {'START':0,'O':0,'B-positive':0,'B-neutral':0,'B-negative':0,'I-positive':0,'I-neutral':0,'I-negative':0, 'STOP':0}
    for label_in, t_counts in transmission_count.items():
        for label_out, count in t_counts.items():
            transmission_prob[label_in][label_out] = count/tags_count[label_in]
    """
    #Special Cases
    for first_label, start_count in transmission_count['START'].items():
        if start_count > 0:
            transmission_prob['START'][first_label] = 1
    """
    return transmission_prob

def estimate_emission_parameters_with_unk(count_tags, count_tag_words,k=1):
  all_estimations = {} #dictionary
  for unique_tag_tuple in count_tag_words.items():
    single_tag_estimation = {} #dictionary
    for word_count in unique_tag_tuple[1].items():
      estimated_value = word_count[1]/(count_tags[unique_tag_tuple[0]] + k) #this is the label y count
      single_tag_estimation[word_count[0]] = estimated_value
    single_tag_estimation['#UNK#'] = k/(count_tags[unique_tag_tuple[0]] + k)
    all_estimations[unique_tag_tuple[0]] = single_tag_estimation
  return all_estimations

# Input: list of lists containing word, label, with "\n" delimiting new lines. Output of read_data_transmission.
# Output: list of documents (which are lists containing word, label). 3-layer listing.
def separate_documents(data):
    out = [[]]
    for i in data:
        if i == '\n':
            out.append([])
        else:
            out[-1].append(i)

    # To get rid of the last empty array
    return out[:-1]

def get_training_set_words(data):
    words = set()
    for i in data:
        if len(data) > 1:
            words.add(i[0])
    return words

# Viterbi algorithm to predict output labels on each document.
# Note: should be called on EACH DOCUMENT of the VALIDATION/TEST set (data is a list of list containing strings)
# a(u,v) is t_params
# b(u,o) is e_params

def viterbi(data, t_params, e_params, word_set):

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
    cache = [{'START':[n_inf, [None,None,None,None,None]],
    'STOP': [n_inf, [None,None,None,None,None]], 
    'O':[n_inf, [None,None,None,None,None]],
    'B-positive':[n_inf, [None,None,None,None,None]],
    'B-neutral':[n_inf, [None,None,None,None,None]],
    'B-negative':[n_inf, [None,None,None,None,None]],
    'I-positive':[n_inf, [None,None,None,None,None]],
    'I-neutral':[n_inf, [None,None,None,None,None]],
    'I-negative':[n_inf, [None,None,None,None,None]]} for i in range(n+2)]

    cache[0]['START'][0] = 0 # Technically this should be 0

    #for i in range(5):
    #    print(i)
    #    print(cache)
    #quit()

# USE ANOTHER APPROACH KEEP A LIST OF 5 PARENTS IN EACH OF THE 

    for j in range(0, n):
        next_word = data[j]
        # print("\n\n Step", j+1, "current word is:", next_word)
        # Iterate over all of the current labels in this step.
        for u in labels:
            max_labels =[] #for each STATE thEre is a list of top 5 POSSIBLE STATES, EDIT

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
                # ADD ENTRY TO LIST O
                max_labels.append((max_label, prob))

                # reorder and strip off the ends:
                # https://www.geeksforgeeks.org/python-program-to-sort-a-list-of-tuples-by-second-item/
                max_labels.sort(key = lambda x: x[1]) #sort based on probability values
                if len(max_labels)>5: #IF MORE THAN 5 ENTRIES IN MAX LABELS THEN CHOP OFF
                    max_labels = max_labels[5:] #chop off until 5 elements remain, DELETE ALL AFTER INDEX 5
                #print(max_labels)

            # print('best v is', max_label, 'with prob', maximum)
            if maximum == n_inf:
                continue # DO NOTHING
            cache[j+1][u][0] = maximum #SET THE CACHE ENTRY TO MAXIMUM PROBABILITY
            #print(len(max_labels))
            for i in range(len(max_labels)):
                cache[j+1][u][1][i] = max_labels[i] #append 1st, 2nd, 3rd, 4th, 5th based on the i indexes
            print(max_labels)
        print(cache[j]) #edit
        #quit()
    #print(cache[k])
    
    

    """
    # Final Step (n+1)
    maximum = n_inf
    # EDIT
    max_labels = {}
    for v in labels:
        prev_cached_value = cache[n][v][0]
        transmission_prob = t_params[v]['STOP']
        if (prev_cached_value == 0 or transmission_prob == 0):
            continue
        prob = prev_cached_value + math.log(transmission_prob)
        if maximum < prob:
            maximum = prob
            max_label = v

    if maximum != n_inf:
        cache[n+1]['STOP'][0] = maximum
        cache[n+1]['STOP'][1] = max_label

    # for i in range(len(cache)):
    #     print(i, cache[i])
    # print('\n')
    
    # EDIT: FINDING THE TOP 5 MOST PROBABLY LABELS
    # Finding the most probable labels, use a list where each of them stores TOP 5 VALUES
    output = [['','','','',''] for i in range(n)]
    print(output)
    # Default to "O" if emission isn't possible.
    if max_label == None:
        max_label = "O"

    # for the n-1th to 1st word
    for j in range(n+1, 1, -1):
        # print("step", j, "old max:", max_label, "in cache:", cache[j])
        for element in cache[j].values():
            print(element)
        break
        max_label = cache[j][max_label][1]
        if max_label == None:
            max_label = "O"
        output[j-2] = max_label
    return output
    """

def viterbi_loop(separated, t_params, e_params, word_set):
    final = []
    for doc in separated:
        final.append(viterbi(doc, t_params, e_params, word_set))
    return final

# Input: dev_set (list of lists of strings)
def output_prediction(prediction, data, path):
    assert(len(prediction) == len(data))
    file = open(path, "w", encoding="utf-8")
    n = len(data)
    print("Writing", n, "lines")
    for i in range(n):
        assert(len(data[i]) == len(prediction[i]))
        m = len(data[i])
        for j in range(m):
            file.write(data[i][j] + " " + prediction[i][j] + "\n")
        file.write("\n")
    print("Wrote predictions to", path)


## Actual running code
#Outputs list (size n) of list (size 2) in this form: ['word', 'label']
es_train = utilities.read_data_transmission(r"ES\train")
train_words = get_training_set_words(es_train)
es_dev = utilities.read_dev(r"ES\dev.in")
# print(es_dev)
# separated = separate_documents(es_train)
tags = utilities.count_tags_transmission(es_train)
tag_words = utilities.count_tag_words(es_train)
transmission_counts = count_transmissions(es_train)
t_params = estimate_transmission_parameters(transmission_counts, tags)
e_params = estimate_emission_parameters_with_unk(tags, tag_words)

# file = open("e_params", "w", encoding="utf-8")
# file.write(str(e_params))

# ru_train = utilities.read_data_transmission(r"RU\train")

# # Testing viterbi
# test = ['Con', 'lo', 'cual', 'en', 'el', 'comedor', 'tienes', 'que', 'levantar', 'mas', 'la', 'voz', 
# 'para', 'oirte', 'y', 'se', 'forma', 'un', 'ambiente', 'que', 'no', 'lo', 'que', 'se', 'espera', 'de', 'una', 'estrella', 'michelin', '.']
# output_sequence = viterbi(test, t_params, e_params, train_words)
# # print('\n')
# # print("ogiginal length", len(test))
# # print('\n')
# # print(test)
# # print("output length", len(output_sequence))
# print('\n')
# print(output_sequence)

## Actual viterbi
prediction = viterbi_loop(es_dev, t_params, e_params, train_words)

## Output into dev.out
output_prediction(prediction, es_dev, r"ES\dev.p2.out")
