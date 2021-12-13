from copy_utilities import read_universal_
import utilities
import part2
import part1
import os 
import numpy as np
import sys

#import all file paths
#common words are stop words for each language
STOP_words_ES_file_path = read_universal_('stopwords_ES.txt','ES')
STOP_words_RU_file_path = read_universal_('stopwords_RU.txt','RU')

#training path 
RU_train = read_universal_('train','RU')
ES_train = read_universal_('train','ES')

# test file path dev set
RU_test_dev = read_universal_('dev.in','RU')
ES_test_dev = read_universal_('dev.in','ES')

# write out file path (for dev ones)
RU_test_dev_write = read_universal_('dev.p4.out','RU')
ES_test_dev_write = read_universal_('dev.p4.out','ES')

#write for test set portion 2 
RU_test = read_universal_('test.in','test/RU-test')
ES_test = read_universal_('test.in','test/ES-test')

# write for the test portion
RU_test_write = read_universal_('test.p4.out','RU')
ES_test_write = read_universal_('test.p4.out','ES')

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

#remove all the russian and spanish stopwords
def remove_stopwords(dataset,stop_words,symbols_list=[]):
    original_dataset = []
    file_dataset = open(dataset,'r',encoding='utf-8')
    training_set = file_dataset.readlines()
    for line in training_set:
        # if to include \n
        if len(line) == 1:
            original_dataset.append("\n")
        else:
            line = line.rstrip('\n') #split into the "text" and the "tag/label" using line.split()
            line = line.rpartition(' ')
            line = list(line)
            del line[1]
            if line != ['', '']:
                if line[0] in stop_words: #if the word belongs to the list of stopwords or list of symbols, assign the label O
                    line[1] = "O" #assign label O
                elif line[0] in symbols_list:
                    continue
                original_dataset.append(line)
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

# Remove Stopwords
def smooth_labels_transmission(transmission_parameters,alpha_sm=0.01):
    smoothed_dict = transmission_parameters
    #alpha_sm = 0.1 #hyperparameter for label smoothing, default 0.1
    for entry in smoothed_dict: #for each dictionary
        for label in smoothed_dict[entry]: #for each label in each dictionary
            if label != 'START':
                smoothed_dict[entry][label] *= (1 - alpha_sm)
                smoothed_dict[entry][label] += (alpha_sm/(len(smoothed_dict[entry])-1)) #add by the smoothing factor/number of labels without START
            # there is no transition to START at all
    return smoothed_dict #return smoothed dictionary

def smooth_labels(labels, factor=0.1):
	# smooth the labels
	labels *= (1 - factor)
	labels += (factor / labels.shape[1])
	# returned the smoothed labels
	return labels

def smooth_labels_emission(emission_dict,alpha_sm=0.01):
    smoothed_dict = emission_dict
    for label, word_prob_dict in emission_dict.items():
        for word in word_prob_dict.keys():
            smoothed_dict[label][word] *= (1 - alpha_sm)
            smoothed_dict[label][word] += (alpha_sm/(len(word_prob_dict)))
    return smoothed_dict



def run_viterbi(training_path, test_path, output_path,mode,alpha_sm=0.0): #mode ES or RU
    if mode =="ES":
        stopwords_a = read_stopwords(STOP_words_ES_file_path)
    elif mode =="RU":
        stopwords_a = read_stopwords(STOP_words_RU_file_path)
    train = remove_stopwords(training_path,stopwords_a)
    train_words = utilities.get_training_set_words(train)
    test = utilities.read_dev(test_path)
    tags = utilities.count_tags(train)
    tag_words = utilities.count_tag_words(train)
    
    transmission_counts = part2.count_transmissions(train)
    t_params = part2.estimate_transmission_parameters(transmission_counts, tags)
    t_params = smooth_labels_transmission(t_params,alpha_sm=alpha_sm)
    e_params = part1.estimate_emission_parameters_with_unk(tags, tag_words)
    e_params = smooth_labels_emission(e_params,alpha_sm=alpha_sm)
    prediction = part2.viterbi_loop(test, t_params, e_params, train_words)
    utilities.output_prediction(prediction, test, output_path)

def run_everything(training_path, test_path, output_path, mode):
    run_viterbi(training_path,test_path,output_path,mode)
    


if __name__ == "__main__":
    n = len(sys.argv)
    if os.path.exists(RU_test_dev_write):
        os.remove(RU_test_dev_write)
    if os.path.exists(RU_test_write):
        os.remove(RU_test_write)
    if os.path.exists(ES_test_dev_write):
        os.remove(ES_test_dev_write)
    if os.path.exists(ES_test_write):
        os.remove(ES_test_write)

    if n == 1:
        #RU
        run_everything(RU_train,RU_test_dev,RU_test_dev_write,"RU")
        run_everything(RU_train,RU_test,RU_test_write,"RU")
        #ES
        run_everything(ES_train,ES_test_dev,ES_test_dev_write, "ES")
        run_everything(ES_train,ES_test,ES_test_write,"ES")
    else:
        if n == 4:
            run_everything(sys.argv[1], sys.argv[2], sys.argv[3])
        else:
            print("usage: python part4.py [train_path] [test_path] [output_path]")
    
    #evaluation portion
    print('The scores for the russian dataset is:')
    os.system('python3 EvalScript/evalResult.py RU/dev.out RU/dev.p4.out')
    print('The scores for the ES dataset is:')
    os.system('python3 EvalScript/evalResult.py ES/dev.out ES/dev.p4.out')

    
