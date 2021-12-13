import utilities
import sys
import os

# Estimates emission parameters using MLE.
# Adds an #UNK# token for use when we encounter a word in the test set that is not in our training set.
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

# Simple sentiment analysis system on a sentence.
def predict_using_emission(words, e_params, word_set):
    labels = ['O', 'B-positive', 'B-neutral', 'B-negative', 'I-positive', 'I-neutral', 'I-negative']
    out = []
    for word in words:
        max_label = 'O'
        max_probability = 0
        if word not in word_set:
            # The word is not seen in our test set. We replace it with #UNK#.
            word = "#UNK#"
        for u in labels:
            if word not in e_params[u]:
                # No possible emission to this word from this label so we skip it.
                continue
            current_prob = e_params[u][word]
            if current_prob > max_probability:
                max_label = u
                max_probability = current_prob
        out.append(max_label)
    return out

# Runs the sentence on each word in our dataset.
def prediction_loop(separated, e_params, word_set):
    final = []
    for doc in separated:
        final.append(predict_using_emission(doc, e_params, word_set))
    return final

# Wrapper function that trains the emission parameters and runs the predictor on the
def run_emission_prediction(training_path, test_path, output_path):
    train = utilities.read_data(training_path)
    train_words = utilities.get_training_set_words(train)
    tags = utilities.count_tags(train)
    test = utilities.read_dev(test_path)
    tag_words = utilities.count_tag_words(train)
    e_params = estimate_emission_parameters_with_unk(tags, tag_words)
    prediction = prediction_loop(test, e_params, train_words)
    utilities.output_prediction(prediction, test, output_path)

if __name__ == '__main__':
    n = len(sys.argv)

    if n == 1:
        run_emission_prediction(r"ES/train", r"ES/dev.in", r"ES/dev.p1.out")
        run_emission_prediction(r"RU/train", r"RU/dev.in", r"RU/dev.p1.out")
    else:
        if n == 4:
            run_emission_prediction(sys.argv[1], sys.argv[2], sys.argv[3])
        else:
            print("usage: python part1.py [train_path] [test_path] [output_path]")
            
    python_cmd = "python3"
    if os.name != "posix":
        python_cmd = "python"
    #evaluation portion
    print('The scores for the russian dataset is:')
    os.system(f'{python_cmd} EvalScript/evalResult.py RU/dev.out RU/dev.p1.out')
    print('The scores for the ES dataset is:')
    os.system(f'{python_cmd} EvalScript/evalResult.py ES/dev.out ES/dev.p1.out')