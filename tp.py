from cmath import polar
from distutils.command.clean import clean
import imp
import snscrape.modules.twitter as sntwt
import pandas as pd
# from transformers import AutoTokenizer, AutoModelForSequenceClassification
# from scipy.special import softmax
from textblob import TextBlob

def mainfunction(str):
    query = str

    tweets = []
    content = []
    lim = 300
    for t in sntwt.TwitterSearchScraper(query).get_items():
        if(len(tweets) == lim):
            break
        else:
            tweets.append([t.username, t.content])
            content.append(t.content)

    content_matrix = []
    for t in content:
        content_words = []
        for words in t.split(' '):
            if words.startswith('@') and len(words) > 1:
                words = '@user'
            
            elif words.startswith('http'):
                words = "http"
            content_words.append(words)
        content_matrix.append(content_words)

    clean_tweets = []

    #To filter out only English tweets
    from langdetect import detect

    for x in content_matrix:
        tweet_proc = " ".join(x)
        lang = detect(tweet_proc)
        if(lang == "en"):
            clean_tweets.append(tweet_proc)

    # print(clean_tweets)
    no_of_tweets = len(clean_tweets)
    total_polarity = 0.0
    neg_pol = 0
    pos_pol = 0
    total_subjectivity = 0.0
    for t in clean_tweets:
        blob = TextBlob(t)
        total_polarity += blob.sentiment.polarity
        pol = blob.sentiment.polarity
        if(pol < 0):
            neg_pol += 1
        elif(pol > 0):
            pos_pol += 1
        
        total_subjectivity += blob.sentiment.subjectivity

    polarity = total_polarity/no_of_tweets
    subjectivity = total_subjectivity/no_of_tweets
    neg_percent = neg_pol/no_of_tweets
    pos_percent = pos_pol/no_of_tweets
    print("Total tweets: ", no_of_tweets)
    print("negative tweets: ", neg_pol)
    print("Positive tweets: ", pos_pol)
    print("Neg Polarity: ", neg_percent*100, "%")
    print("Pos Polarity: ", pos_percent*100, "%")
    print("Subjectivity: ", subjectivity)
    print("Polarity: ", polarity)
    
    
    list = [no_of_tweets, neg_pol, pos_pol, round(polarity, 4), round(subjectivity*100, 4)]

    return list
    # roberta = "cardiffnlp/twitter-roberta-base-sentiment"

    
    # model = AutoModelForSequenceClassification.from_pretrained(roberta)
    # tokenizer = AutoTokenizer.from_pretrained(roberta)

    # labels = ['Negative', 'Neutral', 'Positive']

    # encoded_twt = tokenizer(clean_tweets[3], return_tensors='pt')
    # output = model(**encoded_twt)

    # score = output[0][0].detach().numpy()

    # score = softmax(score)

    # for i in range(len(score)):
    #     l = labels[i]
    #     s = score[i]
        
    #     print(l,s)

    # #returning the score to the flask app     
    # return score
# fileobj = open(file, 'rb')
# pkl_chk = pickle.load(fileobj)
# # print("The value of pkl check: ")
# # print(pkl_chk)