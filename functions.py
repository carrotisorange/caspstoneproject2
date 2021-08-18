# import all the packages
from flask import render_template
import preprocess_kgptalkie as ps
import re
import pandas as pd
import matplotlib.pyplot as plt
from googletrans import Translator
import pickle
# import required modules
import spacy

nlp = spacy.load("en_core_web_lg")
from collections import Counter
from wordcloud import WordCloud, STOPWORDS

translator = Translator()


# 1. function to preprocess the input
def preprocess_input(x):
    x = str(x).lower().replace('\\', '').replace('_', ' ')
    x = ps.remove_urls(x)
    x = ps.remove_html_tags(x)
    # x = ps.remove_accented_chars(x)
    x = ps.remove_special_chars(x)
    x = re.sub("(.)\\1{2,}", "\\1", x)
    # x = ''.join([i for i in x if not i.isdigit()])
    return x


# 2. function to validate the input
def validate_input(preprocessed_input):
    error = ""
    # reject numerical input
    doc = nlp(preprocessed_input)
    if preprocessed_input.isdigit():
        error = "rejectNumerical"
        return error
    # reject input with less than 3 characters
    elif len(preprocessed_input) < 3:
        error = "rejectShortText"
        return error
    elif translator.detect(preprocessed_input).lang != 'en' and translator.detect(preprocessed_input).lang != 'tl' and translator.detect(preprocessed_input).lang != 'ko':
        error = 'languageNotSupported'
        return error
    elif doc[0].pos_ != 'NOUN':
        error = "inputIsNotANoun"
        return error

    return ps.make_base(preprocessed_input)


# 3. function to classify the input
def classify_input(validated_input):
    classifier_f = open("C://Users//hp user//Desktop//caspstoneproject2//model//model.pickle", "rb")
    clf = pickle.load(classifier_f)
    classifier_f.close()
    classification = clf.predict([validated_input])
    if classification == [1]:
        result = '1'
    else:
        result = '0'

    return result


# 4. function to get the top words based on interaction count
def get_the_top_product_ideas(product_ideas):
    results = product_ideas[product_ideas['label'] == 1]

    return results
