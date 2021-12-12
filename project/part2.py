import utilities
import math
import sys
import part1

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

    for j in range(0, n):
        next_word = data[j]
        # print("\n\n Step", j+1, "current word is:", next_word)
        # Iterate over all of the current labels in this step.
        for u in labels:
            # print("\n Checking u: ", u)
            maximum = n_inf
            max_label = None
            # Because we want to find the maximum v
            for v in labels:
                # If any of the observed probabilities are 0, we should skip because that is an impossible path
                if (cache[j][v][0] == n_inf or t_params[v][u] == 0):
                    # print(v, "to", u, "is impossible")
                    continue
                prev_cached_value = cache[j][v][0]
                if next_word in word_set:
                    if next_word not in e_params[u].keys():
                        # print("impossible emission: word in training set yet not seen for this label.")
                        continue
                    else:
                        emission_prob = e_params[u][next_word]
                else:
                    # print("not in training set. using the #UNK# probability")
                    emission_prob = e_params[u]['#UNK#']
                transmission_prob = t_params[v][u]
                # print("cache:", prev_cached_value, "emiss:", emission_prob, "trans:", transmission_prob)
                prob = prev_cached_value + math.log(emission_prob) + math.log(transmission_prob)
                # print(v, 'to', u, 'emitting', next_word, 'has prob', prob)
                if maximum < prob:
                    maximum = prob
                    max_label = v
            
            # print('best v is', max_label, 'with prob', maximum)
            if maximum == n_inf:
                continue
            cache[j+1][u][0] = maximum
            cache[j+1][u][1] = max_label
    
    # Final Step (n+1)
    maximum = n_inf
    max_label = None
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
    
    # Finding the most probable labels.
    output = ['' for i in range(n)]

    # Default to "O" if emission isn't possible.
    if max_label == None:
        max_label = "O"

    # for the n-1th to 1st word
    for j in range(n+1, 1, -1):
        # print("step", j, "old max:", max_label, "in cache:", cache[j])
        max_label = cache[j][max_label][1]
        if max_label == None:
            max_label = "O"
        output[j-2] = max_label
    
    return output

def viterbi_loop(separated, t_params, e_params, word_set):
    final = []
    for doc in separated:
        final.append(viterbi(doc, t_params, e_params, word_set))
    return final


def run_viterbi(training_path, test_path, output_path):
    train = utilities.read_data(training_path)
    train_words = utilities.get_training_set_words(train)
    test = utilities.read_dev(test_path)
    tags = utilities.count_tags(train)
    tag_words = utilities.count_tag_words(train)
    transmission_counts = count_transmissions(train)
    t_params = estimate_transmission_parameters(transmission_counts, tags)
    e_params = part1.estimate_emission_parameters_with_unk(tags, tag_words)
    prediction = viterbi_loop(test, t_params, e_params, train_words)
    utilities.output_prediction(prediction, test, output_path)

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

## Actual viterbi calls
if __name__ == '__main__':
    n = len(sys.argv)

    if n == 1:
        run_viterbi(r"ES/train", r"ES/dev.in", r"ES/dev.p2.out")
        run_viterbi(r"RU/train", r"RU/dev.in", r"RU/dev.p2.out")
    else:
        if n == 4:
            run_viterbi(sys.argv[1], sys.argv[2], sys.argv[3])
        else:
            print("usage: python part2.py [train_path] [test_path] [output_path]")