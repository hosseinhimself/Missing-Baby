import tweepy
import pandas as pd


# function to perform data extraction
def scrape(words, date_since, numtweet):
    # Creating DataFrame using pandas
    db = pd.DataFrame(columns=['username',
                               'description',
                               'location',
                               'following',
                               'followers',
                               'totaltweets',
                               'retweetcount',
                               'link',
                               'text',
                               'hashtags'])

    # We are using .Cursor() to search
    # through twitter for the required tweets.
    # The number of tweets can be
    # restricted using .items(number of tweets)
    tweets = tweepy.Cursor(api.search_tweets,
                           words, lang="en",
                           since_id=date_since,
                           tweet_mode='extended').items(numtweet)

    # .Cursor() returns an iterable object. Each item in
    # the iterator has various attributes
    # that you can access to
    # get information about each tweet
    list_tweets = [tweet for tweet in tweets]

    # Counter to maintain Tweet Count
    i = 1

    # we will iterate over each tweet in the
    # list for extracting information about each tweet
    for tweet in list_tweets:
        try:
            print('here')
            username = tweet.user.screen_name
            description = tweet.user.description
            location = tweet.user.location
            following = tweet.user.friends_count
            followers = tweet.user.followers_count
            totaltweets = tweet.user.statuses_count
            retweetcount = tweet.retweet_count
            link = f"https://twitter.com/i/web/status/{tweet.id}"
            hashtags = tweet.entities['hashtags']

            # Retweets can be distinguished by
            # a retweeted_status attribute,
            # in case it is an invalid reference,
            # except block will be executed
            try:
                text = tweet.retweeted_status.full_text
            except AttributeError:
                text = tweet.full_text
            hashtext = list()
            for j in range(0, len(hashtags)):
                hashtext.append(hashtags[j]['text'])

            # Here we are appending all the
            # extracted information in the DataFrame
            ith_tweet = [username, description,
                         location, following,
                         followers, totaltweets,
                         retweetcount, link, text, hashtext]
            db.loc[len(db)] = ith_tweet

            # Function call to print tweet data on screen
            #printtweetdata(i, ith_tweet)
            i = i + 1
        except:
            print("A problem happened here!", i)
    filename = 'scraped_tweets_missingbaby.csv'

    # we will save our database as a CSV file.
    db.to_csv(filename)


if __name__ == '__main__':
    # Enter your own credentials obtained
    # from your developer account
    consumer_key = ""
    consumer_secret = ""
    access_key = ''
    access_secret = ''
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    # Enter Hashtag and initial date
    words = "Constance Marten OR Mark Gordon OR Constance Mark OR baby's death Victoria OR Marten Gordon OR Marten and Gordon"
    date_since = '2023-02--01'

    # number of tweets you want to extract in one run
    numtweet = 10
    scrape(words, date_since, numtweet)
    print('Scraping has completed!')


