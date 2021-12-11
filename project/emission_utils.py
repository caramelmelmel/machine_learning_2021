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
        #print(label_word_pair)
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

#call for ES and RU
# Output: dictionary of form {'label': {'word1': probability that word1 is label1, ...}}
#Outputs list (size n) of list (size 2) in this form: ['word', 'label'] read_data fn

def split_labels_test(path):
  dataset = []
  f = open(path,"r")
  training_set = f.readlines()
  for line in training_set:
    dataset.append(line) #append to the ES dataset
  #Remove empty lists within list
  Edataset = [ele for ele in dataset if ele != []]
  returned_ls = []
  for element in Edataset:
    returned_ls.append(element.rstrip("\n"))
  returned_ls = returned_ls[:-1]
  return returned_ls

def emission_probability_unk(unk,train,k=1):
  emission_dict = {}
  for label in train.keys():
    count_y = 0
    word_dict = train[label]
    for word_count in word_dict.values():
      count_y += word_count

    #keep track of whether or not in the training set
    count_y_to_x = 0
    for word in unk[label].keys():
      estimation_x = k/(count_y + k)
      emission_dict[label]['#UNK#'] = estimation_x

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
    

#read the dev.in and the dev.out files properly
#for testing
#compare word probablity
def test_emission(word_probabilities_label,word_file):
  word_probabilities = {}
  word_label = {}

  dev_inputs = open(word_file,'r')
  lines_in = dev_inputs.readlines()
  for word in lines_in:
      word = word.rstrip()
    #initialise
      if word not in word_probabilities:
        word_probabilities[word] = 0

      for label, word_prob_dict in word_probabilities_label.items():
        if word not in word_prob_dict.keys():
          probability = word_prob_dict['#UNK#']
        else:
          probability = word_prob_dict[word]

        if word_probabilities[word] < probability:
          word_label[word] = label
          word_probabilities[word] = probability
      
  return word_label

def write_out(write_file_path,prediction_dict,input_file):
    write_file = open(write_file_path,'w')
    input_f = open(input_file,'r')
    input_lines = input_f.readlines()
    for line in input_lines:
        line = line.rstrip()
        if len(line) > 0:
            label = prediction_dict[line]
            write_file.write(f'{line} {label}\n')
        else:
            write_file.write('\n')