import imp
import snscrape.modules.twitter as sntwt
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax

query = "Zhongli"

tweets = []
content = []
lim = 20
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

print(clean_tweets[3])

roberta = "cardiffnlp/twitter-roberta-base-sentiment"

model = AutoModelForSequenceClassification.from_pretrained(roberta)
tokenizer = AutoTokenizer.from_pretrained(roberta)

labels = ['Negative', 'Neutral', 'Positive']

encoded_twt = tokenizer(clean_tweets[3], return_tensors='pt')
output = model(**encoded_twt)

score = output[0][0].detach().numpy()

score = softmax(score)

for i in range(len(score)):
    l = labels[i]
    s = score[i]
    
    print(l,s)