import tweepy
import keys
import pandas as pd
# from databricks import sql
# import os
# with sql.connect(server_hostname = os.getenv('DATABRICKS_HOST'),
#                  http_path = os.getenv('DATABRICKS_HTTP_PATH'),
#                  access_token = os.getenv('DATABRICKS_TOKEN')) as db:


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

# search for tweets with the word crypto
# query = "Crypto"
# start_time = '2022-09-8T22:00:00Z'
# end_time = "2022-09-14T22:00:00Z"
# max_result = 50

# write a function get all the tweets for a given user


def getTweet(client, id):
    tweet = client.get_tweets(
        id, expansions=['author_id'], user_fields=['username'])
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
        # print(tweets.data)
        for tweet in tweets.data:
            twt = getTweet(client, tweet['id'])
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

    df = pd.DataFrame(results)
    df.to_csv('tweets.csv')
    # print(df.head())


if __name__ == '__main__':
    searchTweets('crypto', 10)
