import os

## Contains utilities (data reading, counting, data writing) shared by all of the parts.

## TODO: see if we still need, if not we can delete
#Outputs list (size n) of list (size 2) in this form: ['word', 'label']
def read_data(path):
  dataset = []
  f = open(path,"r", encoding="utf-8")
  training_set = f.readlines()
  for line in training_set:
    content_line = line.split() #split into the "text" and the "tag/label" using line.split()
    dataset.append(content_line) #append to the ES dataset
  #Remove empty lists within list
  Edataset = [ele for ele in dataset if ele != []]
  return Edataset

# e(x|y) = Count(y -> x)/Count(y)

## TODO: rename to read_train?
# FOR TRANSMISSION EDITED
# Used to read all training sets that are of form ['word' label']
# Outputs list (size n) of lists (size of each sentence) of lists (size 2) in the form: ['word', 'label']
def read_data_transmission(path):
  dataset = []
  f = open(path,"r", encoding="utf-8")
  training_set = f.readlines()
  for line in training_set:
    # if to include \n
    if len(line) == 1:
      dataset.append("\n")
    else:
      line = line.rstrip('\n')
      line = line.rpartition(' ')
      line = list(line)
      del line[1]
      if line != ['', '']:
        dataset.append(line)
  #Remove empty lists within list
  Edataset = [ele for ele in dataset]
  return Edataset

## TODO: see if we still need, if not we can delete
# Count(y)
# Output: dictionary of form {'label', 'count of this label in the dataset'}
def count_tags(training_set):
  unique_tag_count = {'O':0,'B-positive':0,'B-neutral':0,'B-negative':0,'I-positive':0,'I-neutral':0,'I-negative':0}
  #to store the unique tag + the total count of each from the training dataset
  for data_pair in training_set:
    if data_pair[1] in unique_tag_count.keys():
      unique_tag_count[data_pair[1]] += 1
  return unique_tag_count

## TODO: rename to count_tags?
# COUNT TAGS TRANSMISSION
# This is a modification of count_tags to also take into account the START/STOP states as indicated by new lines.
def count_tags_transmission(training_set):
  unique_tag_count = {'START':0,'O':0,'B-positive':0,'B-neutral':0,'B-negative':0,'I-positive':0,'I-neutral':0,'I-negative':0,'STOP':0}
  #to store the unique tag + the total count of each from the training dataset
  for data_pair in training_set:
    if len(data_pair) > 1:
      if data_pair[1] in unique_tag_count.keys():
        unique_tag_count[data_pair[1]] += 1
    elif len(data_pair)==1:
      unique_tag_count['START'] += 1 #for every newlin \n add to start and stop
      unique_tag_count['STOP'] += 1
  return unique_tag_count

# Count(y -> x)
# Output: dictionary of form {'label', {'word1': count of word1 in this label, ...}}
def count_tag_words(training_set):
  # We want to estimate the x given the ys
  # From the above code block we have count(y)
  label_generate_all = {'O':{},'B-positive':{},'B-neutral':{},'B-negative':{},'I-positive':{},'I-neutral':{},'I-negative':{}}
  for data in training_set:
    if len(data) > 1:
      try:
        if data[0] not in label_generate_all[data[1]].keys():
          label_generate_all[data[1]][data[0]] = 1
        else:
          label_generate_all[data[1]][data[0]] += 1 
      except KeyError:
        print("error", KeyError, data)
  return label_generate_all

## TODO: delete?
# Output: dictionary of
def estimate_transmission_parameters(count_tags, count_tag_words):
  all_estimations = {} #dictionary
  for unique_tag_tuple in count_tag_words.items():
    single_tag_estimation = {} #dictionary
    for word_count in unique_tag_tuple[1].items():
      estimated_value = word_count[1]/count_tags[unique_tag_tuple[0]] #this is the label y count
      single_tag_estimation[word_count[0]] = estimated_value
    all_estimations[unique_tag_tuple[0]] = single_tag_estimation
  return all_estimations

#pass in the file name as the string
def read_universal(file_name):
  return os.getcwd() + file_name

# Reads in the dev/test set (or any line-separated text file containing only words)
def read_dev(path):
  out = [[]]
  f = open(path, "r", encoding="utf-8")
  lines_in = f.readlines()
  for word in lines_in:
    if word == "\n":
      out.append([])
    else:
      out[-1].append(word.rstrip())
  return out[:-1]

# Generates a set of all the unique words encountered in the training set.
def get_training_set_words(data):
    words = set()
    for i in data:
        if len(data) > 1:
            words.add(i[0])
    return words
  
# Input: prediction, data (both are list of lists of strings), output path
# Each inner list represents a sentence and each element is a label (for prediction) or a word (data) respectively
# Writes the prediction into a path specified by the output path.
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