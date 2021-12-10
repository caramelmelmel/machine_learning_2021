#self-reminder
# y are the labels
# x is the words

# y -> x
# Output: dictionary of form {'label', {'word1': count of word1 in this label, ...}}
# label to word individual count
def count_tag_words(training_set):
    label_to_indiv_word_count ={'O':{},
    'B-positive':{},
    'B-neutral':{},
    'B-negative':{},
    'I-positive':{},
    'I-neutral':{},
    'I-negative':{}}
    for tag_word_pair in training_set:
        #label
        label = tag_word_pair[1]
        #word
        word = tag_word_pair[0]
        if word not in label_to_indiv_word_count[label].keys():
            label_to_indiv_word_count[label][word] = 1
        else:
            label_to_indiv_word_count[label][word] += 1
    return label_to_indiv_word_count

# count labels in training set
def count_labels(training_set):
    label_count ={'O':0,
        'B-positive':0,
        'B-neutral':0,
        'B-negative':0,
        'I-positive':0,
        'I-neutral':0,
        'I-negative':0}
    for label_word_pair in training_set:
        label = label_word_pair[1]
        label_count[label] += 1
    return label_count

#estimates the emission for each word and label
#output: {label:{word:count}}
def estimate_emission_parameters(counted_tags,counted_tag_words):
    all_estimations = {}
    for tag, word_count_dict in counted_tag_words.items():
        if tag not in all_estimations.keys():
            all_estimations[tag] = {}
        for word, count in word_count_dict.items():
            if word not in all_estimations[tag].keys():
                all_estimations[tag][word] = count/counted_tags[tag]
    return all_estimations


    
    

