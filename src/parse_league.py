# Put all json files in directory dir
# python parse_league.py dir

import os
import json
import nltk
import sys
from stop_words import get_stop_words
from nltk.corpus import stopwords

ignore = list(get_stop_words('en'))         #Have around 900 stopwords
nltk_words = list(stopwords.words('english'))   #Have around 150 stopwords
ignore.extend(nltk_words)
ngram_map = dict()

def print_ngrams():
    sorted_map = sorted(ngram_map.items(), key=lambda x:-x[1])
    for (ngram, count) in sorted_map:
        if count > 1:
            print("\"" + ' '.join(list(ngram)).strip() + "\"", count)


def find_ngrams(input_list, n):
    return list(zip(*[input_list[i:] for i in range(n)]))

def getChats_v2(jsonObj):
    extractChat = lambda x: x["chat"]
    ingame = jsonObj["chat_logs"]["in_game"]
    postgame = jsonObj["chat_logs"]["post_game"]
    pregame = jsonObj["chat_logs"]["pre_game"]
    
    ingame = (list(map(extractChat, ingame)))
    postgame = (list(map(extractChat, postgame)))
    pregame = (list(map(extractChat, pregame)))
    
    allChats = ingame + postgame + pregame
    return allChats

def getChats_v1(jsonObj):
    chats = jsonObj["text"]
    extractChat = lambda x: x["chat"]
    allChats = (list(map(extractChat, chats)))
    return allChats
    
def getChats(jsonObj):
    if "chat_logs" in jsonObj:
        return getChats_v2(jsonObj)
    if "text" in jsonObj:
        return getChats_v1(jsonObj)
    return []
    
def updateNgramMap(chats):
    for chat in chats:
        words = chat.split(" ")
        unigrams = find_ngrams(words, 1)
        bigrams = find_ngrams(words, 2)
        trigrams = find_ngrams(words, 3)
        ngrams = unigrams + bigrams + trigrams
        
        for ngram in ngrams:
            if len(ngram) == 1:
                if ngram[0] in ignore:
                    continue
            if ngram not in ngram_map:
                ngram_map[ngram] = 0
            ngram_map[ngram] += 1
    
def analyze(dir_path):
    chat_files = os.listdir(dir_path)
    
    for filename in chat_files:
        filepath = os.path.join(dir_path, filename)
        f = open(filepath)
        
        data = json.load(f)
        chats = getChats(data)
        updateNgramMap(chats)
    print_ngrams()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('usage: python parse_league.py json_dir')
        exit(1)
    analyze(sys.argv[1])