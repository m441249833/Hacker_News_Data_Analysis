# -------------------------------------------------------
# Assignment 2
# Written by Ke Ma 26701531
# For COMP 472 Section JX – Summer 2020
# --------------------------------------------------------
import re
import pandas as pd

# clean digits and punctuation.
fr = open("remove/remove_word.txt","w",encoding="utf-8")
def clean(title):
    title = re.sub('\d+', ' ', title).lower()
    words = re.findall('[a-zA-Z_]+', title)
    clean_words = []
    for word in words:
        if len(word) > 2 and len(word) < 9:
            clean_words.append(word)
        else:
            fr.write(word + "\n")
    return clean_words

print("Reading hns_2018_2019.csv.....")
df = pd.read_csv('hns_2018_2019.csv')
print("Cleaning title.....")
df['clean_title'] = df['Title'].apply(clean)


df = df[df['year'] == 2018]
story_df = df[df['Post Type'] == 'story']
show_hn_df = df[df['Post Type'] == 'show_hn']
ask_hn_df = df[df['Post Type'] == 'ask_hn']
poll_df = df[df['Post Type'] == 'poll']


story = {}
show_hn = {}
ask_hn = {}
poll = {}

#classify all words into its class
for row in story_df['clean_title']:
    if len(row) != 0:
        for word in row:
            if story.get(word) == None:
                story[word] = 1
            else:
                story[word] += 1

for row in show_hn_df['clean_title']:
    if len(row) != 0:
        for word in row:
            if show_hn.get(word) == None:
                show_hn[word] = 1
            else:
                show_hn[word] += 1

for row in ask_hn_df['clean_title']:
    if len(row) != 0:
        for word in row:
            if ask_hn.get(word) == None:
                ask_hn[word] = 1
            else:
                ask_hn[word] += 1

for row in poll_df['clean_title']:
    if len(row) != 0:
        for word in row:
            if poll.get(word) == None:
                poll[word] = 1
            else:
                poll[word] += 1

#count total number of words in each class
story_count = len(story)
show_hn_count = len(show_hn)
ask_hn_count = len(ask_hn)
poll_count = len(poll)

#put all words in a set as a corpus.
corpus = sorted(set(list(story.keys()) + list(show_hn.keys()) + list(ask_hn.keys()) + list(poll.keys())))

print("Building wordlength-model......")
# output the model information
f = open("wordlength-model.txt", "w", encoding="utf-8")
i = 1
for word in corpus:
    c1, c2, c3, c4 = 0, 0, 0, 0
    if story.get(word) != None:
        c1 = story[word]
    if show_hn.get(word) != None:
        c2 = show_hn[word]
    if ask_hn.get(word) != None:
        c3 = ask_hn[word]
    if poll.get(word) != None:
        c4 = poll[word]

    str_temp = str(i) + "  " + word + "  " \
               + str(c1) + "  " + str(round(((c1 + 0.5) / (story_count + len(corpus) * 0.5)), 5)) + "  " \
               + str(c2) + "  " + str(round((c2 + 0.5) / (show_hn_count + len(corpus) * 0.5), 5)) + "  " \
               + str(c3) + "  " + str(round((c3 + 0.5) / (ask_hn_count + len(corpus) * 0.5), 5)) + "  " \
               + str(c4) + "  " + str(round((c4 + 0.5) / (poll_count + len(corpus) * 0.5), 5)) + "\n"
    f.write(str_temp)
    i += 1

print("Total words: "+str(len(corpus)))
f.close()
print("Completed.")