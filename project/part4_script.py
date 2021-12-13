import os
from copy_utilities import read_universal_
import numpy as np
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

step = 0.1

python_cmd = "python3"
if os.name != "posix":
    python_cmd = "python"

for i in np.arange(0,1.0,step):
    print(f"The value of alpha is {i}")

    os.system(f'{python_cmd} part4.py {i}')
    
    