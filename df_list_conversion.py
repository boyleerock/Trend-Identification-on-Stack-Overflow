import pandas as pd
from Phrase import Phrase


def df_to_list(df):
    num_row = len(df)
    list = []
    if (num_row == 0):
        return list
    else:
        for i in range(0, num_row):
            phrase = Phrase([df.iat[i, 0], df.iat[i, 1]])
            phrase.freq = df.iat[i, 2]  # total freq
            list.append(phrase)

        return list


# todo: add freqs list values
def list_to_df(list):
    # create words and (total) frequency list
    freq_list = []
    words_list_1 = []
    word_list_2 = []
    length = len(list)
    for i in range(0, length):  # todo
        freq_list.append(list[i].freq)
        words_list_1.append(list[i].words[0])
        word_list_2.append(list[i].words[1])

    # dictionary of list
    dict = {'word 1': words_list_1, 'word 2': word_list_2, 'frequency': freq_list}
    df = pd.DataFrame.from_dict(dict)

    return df
