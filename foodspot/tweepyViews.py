from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework import serializers
from django.http import HttpResponse
import tweepy
import json
from textblob import TextBlob

consumer_key = 'YXljpaC7F1DTfV9oNqFBOtljF'
consumer_secret = 'x4aUOdpYyuGpeWECVr1XBm3l2to1BkYBTUdpt39TkuLnl2FHTR'
access_token = '2282360125-Cu77pahpo45uCOBDIOcv1WEBUqBovAXa5i7qU9E'
access_token_secret = 'DSY2XW5KVKw5iYvr0XSpXoMxDPCQu5FwE5SpP6pSn6r8M'

def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'


class Tweet:
	def __init__(self, **kwargs):
		for field in ('id', 'text'):
			setattr(self, field, kwargs.get(field, None))

tweets = {
	
	1 : Tweet(id=1, text="Hello World"),
	2 : Tweet(id=2, text="Hey"),
	3 : Tweet(id=3, text="Hi"),
}

class TweetSerializer(serializers.Serializer):
	id = serializers.IntegerField(read_only=True)
	text = serializers.CharField(max_length=256)

	def create(self, validated_data):
		return Tweet(id=None, **validated_data)

	def update(self, instance, validated_data):
		for field in validated_data.items():
			setattr(instance, field, value)
		return instance

class TweepyViewSet(ViewSet):

	serializer_class = TweetSerializer

	def list(self, request):
		
		auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_token, access_token_secret)

		api = tweepy.API(auth, parser = tweepy.parsers.JSONParser())
		# api = tweepy.API(auth)

		# public_tweets = api.home_timeline()

		results1 = api.search(q="-filter:retweets",geocode='28.7041,77.1025,10km', rpp=100)
		# results2 = api.search(q="happy OR glad  -filter:retweets",geocode='28.7041,77.1025,10km', rpp=100)
# 
		print results1




		serializer = TweetSerializer(
			instance = tweets.values(), many=True)
		return HttpResponse(json.dumps(results1))
