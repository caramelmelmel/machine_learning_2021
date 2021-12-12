import utilities

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

def prediction_loop(separated, e_params, word_set):
    final = []
    for doc in separated:
        final.append(predict_using_emission(doc, e_params, word_set))
    return final
        
def run_emission_prediction(training_path, test_path, output_path):
    train = utilities.read_data_transmission(training_path)
    train_words = utilities.get_training_set_words(train)
    tags = utilities.count_tags_transmission(train)
    test = utilities.read_dev(test_path)
    tag_words = utilities.count_tag_words(train)
    e_params = estimate_emission_parameters_with_unk(tags, tag_words)
    prediction = prediction_loop(test, e_params, train_words)
    utilities.output_prediction(prediction, test, output_path)

run_emission_prediction(r"ES/train", r"ES/dev.in", r"ES/dev.p1.out")
run_emission_prediction(r"RU/train", r"RU/dev.in", r"RU/dev.p1.out")