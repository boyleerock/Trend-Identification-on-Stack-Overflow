from extract_phrase import *
from request_data import *
import pandas as pd
from merge_list import merge_list
from df_list_conversion import *
from request_data import *


# def main():
#     print("main")
#
# if __name__ == "__main__":

# get start&end of each time window
def split_windows(start, end, num_window):
    start_time = datetime.strptime(start, '%Y-%m-%d')
    end_time = datetime.strptime(end, '%Y-%m-%d')

    delta = end_time - start_time
    total_seconds = delta.total_seconds()  # total seconds in between

    interval = total_seconds / num_window  # length of each time window

    end_dates = []
    for i in range(num_window):
        end_dates.append(start_time + timedelta(seconds=interval * (i + 1)))  # end date of each time window
        end_dates[i] = end_dates[i].strftime("%Y-%m-%d, %H:%M:%S")  # convert to string

    # construct a matrix storing start/end time, e.g.,
    # time_window_1 start (excl.) end (incl.)
    # time_window_2 start (excl.) end (incl.)
    # time_window_3 start (excl.) end (incl.)
    # fixme: excl or incl?
    start_end = []
    for i in range(num_window):
        start = ""
        if (i == 0):
            start = start_time.strftime("%Y-%m-%d, %H:%M:%S")
        else:
            start = end_dates[i - 1]
        end = end_dates[i]
        start = start.replace(',', '')
        end = end.replace(',', '')
        row = [start, end]
        start_end.append(row)

    # print(start_end)

    return start_end


input_file = "static/txt/input.txt"
freqs = []
f = open(input_file, 'r')  # read input posted by front-end
lines = f.readlines()

line_split = lines[0].split(" ")

# get each value [start, end, num_window, limit, types, sort, word]
for i in range(0, 7):
    line_split[i] = line_split[i].split(":")[1]
print(line_split)
start = line_split[0]
end = line_split[1]
num_window = int(line_split[2])
limit = line_split[3]
types = line_split[4]
sort = line_split[5]
word = line_split[6]

# get time windows
start_end = split_windows(start, end, num_window)

list_res = []
list_merged = []
for i in range(num_window):
    line_split[0] = start_end[i][0]
    line_split[1] = start_end[i][1]
    df = request_data(line_split)  # request data
    new_df_res = extract(df, word)  # extract phrases
    new_list_res = df_to_list(new_df_res)
    if (i == 0):
        list_merged = new_list_res
    else:  # have 2 lists or more: merge
        list_merged = merge_list(list_merged, new_list_res)
    if (len(list_merged) > 0):
        print(list_merged[0].words)
    # df_res = extract(df, 2, word)
    # list_res = df_to_list(new_df_res)

df_merged = list_to_df(list_merged)  # convert merged list to df

# append frequency of individual time windows
single_freq = []
for j in range(0, num_window):
    for i in range(0, len(list_merged)):
        single_freq.append(list_merged[i].freqs[j])
        # dict = {'time_window_%s' % j: single_freq}
        # df = pd.DataFrame.from_dict(dict)
        # df['time_window_%s' % j] = single_freq
    df_merged.insert(j + 3, start_end[j][0] + " - " + start_end[j][1], single_freq, True)
    # merged_df.append(dict,ignore_index=True)
    single_freq = []
df_merged.to_csv("output/merge.csv")

