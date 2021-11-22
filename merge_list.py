import pandas as pd


# todo: can work on list alternatively
def merge_df(df, new_df):
    new_length = new_df.shape[0]
    for i in range(0, new_length):  # iterate old df
        word_1 = new_df.iat[i, 0]
        word_2 = new_df.iat[i, 1]
        length = df.shape[0]
        for j in range(0, length):  # iterate new df
            if (word_1 == df.iat[j, 0] and word_2 == df.iat[j, 1]):  # if 2 phrases match
                df.iat[j, 2] = df.iat[j, 2] + 1  # frequency ++
            else:
                # append a row
                data = {'word 1': df.iat[j, 0], 'word 2': df.iat[j, 0], 'frequency': df.iat[j, 0]}
                new_row = pd.DataFrame(data=data, index=[len(df)])
                df.append(new_row)

    return df


# add frequency of new time frame
def add_freq(list):
    length = len(list)
    num_freqs = len(list[0].freqs)
    for i in range(0, length):
        if (num_freqs == 0):  # uninitialized, no freqs values
            list[i].freqs = []
            list[i].freqs.append(list[i].freq)
            list[i].freqs.append(0)
        else:  # already have freqs values
            list[i].freqs.append(0)

    return list


def merge_list(list, new_list):
    # if (len(list) == 0 and len(new_list) != 0):
    #     for i in range(len(new_list)):
    #         new_list[i].freqs.append(0)
    #         new_list[i].freqs.append(new_list[i].freq)
    #     return new_list
    # elif (len(list) != 0 and len(new_list) == 0):
    #     for i in range(len(list)):
    #         list[i].freqs.append(list[i].freq)
    #         list[i].freqs.append(0)
    #     return list
    # elif (len(list) == 0 and len(new_list) == 0):
    #     from Phrase import Phrase
    #     mock_phrase = Phrase(["fake", "thing"])
    #     mock_phrase.freq = -1
    #     list.append(mock_phrase)
    #     for i in range(len(list)):
    #         list[i].freqs.append(list[i].freq)
    #         list[i].freqs.append(-1)
    #     return list
    # else:
        list = add_freq(list)  # append new frequency as 0
        num_freqs = len(list[0].freqs)  # number of frequency values in array
        length = len(list)
        new_length = len(new_list)
        for i in range(0, new_length):
            matched = False
            new_phrase = new_list[i]

            for j in range(0, length):  # [0, length-1]
                phrase = list[j]

                if (phrase.words[0] == new_phrase.words[0] and phrase.words[1] == new_phrase.words[1]):
                    # matched phrase
                    matched = True
                    list[j].freqs[num_freqs - 1] = new_phrase.freq  # update new frequency
                    list[j].freq = phrase.freq + new_phrase.freq  # total frequency
                    break

            # unmatched
            if (matched == False):
                list.append(new_phrase)
                last_idx = len(list) - 1
                list[last_idx].freqs = []  # initialize freq list

                # add freqs
                for d in range(0, num_freqs):
                    list[last_idx].freqs.append(0)
                list[last_idx].freqs[num_freqs - 1] = new_phrase.freq

        # sort the list according to frequency
        def take_freq(phrase):
            return phrase.freq

        list.sort(key=take_freq, reverse=True)

        return list
