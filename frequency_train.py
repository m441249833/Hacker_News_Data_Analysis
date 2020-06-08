# -------------------------------------------------------
# Assignment 2
# Written by Ke Ma 26701531
# For COMP 472 Section JX – Summer 2020
# --------------------------------------------------------
import re
import pandas as pd
import math
import matplotlib.pyplot as plt

def clean(title):
    title = re.sub('\d+', ' ', title).lower()
    words = re.findall('[a-zA-Z_]+', title)
    return words


print("Reading hns_2018_2019.csv.....")
df = pd.read_csv('hns_2018_2019.csv')
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
# classify all words into its class
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


def getPerformance(frequency):
    # clean digits and punctuation.
    print("Removing frequency <="+str(frequency)+" words")
    # clean less frequent words
    # TODO
    for word in list(story):
        if story[word] <= frequency :
            del story[word]

    for word in list(ask_hn):
        if ask_hn[word] <= frequency :
            del ask_hn[word]

    for word in list(show_hn):
        if show_hn[word] <= frequency :
            del show_hn[word]

    for word in list(poll):
        if poll[word] <= frequency :
            del poll[word]


    # count total number of words in each class
    story_count = len(story)
    show_hn_count = len(show_hn)
    ask_hn_count = len(ask_hn)
    poll_count = len(poll)

    # put all words in a set as a corpus.
    corpus = sorted(set(list(story.keys()) + list(show_hn.keys()) + list(ask_hn.keys()) +list(poll.keys())))

    training_model = {}
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
        training_model[word] = [
            c1, round(((c1 + 0.5) / (story_count + len(corpus) * 0.5)), 5),
            c2, round((c2 + 0.5) / (show_hn_count + len(corpus) * 0.5), 5),
            c3, round((c3 + 0.5) / (ask_hn_count + len(corpus) * 0.5), 5),
            c4, round((c4 + 0.5) / (poll_count + len(corpus) * 0.5), 5)
        ]

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

    correct = 0
    total_test = 0

    start_index = df.index[0]
    end_index = df.index[-1]

    for i in range(start_index, end_index+1):
        score_story = math.log10(p_story)
        score_show = math.log10(p_show_hn)
        score_ask = math.log10(p_ask_hn)
        score_poll = float("-inf")

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

        if df['Post Type'][i] == result:
            correct += 1
        total_test += 1
    return (correct / total_test)*100


def getPerformance2(frequency):
    print("Removing frequency > " + str(int(frequency*100)) + "% words")
    if (len(story.values()) == 0):
        story_limit = 0
    else:
        story_values = sorted(story.values(),reverse=True)
        story_limit = story_values[int(len(story_values) * frequency)]

    if (len(ask_hn.values()) == 0):
        ask_limit = 0
    else:
        ask_values = sorted(ask_hn.values(), reverse=True)
        ask_limit = ask_values[int(len(ask_values) * frequency)]

    if (len(ask_hn.values()) == 0):
        show_limit = 0
    else:
        show_values = sorted(show_hn.values(), reverse=True)
        show_limit = show_values[int(len(show_values) * frequency)]

    if len(poll.values()) ==0 :
        poll_limit = 0
    else:
        poll_values = sorted(poll.values(), reverse=True)
        poll_limit = show_values[int(len(poll_values) * frequency)]

    # clean less frequent words
    # TODO
    for word in list(story):
        if story[word] > story_limit :
            del story[word]

    for word in list(ask_hn):
        if ask_hn[word] > ask_limit :
            del ask_hn[word]

    for word in list(show_hn):
        if show_hn[word] > show_limit :
            del show_hn[word]

    for word in list(poll):
        if poll[word] > poll_limit :
            del poll[word]



    # count total number of words in each class
    story_count = len(story)
    show_hn_count = len(show_hn)
    ask_hn_count = len(ask_hn)
    poll_count = len(poll)

    # put all words in a set as a corpus.
    corpus = sorted(set(list(story.keys()) + list(show_hn.keys()) + list(ask_hn.keys())))

    training_model = {}
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
        training_model[word] = [
            c1, round(((c1 + 0.5) / (story_count + len(corpus) * 0.5)), 5),
            c2, round((c2 + 0.5) / (show_hn_count + len(corpus) * 0.5), 5),
            c3, round((c3 + 0.5) / (ask_hn_count + len(corpus) * 0.5), 5),
            c4, round((c4 + 0.5) / (poll_count + len(corpus) * 0.5), 5)
        ]

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

    correct = 0
    total_test = 0
    for i in range(5000, 10000):
        score_story = math.log10(p_story)
        score_show = math.log10(p_show_hn)
        score_ask = math.log10(p_ask_hn)
        score_poll = float("-inf")

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

        if df['Post Type'][i] == result:
            correct += 1
        total_test += 1
    return (correct / total_test)*100

print("Removing low-frequent words and calculating performance...")
x1=[1,5,10,15,20]
y1 = [getPerformance(1),getPerformance(5),getPerformance(10),getPerformance(15),getPerformance(20)]

print("Removing high-frequent words and calculating performance...")
x2 = [5,10,15,20,25]
y2 = [getPerformance2(0.05),getPerformance2(0.1),getPerformance2(0.15),getPerformance2(0.2),getPerformance2(0.25)]

#first plot
plt.xlabel("Frequency boundary ")
plt.ylabel("Performance %")
plt.plot(x1,y1)
plt.show()

#second plot
plt.xlabel("Frequency boundary %")
plt.ylabel("Performance %")
plt.plot(x2,y2)
plt.show()