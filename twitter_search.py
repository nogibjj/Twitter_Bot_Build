import tweepy
import keys
import pandas as pd
import boto3
from botocore.exceptions import NoCredentialsError


consumer_key = keys.consumer_key
consumer_secret = keys.consumer_secret
Bearer_Token = keys.Bearer_Token
Token = keys.Token
Token_Secret = keys.Token_Secret

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(Token, Token_Secret)
api = tweepy.API(auth)

getClient = tweepy.Client(bearer_token=Bearer_Token,
                          consumer_key=consumer_key,
                          consumer_secret=consumer_secret,
                          access_token=Token,
                          access_token_secret=Token_Secret)
client = getClient


# write a function that gets the tweet with the tweet id
def getTweet(id_twitter):
    tweet = client.get_tweets(
        id_twitter, expansions=['author_id'], user_fields=['username'])
    return tweet


# write a function that searches twitter with key words and returns the tweets with user id of the user who tweeted it
def searchTweets(query, max_results):
    tweets = client.search_recent_tweets(query=query,
                                         tweet_fields=[
                                             'text', 'context_annotations', 'created_at'],
                                         expansions=['referenced_tweets.id', 'attachments.media_keys',
                                                     'author_id', 'entities.mentions.username', 'geo.place_id'],
                                         user_fields=[
                                             'id', 'username', 'description', 'entities', 'protected', 'public_metrics', 'verified'],
                                         place_fields=['place_type', 'geo'],
                                         max_results=max_results)

    user = {u['id']: u for u in tweets.includes['users']}

    results = []
    if not tweets.data is None and len(tweets.data) > 0:
        for tweet in tweets.data:
            twt = getTweet(tweet['id'])
            obj = {}
            obj['author_id'] = tweet.id
            obj['text'] = tweet.text
            obj['lang'] = tweet.lang
            obj['entities'] = tweet.entities
            obj['username'] = twt.includes['users'][0].username
            if user[tweet.author_id]:
                user1 = user[tweet.author_id]
                obj['public_metrics'] = user1.public_metrics
                obj['verified'] = user1.verified
            obj['url'] = 'https://twitter.com/{}/status/{}'.format(
                twt.includes['users'][0].username, tweet['id'])
            obj['followers_count'] = user1.public_metrics['followers_count']
            obj['following_count'] = user1.public_metrics['following_count']
            obj['tweet_count'] = user1.public_metrics['tweet_count']

            results.append(obj)
    else:
        return "No tweets found"

    search_df = pd.DataFrame(results)

    # save the dataframe to s3
    search_df.to_csv("s3://projecttwitterbot/Searching/search_df.csv",
                     storage_options={'key': keys.access_key, 'secret': keys.secret_access_key})


if __name__ == '__main__':
    searchTweets('crypto', 50)
