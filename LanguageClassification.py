#!/usr/bin/env python
# coding: utf-8

import string
import re, collections

import pickle as pkl

def preprocess(text):
    '''
    Removes punctuation and digits from a string, and converts all characters to lowercase. 
    Also clears all \n and hyphens (splits hyphenated words into two words).
    
    '''
        
    preprocessed_text = text.lower().replace('-', ' ')
    
    translation_table = str.maketrans('\n', ' ', string.punctuation+string.digits)
    
    preprocessed_text = preprocessed_text.translate(translation_table)
        
    return preprocessed_text

def split_into_subwords(text):
    merges = pkl.load(open('Data/Auxiliary/merge_ordered.pkl', 'rb'))
    subwords = []
    for word in text.split():
        for subword in merges:
            subword_count = word.count(subword)
            if subword_count > 0:
                word = word.replace(subword, ' ')
                subwords.extend([subword]*subword_count)
    return ' '.join(subwords)


def predict_language(text):

    language_dictionary = {'en': 'English',
            'sk': 'Slovak',
            'cs': 'Czech'
            }

    naive_classifier = pkl.load(open('Saved_Models/finalized_model.sav', 'rb'))
    text_subwords = []
    preprocessed_text = preprocess(text)
    text_subwords.append(split_into_subwords(preprocessed_text))
    vec = pkl.load(open('Data/Vectorizers/vectorizer.pk', 'rb'))
    test_vec = vec.transform(text_subwords)
    result = naive_classifier.predict(test_vec)
    return language_dictionary[result[0]]
