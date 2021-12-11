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

# Viterbi algorithm to predict output labels on each document.
# Note: should be called on EACH DOCUMENT of the VALIDATION/TEST set (data is a list of list containing strings)
# a(u,v) is t_params
# b(u,o) is e_params
def viterbi(data, t_params, e_params):
    n = len(data)
    # Includes only possible labels for the words in our dataset: ie. excludes 'START' and 'STP{}
    labels = ['O', 'B-positive', 'B-neutral', 'B-negative', 'I-positive', 'I-neutral', 'I-negative']

    # Initialization.
    # cache is a list, where the list index represents the current position in the data
    # each element consists of a dictionary of possible labels at that position
    #IMPORTANT
    # each possible label maps to a list of format [probability up to this point, parent label]
    # 0: START 1: 1st word ... n: nth word n+1: END --> size = n+2

    cache = [{'START':[0, None],
    'STOP': [0, None], 
    'O':[0, None],
    'B-positive':[0, None],
    'B-neutral':[0, None],
    'B-negative':[0, None],
    'I-positive':[0, None],
    'I-neutral':[0, None],
    'I-negative':[0, None]} for i in range(n+2)]

    cache[0]['START'][0] = 1
    # 1st step from 'START' to first label - there is only 1 label that meets this condition and only 1 path for this step.
    for label, prob in t_params['START'].items():
        if prob > 0:
            cache[1][label][0] = 1
            cache[1][label][1] = 'START'
            break

    # 0th value of the cache is the START token, but the 0th value of the dataset is the 1st word.
    # the START token is not part of the dataset - so we iterate until n+1.
    # ie. from 1 to n instead of 0 to n-1.
    for j in range(1, n):
        next_word = data[j]
        # Iterate over all of the current labels in this step.
        for u in labels:
            maximum = -sys.float_info.max
            max_label = ''
            # Because we want to find the maximum v
            for v in labels:
                # print("transmission from", v, "to", u)
                # If any of the observed probabilities are 0, we should skip because that is an impossible path
                if (cache[j][v][0] == 0 or t_params[v][u] == 0):
                    # print(v, "to", u, "is impossible")
                    continue
                prev_cached_value = cache[j][v][0]
                # print('now logging cache', cache[j][u][0], t_params[v][u])
                if next_word not in e_params[u].keys():
                    # print("the next word is not in our dictionary. using the #UNK# probability")
                    emission_prob = math.log(e_params[u]['#UNK#'])
                else:
                    # print("word in our dictionary")
                    emission_prob = math.log(e_params[u][next_word])
                transmission_prob = math.log(t_params[v][u])
                prob = prev_cached_value + emission_prob + transmission_prob
                # print(v, 'to', u, 'word:', next_word, 'has prob', prob)
                if maximum < prob:
                    maximum = prob
                    max_label = v
                
            cache[j+1][u][0] = math.exp(maximum)
            cache[j+1][u][1] = max_label
    
    # Final Step (n+1)
    maximum = -sys.float_info.max
    max_label = ''
    for v in labels:
        prev_cached_value = cache[n][v][0]
        transmission_prob = t_params[v]['STOP']
        if (prev_cached_value == 0 or transmission_prob == 0):
            continue
        prob = math.log(prev_cached_value) + math.log(transmission_prob)
        if maximum < prob:
            maximum = prob
            max_label = v

    cache[n+1]['STOP'][0] = math.exp(maximum)
    cache[n+1]['STOP'][1] = max_label

    # for i in range(len(cache)):
    #     print(i, cache[i])
    # print('\n')
    
    # Finding the most probable labels.
    output = ['' for i in range(n)]
    # for the nth word
    output[n-1] = max_label
    # for the n-1th to 1st word
    for j in range(n, 1, -1):
        # print("step", j, "old max:", max_label, "in cache:", cache[j])
        max_label = cache[j][max_label][1]
        output[j-2] = max_label
    
    return output

def viterbi_loop(separated, t_params, e_params):
    final = []
    for doc in separated:
        final.append(viterbi(doc, t_params, e_params))
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
es_dev = utilities.read_dev(r"ES\dev.in")
# print(es_dev)
# separated = separate_documents(es_train)
tags = utilities.count_tags_transmission(es_train)
tag_words = utilities.count_tag_words(es_train)
transmission_counts = count_transmissions(es_train)
t_params = estimate_transmission_parameters(transmission_counts, tags)
e_params = estimate_emission_parameters_with_unk(tags, tag_words)

# ru_train = utilities.read_data_transmission(r"RU\train")

## Testing viterbi
# test = separated[0]
# output_sequence = viterbi(test, t_params, e_params)
# print('\n')
# print("ogiginal length", len(test))
# print('\n')
# print(test)
# print("output length", len(output_sequence))
# print('\n')
# print(output_sequence)

## Actual viterbi
prediction = viterbi_loop(es_dev, t_params, e_params)

## Output into dev.out
output_prediction(prediction, es_dev, r"ES\dev.p2.out")