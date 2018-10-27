import pandas as pd
from nltk.corpus import stopwords
import nltk as nl
from nltk import PorterStemmer
from collections import namedtuple

Vector = namedtuple("Vector", 'data,label')
stemmer = PorterStemmer()

def preprocess(data):
    stopword_set = set(stopwords.words("english"))
    lower = []
    all_words = []
    without_stopwords = []
    new_data = []
    stemmed = []
    for item in data:
        if "\n" in item:
            item = item.replace("\n", " ")
        new_data.append(item)
        lower = item.lower()
        all_words = nl.word_tokenize(lower)
        without_stopwords = []
        for word in all_words:
            if word not in stopword_set and word.isalpha():
                without_stopwords.append(word)
        for item in without_stopwords:
            stemmed.append(stemmer.stem(item))
    stemmed_set = set(stemmed)
    return stemmed

def GetAllDataFeatures(stemmed):
    freq_words = nl.FreqDist(stemmed)
    frequent = list(freq_words.keys())[:1000]
    return frequent

def one_hot(curr_input, frequent):
    curr_input = set(curr_input)
    curr_input_features = {}
    for item in frequent:
        if item in curr_input:
            curr_input_features[item] = True
        else:
            curr_input_features[item] = False
    return curr_input_features

def getMostFrequentWords(training_file):
    with open(training_file) as tf:
        column_names = ['text','label']
        read_train_data = pd.read_csv(tf,names=column_names, encoding='latin-1')
        text = read_train_data.text.tolist()
        text[:] = text[1:]
    return GetAllDataFeatures(preprocess(text))

def generateTrainingSet(training_file, frequent_words):
    training_set = []
    with open(training_file) as tf:
        next(tf)
        column_names = ['text','label']
        read_train_data = pd.read_csv(tf,names=column_names, encoding='latin-1')
        for index, row in read_train_data.iterrows():
            preprocessed_review = preprocess([ row["text"] ]  )
            hot_list = one_hot(preprocessed_review, frequent_words)
            training_set.append(Vector(hot_list, row["label"]))
    return training_set
        
def main(training_file, testing_file):
    frequent_words = getMostFrequentWords(training_file)
    print("most frequent_words: ", frequent_words)
    training_set = generateTrainingSet(training_file, frequent_words)
    print("training set: ", training_set)
    nbc = nl.NaiveBayesClassifier.train(training_set)
    print("trained....")
    testing_set = generateTrainingSet(testing_file, frequent_words)
    print(nl.classify.accuracy(nbc, testing_set)*100)
    

if __name__ == "__main__":
    main("training_file1.csv","testing_file1.csv")
