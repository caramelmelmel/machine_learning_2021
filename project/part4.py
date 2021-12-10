#Improved sentiment analysis model
import utilities
import string
import sys

# Generate a list of stopwords
# Use lemmization
# Remove stop words, in ES and RU
# Take out all of the stop words and label it as O, which indicates that they are outside
# https://github.com/Alir3z4/stop-words/blob/master/spanish.txt
def read_stopwords(stopwords_path):
    stopwords_list = []
    f = open(stopwords_path,"r", encoding="utf-8")
    stopwords_set = f.readlines()
    for line in stopwords_set:
        line2 = line.strip("\n")
        stopwords_list.append(line2)
    #Remove empty lists within list
    stop_words = [ele for ele in stopwords_list if ele != []]
    return stop_words

def remove_stopwords_es(dataset_spanyol, stop_words_list, symbols_list=[]): #input the spanish dataset here, default empty symbols
  original_dataset = []
  f = open(dataset_spanyol,"r", encoding="utf-8")
  training_set = f.readlines()
  for line in training_set:
    # if to include \n
    if len(line) == 1:
      original_dataset.append("\n")
    else:
      content_line = line.split() #split into the "text" and the "tag/label" using line.split()
      if content_line[0] in stop_words_list: #if the word belongs to the list of stopwords or list of symbols, assign the label O
          content_line[1] = "O" #assign label O
          original_dataset.append(content_line) #append to the ES dataset
      elif content_line[0] in symbols_list:
          continue
          #print(content_line[0])
  #Remove empty lists within list
  Edataset = [ele for ele in original_dataset]
  return Edataset

def get_symbols(edataset): #to get all of the symbols
    symbol_set=[]
    for element in edataset:
        #print(element)
        if element[0][0].isalnum() == False and element[0] not in symbol_set: #if it is not an alphabet
            symbol_set.append(element[0])
    return symbol_set

# Russian Alphabet
# АаБбВвГгДдЕеЁёЖжЗзИиЙйКкЛлМмНнОоПпРрСсТтУуФфХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯя

# Russian Stopwords
# Remove symbols as well, using the stopwords method
# Spanish Stopwords, strip from the dataset????
# Not suitable for this use case since we are removing entries from the dev.in and dev.out
# https://github.com/stopwords-iso/stopwords-es
# https://www.ranks.nl/stopwords/spanish
# Use a different algorithm, perhaps Naive Bayes Algorithm

# Naive Bayes Algorithm
stopwordsES = read_stopwords("stopwords_ES.txt")

modif = remove_stopwords_es(r"ES\train",stopwordsES) #remove all stopwords
print(modif)

tags = utilities.count_tags_transmission(modif)
print(sum(tags.values()))

stopwordsRU = read_stopwords("stopwords_RU.txt")
modif_RU = remove_stopwords_es(r"RU\train",stopwordsRU)
tags_ru = utilities.count_tags_transmission(modif_RU)
print(modif_RU)
print(get_symbols(modif_RU))
#print(string.printable)
#print(tags_ru)
#print(stopwordsRU)
# Label Smoothing

"""
# https://github.com/ongkahyuan/ML-project/blob/main/part5.py
# Smoothing Emission Parameters (EDIT THIS) EDIT EDIT EDIT EDIT EDIT
def set_emission_dict(self, emission_dict):
        self.emission_dict = emission_dict

def __smooth_emission_params(self):
        generates emission parameters based on training data, saves it as self.e_x_given_y
        params_count = {}
        unique_symbols = []
        for key, value in self.emission_dict.items():
            if key[0] not in unique_symbols:
                unique_symbols.append(key[0])
        
        n = len(unique_symbols)
        # n refers to the number of observations/symbols 

        for state in self.states:
            params_count[state] = [0,0,0]
            # print(params_count[state])
            # key is the state, value is list [total no. of symbols, total no. of non-zero probability, probability p]
            # i.e. [Ts, v, p]
            for key, value in self.emission_dict.items():
                if state in key:
                    params_count[state][0] += 1
                    if value != 0:
                        params_count[state][1] += 1
                    else:
                        continue
                    params_count[state][2] += 1/(params_count[state][0] + params_count[state][1])
                # p = 1/(Ts+v)
        
        for state in self.states:
            for key, value in self.emission_dict.items():
                if state in key:
                    if value != 0:
                        self.emission_dict[key] = value - params_count[state][2]
                    else:
                        self.emission_dict[key] = (params_count[state][2]*params_count[state][2])/n-params_count[state][2]
                        # v*p/n-v

def get_smooth_emission_params(self):
        self.__smooth_emission_params()
        return self.emission_dict
"""