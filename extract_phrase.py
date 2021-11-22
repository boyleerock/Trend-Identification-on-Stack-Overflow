import spacy
import pandas as pd
# noinspection PyUnresolvedReferences
from spacy.matcher import Matcher
import request_data
import clear_df
import Phrase
import re
# noinspection PyUnresolvedReferences
from spellchecker import SpellChecker
import inflect
import datetime

# Load English tokenizer, tagger, parser and NER
nlp = spacy.load("en_core_web_sm")


# df = request_data.df  # get the df from request_data.py
# from request_data import request_data
# df = request_data()


# def has_char(df,row_num):
#     has_char = df['body'].str.contains('a') or df['body'].str.contains('b') or df['body'].str.contains('c')

def extract(df, word):
    word = word.lower()
    print("extracting phrases at", datetime.datetime.now())
    print("length of raw data:", df.shape[0])
    length = df.shape[0]
    # fixme: error handling
    if (length == 0):
        d = {'id': ["0"], 'title': ["0"], 'body': ["0"]}
        df = pd.DataFrame(data=d)
        print("Dataframe is empty!")

    from clear_df import clear_df

    query = clear_df(df, 2)  # fixme: find the correct column

    # matcher
    matcher = Matcher(nlp.vocab)
    # Add match ID "post" with patterns A N, N N (N includes proper nouns)
    pattern = [
        [{"POS": "ADJ"}, {"POS": "NOUN"}], [{"POS": "NOUN"}, {"POS": "NOUN"}], [{"POS": "PROPN"}, {"POS": "NOUN"}],
        [{"POS": "NOUN"}, {"POS": "PROPN"}], [{"POS": "PROPN"}, {"POS": "PROPN"}],
        [{"POS": "ADJ"}, {"POS": "PROPN"}]  # ,[{"POS": "DET"}, {"POS": "NOUN"}]
    ]
    matcher.add("post", pattern)

    full_list = []  # all phrases
    phrases_list = []  # list to store phrases to be sorted
    length = query.shape[0]  # total number of rows of raw df

    # read input for spelling and singularize
    f = open('static/txt/input.txt', 'r')  # read input posted by front-end
    lines = f.readlines()
    line_split = lines[0].split(" ")
    spell = line_split[8].split(":")[1]
    singular = line_split[9].split(":")[1]
    print("spell", spell)
    print("singular", singular)

    if (spell == "1" or singular == "1"):
        spell = SpellChecker()
        singularize = inflect.engine()
        for i in range(0, length):  # [0, length-1]
            if (pd.isna(query.iat[i, 2]) == False):
                text = query.iat[i, 2]  # body at column 2
                text = nlp(text)  # prepare for nlp analysis
                matches = matcher(text)  # match
                for match_id, start, end in matches:
                    string_id = nlp.vocab.strings[match_id]  # Get string representation
                    span = text[start:end]  # The matched span (2 words)
                    # print(  # match_id, string_id, start, end,#
                    # span.text)

                    # to lower case
                    if (" " in span.text):  # eliminate "id"
                        span = [span[0].text.lower(), span[1].text.lower()]
                        # spelling correction
                        if (spell == "1"):
                            # print("enabled spelling correction")
                            span[0] = spell.correction(span[0])
                            span[1] = spell.correction(span[1])
                        # plural -> singular
                        if (singular == "1"):
                            # print("enabled singularize")
                            if (singularize.singular_noun(span[0])):
                                span[0] = str(singularize.singular_noun(span[0]))
                            if (singularize.singular_noun(span[1])):
                                span[1] = str(singularize.singular_noun(span[1]))

                        match1 = re.search('[a-z]', span[0])
                        match2 = re.search('[a-z]', span[1])

                        if (match1 or match2):  # fixme: either side has letters
                            match1 = re.search(word, span[0])
                            match2 = re.search(word, span[1])

                            if (match1 or match2):  # have the word to be searched

                                from Phrase import Phrase  # phrase class

                                phrase = Phrase(span)  # create a phrase instance with the 2 words []

                                # add phrase
                                phrases_list.append(phrase)
                                full_list.append(span)

                                # check if phrase already stored
                                len_list = len(phrases_list)
                                if (len_list >= 2):
                                    for j in range(0, len_list - 1):  # (0, len_list-2]
                                        if (phrases_list[j].words[0] == span[0]
                                                and phrases_list[j].words[1] == span[1]):  # both words matched
                                            phrases_list[j].freq += 1  # increment frequency
                                            phrases_list.pop()  # remove duplicate phrase from list
    else:
        for i in range(0, length):  # [0, length-1]
            if (pd.isna(query.iat[i, 2]) == False):
                text = query.iat[i, 2]  # body at column 2
                text = nlp(text)  # prepare for nlp analysis
                matches = matcher(text)  # match
                for match_id, start, end in matches:
                    string_id = nlp.vocab.strings[match_id]  # Get string representation
                    span = text[start:end]  # The matched span (2 words)
                    # print(  # match_id, string_id, start, end,#
                    # span.text)

                    # to lower case
                    if (" " in span.text):  # eliminate "id"
                        span = [span[0].text.lower(), span[1].text.lower()]

                        match1 = re.search('[a-z]', span[0])
                        match2 = re.search('[a-z]', span[1])

                        if (match1 or match2):  # fixme: either side has letters
                            match1 = re.search(word, span[0])
                            match2 = re.search(word, span[1])

                            if (match1 or match2):  # have the word to be searched

                                from Phrase import Phrase  # phrase class

                                phrase = Phrase(span)  # create a phrase instance with the 2 words []

                                # add phrase
                                phrases_list.append(phrase)
                                full_list.append(span)

                                # check if phrase already stored
                                len_list = len(phrases_list)
                                if (len_list >= 2):
                                    for j in range(0, len_list - 1):  # (0, len_list-2]
                                        if (phrases_list[j].words[0] == span[0]
                                                and phrases_list[j].words[1] == span[1]):  # both words matched
                                            phrases_list[j].freq += 1  # increment frequency
                                            phrases_list.pop()  # remove duplicate phrase from list

    # sort the list according to frequency
    def take_freq(phrase):
        return phrase.freq

    phrases_list.sort(key=take_freq, reverse=True)

    # create words and frequency list
    freq_list = []
    words_list_1 = []
    word_list_2 = []

    if (len(phrases_list) == 0):
        from Phrase import Phrase
        mock_phrase = Phrase(["fake", "thing"])
        mock_phrase.freq = -99999999
        phrases_list.append(mock_phrase)
        print("added",phrases_list[0].words)

    full_len = len(phrases_list)
    print("total number of phrases in this time window:", full_len)
    print(datetime.datetime.now())

    for i in range(0, full_len):  # [0, full_len-1]
        freq_list.append(phrases_list[i].freq)
        words_list_1.append(phrases_list[i].words[0])
        # label significant phrases
        # if (phrases_list[i].freq >= length / 100):
        #     word_list_2.append(phrases_list[i].words[1] + " *")  # todo
        # else:
        word_list_2.append(phrases_list[i].words[1])

    # dictionary of list
    dict = {'word 1': words_list_1, 'word 2': word_list_2, 'frequency': freq_list}
    df_res = pd.DataFrame.from_dict(dict)
    # output the dataframe
    df_res.to_csv('output/table.csv')

    dict_full = {'phrase': full_list}  # list of all phrases without grouping and sorting
    df = pd.DataFrame.from_dict(dict_full)
    # ouput the dataframe
    df.to_csv('intermediate_data/phrases_full.csv')

    return df_res

### testing code
# df = pd.read_csv("output/raw.csv")
# word = "a"
# extract(df, word)
