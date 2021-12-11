import os
import math

# internal files
from copy_utilities import read_universal_, read_data
from emission_utils import count_tag_words, count_labels, estimate_emission_parameters
from emission_utils import estimate_emission_parameters_with_unk
from emission_utils import test_emission
from emission_utils import write_out

#read the files here
ru_ds = read_universal_('train','RU')
word_label_list = read_data(ru_ds)
label_to_individual_count = count_tag_words(word_label_list) 
label_count = count_labels(word_label_list)
estimate_emission = estimate_emission_parameters(label_count, label_to_individual_count)


#unk portion 
###### split the dataset to test and train
tags = count_labels(word_label_list)
tag_words = count_tag_words(word_label_list)
e = estimate_emission_parameters_with_unk(tags, tag_words)
print(e)
#devfile read
dev_in_file = read_universal_('dev.in','RU')
#new line for file reading
read_file = test_emission(e,dev_in_file)
prediction_file = read_universal_('dev.p1.out','RU')
write_out(prediction_file,read_file,dev_in_file)

#get the dictionary out
#print(e)
# 






