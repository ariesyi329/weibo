import numpy as np
import pandas as pd

def load_data(weibo_id):
    df = pd.read_csv('../data/weibo_sample_{}_1.csv'.format(weibo_id), encoding='utf-8')
    df = df.drop('Unnamed: 0',1)
    return df

def list_split(li, loc):
    if len(loc) == 1:
        return li[:loc[0]],li[loc[0]+1:]
    else:
        split_loc = loc[0]
        new_li = li[split_loc+1:]
        new_loc = [x-split_loc-1 for x in loc[1:]]
        return (li[:split_loc],) + list_split(new_li, new_loc)

def get_emotions(index, text):
    #get emotion dic
    emotion_dict = {}
    for ind in index:
        chars = list(text[ind])
        for char in xrange(0, len(chars) - 1):
            if chars[char] == u'[':
                word = ()
                for emotion in xrange(char + 1, len(chars) - 1):
                    if chars[emotion] == u']':
                        break
                    word = word + (chars[emotion],)
                if word not in emotion_dict:
                    emotion_dict[word] = 1
                else:
                    emotion_dict[word] += 1
    #sort dict
    emotion_dict = sorted(emotion_dict.items(), key=lambda x: x[1], reverse=True)
    return emotion_dict

def get_keywords(index, text):
    #get keywords dic
    word_dict = {}
    for ind in index:
        chars = list(text[ind])
        punct_loc = []
        for char in xrange(0, len(chars)):
            if chars[char] in [u']', u'[',u'\uff01',u'\uff0c',u' ',u'@']:
                punct_loc.append(char)
        if punct_loc != []:
            splited = list_split(chars, punct_loc)
        else:
            splited = chars
        for setence in splited:
            if setence != []:
                for char in xrange(0,len(setence)-1):
                    word = (setence[char], setence[char+1])
                    if word not in word_dict:
                        word_dict[word] = 1
                    else:
                        word_dict[word] += 1

    #sort dict
    word_dict = sorted(word_dict.items(), key=lambda x: x[1], reverse=True)
    return word_dict

def dict_to_df(words_dict, columns_name, ranks):
    df = pd.DataFrame(columns=columns_name)
    for rank in xrange(0,ranks):
        word = u''
        for i in xrange(0,len(words_dict[rank][0])):
            word = word + words_dict[rank][0][i]
        freq = words_dict[rank][1]
        df.loc[rank] = [word, freq]
    return df






