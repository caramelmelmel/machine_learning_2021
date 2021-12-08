import utilities
import math

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
    transmission_prob = {'START':{}, 'O':{},'B-positive':{},'B-neutral':{},'B-negative':{},'I-positive':{},'I-neutral':{},'I-negative':{}}
    for label in transmission_prob.keys():
        transmission_prob[label] = {'O':0,'B-positive':0,'B-neutral':0,'B-negative':0,'I-positive':0,'I-neutral':0,'I-negative':0, 'STOP':0}
    for label_in, t_counts in transmission_count.items():
        if label_in != 'START':
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

# def logarify(dict):
#     out = {}
#     for key, inner_dict in dict.items():
#         out[key] = inner_dict
#         print(inner_dict)
#         for inner_key, value in inner_dict.items():
#             out[key][inner_key] = math.log(value)
            
#     return out

# Viterbi algorithm
# a(u,v) is t_params
# b(u,o) is e_params
def viterbi(data, t_params, e_params):
    n = len(data)
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
    print(cache)

    # 0th value of the cache is the START token, but the 0th value of the dataset is the 1st word.
    # the START token is not part of the dataset - so we iterate until n+1.
    for j in range(1, n):
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
    
    # Final Step
    maximum = 0
    max_label = ''
    print(cache)
    for v in labels:
        prev_cached_value = cache[n][u][0]
        transmission_prob = t_params[v]['STOP']
        prob = prev_cached_value * transmission_prob
        if maximum < prob:
            maximum = prob
            max_label = u
    cache[n+1]['STOP'][0] = maximum
    cache[n+1]['STOP'][1] = max_label
    
    # Finding the most probable labels.
    output = ['' for i in range(n)]
    # for the case n (nth word)
    output[n-1] = max_label
    # for the case n-1 until case 1 (1st word)
    for j in range(n-1, 0, -1):
        max_label = cache[j][max_label][1]
        output[j-1] = max_label
    
    return output


## Actual running code
#Outputs list (size n) of list (size 2) in this form: ['word', 'label']
es_train = utilities.read_data_transmission(r"ES\train")
tags = utilities.count_tags(es_train)
tag_words = utilities.count_tag_words(es_train)
transmission_counts = count_transmissions(es_train)
t_params = estimate_transmission_parameters(transmission_counts, tags)
e_params = estimate_emission_parameters_with_unk(tags, tag_words)

viterbi(es_train, t_params, e_params)