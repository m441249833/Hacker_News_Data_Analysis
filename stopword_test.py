# -------------------------------------------------------
# Assignment 2
# Written by Ke Ma 26701531
# For COMP 472 Section JX – Summer 2020
# --------------------------------------------------------
import math
import re
import pandas as pd
import string

# generate stopwords list
stopwords = []
f = open('stopwords.txt', 'r', encoding='utf-8')
for line in f:
    stopwords.append(line.translate(str.maketrans(' ', ' ', string.punctuation)).lower().strip())

# clean out stop words.
def clean(title):
    title = re.sub('\d+', ' ', title).lower()
    words = re.findall('[a-zA-Z_]+', title)
    clean_words = []
    for word in words:
        if word not in stopwords:
            clean_words.append(word)
    return clean_words

print("Collecting 2019 test data......")
df = pd.read_csv('hns_2018_2019.csv')
df['clean_title'] = df['Title'].apply(clean)
df = df[df['year'] == 2019]
story_df = df[df['Post Type'] == 'story']
show_hn_df = df[df['Post Type'] == 'show_hn']
ask_hn_df = df[df['Post Type'] == 'ask_hn']
poll_df = df[df['Post Type'] == 'poll']

p_story = len(story_df) / (len(story_df) + len(show_hn_df) + len(ask_hn_df) + len(poll_df))
p_show_hn = len(show_hn_df) / (len(story_df) + len(show_hn_df) + len(ask_hn_df) + len(poll_df))
p_ask_hn = len(ask_hn_df) / (len(story_df) + len(show_hn_df) + len(ask_hn_df) + len(poll_df))
p_poll = len(poll_df) / (len(story_df) + len(show_hn_df) + len(ask_hn_df) + len(poll_df))

print("Applying data to stopword-model......")


f = open("stopword-model.txt", "r", encoding="utf-8")
lines = f.readlines()
training_model = {}
for line in lines:
    l = line.split()
    training_model[l[1]] = [int(l[2]), float(l[3]), int(l[4]), float(l[5]), int(l[6]), float(l[7]), int(l[8]),
                            float(l[9])]


print("Generating result stopword-result.txt......")
f = open("stopword-result.txt", "w", encoding="utf-8")

start_index = df.index[0]
end_index = df.index[-1]

for i in range(start_index, end_index+1):

    score_story = float("-inf")
    score_show = float("-inf")
    score_ask = float("-inf")
    score_poll = float("-inf")

    if p_story != 0:
        score_story = math.log10(p_story)
    if p_show_hn != 0:
        score_show = math.log10(p_show_hn)
    if p_ask_hn != 0:
        score_ask = math.log10(p_ask_hn)
    if p_poll != 0:
        score_poll = math.log10(p_poll)

    for word in df['clean_title'][i]:
        if training_model.get(word):
            score_story += math.log10(training_model[word][1])
            score_show += math.log10(training_model[word][3])
            score_ask += math.log10(training_model[word][5])
            score_poll += math.log10(training_model[word][7])

    score_story = round(score_story, 3)
    score_show = round(score_show, 3)
    score_ask = round(score_ask, 3)
    score_poll = round(score_poll, 3)

    high_score = max(score_story, score_show, score_ask, score_poll)
    result = ""
    if high_score == score_story:
        result = "story"
    elif high_score == score_show:
        result = "show_hn"
    elif high_score == score_ask:
        result = "ask_hn"
    else:
        result = "poll"

    correct = ""
    if df['Post Type'][i] == result:
        correct = "right"
    else:
        correct = "wrong"
    f.write(str(i - 4999) + "  " + df['Title'][i] + "  " + result + "  " + str(score_story) + "  " + str(
        score_ask) + "  " + str(score_show) + "  " + str(score_poll) + "  " + df['Post Type'][
                i] + "  " + correct + "\n")
f.close()
print("stopword-result.txt generated.")