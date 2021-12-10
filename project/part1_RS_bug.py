import os
import math

# internal files
from copy_utilities import read_universal_, read_data
from emission_utils import count_tag_words, count_labels, estimate_emission_parameters

#read the files here
ru_ds = read_universal_('train','RU')
word_label_list = read_data(ru_ds)
label_to_individual_count = count_tag_words(word_label_list) 
label_count = count_labels(word_label_list)
estimate_emission = estimate_emission_parameters(label_count, label_to_individual_count)
#print(estimate_emission)
#print(label_count)
# use nested word list
#print(label_to_individual_count)




