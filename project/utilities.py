import os
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

# FOR TRANSMISSION EDITED
def read_data_transmission(path):
  dataset = []
  f = open(path,"r", encoding="utf-8")
  training_set = f.readlines()
  for line in training_set:
    # if to include \n
    if len(line) == 1:
      dataset.append("\n")
    else:
      content_line = line.split() #split into the "text" and the "tag/label" using line.split()
      dataset.append(content_line) #append to the ES dataset
  #Remove empty lists within list
  Edataset = [ele for ele in dataset]
  return Edataset

# Count(y)
# Output: dictionary of form {'label', 'count of this label in the dataset'}
def count_tags(training_set):
  unique_tag_count = {'O':0,'B-positive':0,'B-neutral':0,'B-negative':0,'I-positive':0,'I-neutral':0,'I-negative':0}
  #to store the unique tag + the total count of each from the training dataset
  for data_pair in training_set:
    if data_pair[1] in unique_tag_count.keys():
      unique_tag_count[data_pair[1]] += 1
  return unique_tag_count

# COUNT TAGS TRANSMISSION
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
  
    