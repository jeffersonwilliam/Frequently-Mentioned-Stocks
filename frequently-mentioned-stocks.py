import collections
import itertools
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
import tweepy
import pandas as pd
import re


global noOfStocks
global listOfStocks
global final_list
consumer_key = 'key'
consumer_secret = 'secret'

access_token = 'token'
access_token_secret = 'token-secret'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

def stocks_query():
    global noOfStocks, searchTerm, noOfSearchTerms, string_of_stocks, listOfStocks

    noOfStocks = int(input("How many stocks would you be analyzing today? "))

    i = 0

    print("Enter the stocks you would like to analyze below: ")
    listOfStocks = []

    while i < noOfStocks:
        stocks = input()
        listOfStocks.append(stocks)
        i = i + 1

    string_of_stocks = ', '.join(listOfStocks)

    print(string_of_stocks)

    noOfSearchTerms = int(input("How many tweets would you like to work with? : "))


def remove_url(txt):
    # removes specific characters from tweet and returns a new string of tweets
    return " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", txt).split())


def word_count():
    global tweet, all_tweets, counts_nsw
    tweets = tweepy.Cursor(api.search, q=string_of_stocks, lang = 'en').items(noOfSearchTerms)

    # stores all tweets in a list
    all_tweets = [tweet.text for tweet in tweets]

    all_tweets_no_urls = [remove_url(tweet) for tweet in all_tweets]

    # splits and converts words into lower case and stores it in a list
    words_in_tweet = [tweet.lower().split() for tweet in all_tweets_no_urls]

   # creates stopwords variables
    en_stops = set(stopwords.words('english'))

    # cleans stop words from words in words_in_tweet list
    tweets_nsw = [[word for word in tweets if not word in en_stops]
                  for tweets in words_in_tweet]

    # stores some common unnecessary words
    unnecessary_words = ['rt', 'stocks']

    # cleans some unnecessary words from tweets_nsw
    tweets_nsw_no_unnecessary = [[w for w in word if w not in unnecessary_words]
                                 for word in tweets_nsw]

    # combines all words in various tweets into one list devoid of stop words
    all_words_nsw = list(itertools.chain(*tweets_nsw_no_unnecessary))

    # counts the words
    counts_nsw = collections.Counter(all_words_nsw)

def graph_stocks():
    # tweets_nsw = pd.DataFrame(final_list, columns=['words', 'count'])
    tweets_nsw = pd.DataFrame(counts_nsw.most_common(20), columns=['words', 'count'])
    fig, ax = plt.subplots(figsize=(8, 8))

    # Plot horizontal bar graph
    tweets_nsw.sort_values(by='count').plot.barh(x='words', y='count', ax=ax,
            color="red")

    ax.set_title("Popular Stocks Mentioned in Tweets")

    plt.show()


stocks_query()
word_count()
graph_stocks()