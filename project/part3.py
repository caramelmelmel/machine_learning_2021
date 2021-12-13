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

def get_5th_value(list, n):
    list.sort(key = lambda x: float(x[0]),reverse=True)

    if len(list) >= 5: 
        # Get 5th best output sequence
        output = list[4][1]
    else:
        # Get last output sequence if list is shorter than 5.
        output = list[-1][1]
    
    if len(output) < n+2:
        # Append 'O' as default value to be returned (as well as STOP)
        output = output + ['O']*(n+1 - len(output)) + ["STOP"]
    
    return output[1:-1]


def viterbi_5th(data, t_params, e_params, word_set):
    # print("Beginning viterbi for", data)
    n = len(data)
    # Includes only possible labels for the words in our dataset: ie. excludes 'START' and 'STOP'
    labels = ['O', 'B-positive', 'B-neutral', 'B-negative', 'I-positive', 'I-neutral', 'I-negative', 'START']

    # DIFFERENT APPROACH
    n_inf = -math.inf

# USE ANOTHER APPROACH KEEP A LIST OF 5 PARENTS IN EACH OF THE 
    #use a global list/heap to store all possible VITERBI scores for all the paths
    # global list of sequences, sequence score and keep all the parents up to that state # Separate List
    # Sequence will be START all the labels and then STOP
    all_viterbi_list = [
        [0,['START']]
    ] #the VITERBI score followed by the SEQUENCE/PATH

    for j in range(0, n):
        next_word = data[j]
        current_sequences = []
        # print("\n\n Step", j+1, "current word is:", next_word)
        # Iterate over all of the current labels in this step.
        for u in labels:
            # print("\n Checking u: ", u)
            # Check only reachable paths to this currrent node.
            for path in all_viterbi_list:
                # print("label:", u, "& checking path:", path)
                v = path[1][-1]
                sequence = path[1][:]
                # If any of the observed probabilities OF PREVIOUS STATE IS  0, we should skip because that is an impossible path
                if (t_params[v][u] == 0):
                    # print(v, "to", u, "is impossible")
                    continue
                prev_cached_value = path[0]
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
                
                if prob != n_inf:
                    # Adding prob, sequence to the global viterbi list
                    if len(sequence) == j+1: # J = 0 is step 1, where in step 1 the sequence will only include START, length 1
                        sequence.append(u) # 'O', 'u'
                    else:
                        raise Exception("The sequence length is wrong.")
                    # print(v, 'to', u, 'emitting', next_word, 'has prob', prob, 'sequence:', sequence)
                    current_sequences.append([prob, sequence[:]])

        # If at this point current_sequences is empty, there are no more viable paths to this step.
        # We can terminate the algorithm early.
        # We return the 5th longest sequence from the previous step.
        if len(current_sequences) == 0:
            return get_5th_value(all_viterbi_list, n)
        
        # Set all viterbi list to the list of the current sequences.
        all_viterbi_list = current_sequences[:]

        # Only keep top k number of paths to reduce computation time.
        k = 50
        if len(all_viterbi_list)>k:
            all_viterbi_list.sort(key = lambda x: float(x[0]),reverse=True)
            all_viterbi_list = all_viterbi_list[:k]

    # Final Step (n+1)
    current_sequences = []
    # print("\n\n FINAL STEP ")
    for path in all_viterbi_list:
        # print("checking path:", path)
        v = path[1][-1]
        sequence = path[1][:]
        transmission_prob = t_params[v]['STOP']
        prev_cached_value = path[0]
        if (transmission_prob == 0):
            continue
        prob = prev_cached_value + math.log(transmission_prob)

        # AT LAST STEP THE SEQUENCE WILL HAVE LENGTH OF N + 2
        # WE ONLY APPEND IF THE SEQUENCE IS ONE LESS THAN THE MAXIMUM
        # print("n", n)
        # just append Os until you reach the LENGTH
        if prob != n_inf:
            if len(sequence) == n+2: # J = 0 is step 1, where in step 1 the sequence will only include START, length 1
                sequence.append('STOP') # 'O', 'u'
            elif len(sequence) > n+2:
                sequence[-1] = 'STOP'
            else: #ONLY FOR THIS CASE - NEED TO EXTEND ALL BEST SEQUENCES
                sequence = sequence + ['O']*(n+1 - len(sequence)) + ["STOP"] #add Os until it reach the length and ensure the last thing is STOP
                # print("seqlen", len(sequence))

        current_sequences.append([prob, sequence[:]])

    return get_5th_value(current_sequences, n)

def viterbi_loop_5th(separated, t_params, e_params, word_set):
    final = []
    for doc in separated:
        final.append(viterbi_5th(doc, t_params, e_params, word_set))
    return final

def run_viterbi_5th(training_path, test_path, output_path):
    train = utilities.read_data(training_path)
    train_words = utilities.get_training_set_words(train)
    test = utilities.read_dev(test_path)
    tags = utilities.count_tags(train)
    tag_words = utilities.count_tag_words(train)
    transmission_counts = part2.count_transmissions(train)
    t_params =  part2.estimate_transmission_parameters(transmission_counts, tags)
    e_params = part1.estimate_emission_parameters_with_unk(tags, tag_words)
    prediction = viterbi_loop_5th(test, t_params, e_params, train_words)
    utilities.output_prediction(prediction, test, output_path)


# Actual viterbi calls
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