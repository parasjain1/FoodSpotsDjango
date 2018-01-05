from django.utils import timezone
from django.conf import settings
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from models import (
		User, 
		Location, 
		FoodSpot, 
		FoodSpotImage,
		FoodSpotVote,
		FoodSpotComment
	)

# from django.contrib.gis.geos import Point

# for POST requests
class UserSerializer(serializers.ModelSerializer):
	numFoodSpots = serializers.SerializerMethodField()
	email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
	class Meta:
		model = User
		fields = ('id','username', 'email', 'password', 'numFoodSpots', 'fullName')
		extra_kwargs = {'password' : {'write_only' : True }, 'fullName' : {'required' : True } , 'email' : { 'required' : True }}

	def get_numFoodSpots(self, instance):
		return FoodSpot.objects.filter(owner = instance).count()

	def create(self, validated_data):
		user = User(
			email = validated_data['email'],
			username = validated_data['username'],
			fullName = validated_data['fullName']
		)
		user.set_password(validated_data['password'])
		user.save()
		return user


# user serializer class for PUT requests, excludes username field
class UserSerializerForPut(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id','email', 'password')
		extra_kwargs = {'password' : {'write_only' : True }, 'fullName' : {'required' : True } , 'email' : { 'required' : True }}

# user serializer class for public GET requests, excludes email and password field
class UserSerializerForPublicGet(serializers.ModelSerializer):
	numFoodSpots = serializers.SerializerMethodField()
	class Meta:
		model = User
		fields = ('id', 'username', 'numFoodSpots', 'fullName')
	def get_numFoodSpots(self, instance):
		return FoodSpot.objects.filter(owner = instance).count()


class LocationSerializer(serializers.ModelSerializer):
	class Meta:
		model = Location
		exclude = ('owner',)

class FoodSpotCommentSerializer(serializers.ModelSerializer):
	created_date_time = serializers.SerializerMethodField()
	class Meta:
		model = FoodSpotComment
		read_only = ('owner')
		extra_kwargs = {'text' : {'required' : True}, 'foodSpot' : {'required' : True} }
	def get_created_date_time(self, instance):
		return timezone.localtime(instance.timestamp)

class FoodSpotVoteSerializer(serializers.ModelSerializer):
	created_date_time = serializers.SerializerMethodField()
	class Meta:
		model = FoodSpotVote
		read_only = ('owner', 'value')
		extra_kwargs = {'value' : {'required' : True}, 'foodSpot' : {'required' : True}, 'owner' : {'required' : False} }

	def get_created_date_time(self, instance):
		return timezone.localtime(instance.timestamp)

	def create(self, validated_data):	#validated_data has field 'owner' set by the save method.
		return FoodSpotVote.objects.create(**validated_data)

class FoodSpotImageSerializer(serializers.ModelSerializer):
	class Meta:
		model = FoodSpotImage
		exclude = ('foodSpot', )

# refer http://blog.karolmajta.com/parsing-query-parameters-in-rest-framework/
# class FoodSpotQueryParamExpectations(serializers.Serializer):
# 	lat = fields.FloatField()
# 	lng = fields.FloatField()

class FoodSpotSerializer(serializers.ModelSerializer):
	location = LocationSerializer()
	# owner = UserSerializerForPublicGet()
	# since FoodSpot doesn't have a gallery field, we define a MethodField 'gallery' and fill it via the 'fill_gallery' serializer method
	# method name defaults to 'get_gallery' if not specified 
	gallery = serializers.SerializerMethodField('fill_gallery')
	recentLikes = serializers.SerializerMethodField()
	recentDislikes = serializers.SerializerMethodField()
	numLikes = serializers.SerializerMethodField()
	numDislikes = serializers.SerializerMethodField()
	comments = serializers.SerializerMethodField()
	created_date_time = serializers.SerializerMethodField()
	class Meta:
		model = FoodSpot
		fields = '__all__'
		read_only = ('location', 'approved')
<<<<<<< HEAD
		# extra_kwargs = { 'owner' : {'read_only' : True}}
=======
		# extra_kwargs = { 'owner' : {'read_only' : True, 'required' : False}}
>>>>>>> c3fb6e09cd204e042b44f20af650c8e7daecf45c

	'''
	 fill_gallery : method to fill gallery field during GET request
	 Return : returns serialized list of FoodSpotImage instances
 	'''
	def fill_gallery(self, instance):
		return [FoodSpotImageSerializer(foodSpotImage).data for foodSpotImage in instance.gallery.all()]

	def get_recentLikes(self, instance):
		return [FoodSpotVoteSerializer(foodSpotVote).data for foodSpotVote in instance.votes.filter(value = 1).order_by('-id')]

	def get_recentDislikes(self, instance):
		return [FoodSpotVoteSerializer(foodSpotVote).data for foodSpotVote in instance.votes.filter(value = -1).order_by('-id')]

	def get_numLikes(self, instance):
		return instance.votes.filter(value = 1).count()

	def get_numDislikes(self, instance):
		return instance.votes.filter(value = -1).count()

	def get_comments(self, instance):
		return [FoodSpotCommentSerializer(foodSpotComment).data for foodSpotComment in instance.comments.order_by('-id')]

	def get_created_date_time(self, instance):
		return timezone.localtime(instance.timestamp)
		

	def create(self, validated_data):	#validated_data has field 'owner' set by the save method.
		locationData = validated_data.pop('location')	# extract location data
		gallery = validated_data.pop('gallery')	# extract gallery data [Image files uploaded during create request]

		# point = Point(locationData['lng'], locationData['lat'])

		# create location object to pass to FoodSpot create
		location = Location.objects.create(owner = validated_data['owner'], **locationData)	#create location object, passing owner excplicitly from the dict
		# create FoodSpot instance 
		foodSpot = FoodSpot.objects.create(location = location, **validated_data) # create foodSpot object, owner is already present in validated data

		# for each uploaded image file, create a FoodSpotImage instance
		for image in gallery:
			FoodSpotImage.objects.create(foodSpot = foodSpot, image = gallery[image])

		return foodSpot


