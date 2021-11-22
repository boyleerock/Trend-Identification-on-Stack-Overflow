class Phrase:
    words = ["", ""]  # 2 words
    type = ""  # AN or NN
    freq = 1  # frequency in a single time frame
    #total_freq = 0  # combined frequency
    freqs = []  # frequency for multiple time frames

    def __init__(self, words):
        self.words = words
        self.freq = 1
