from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone
from django.db.models.expressions import RawSQL
# from django.contrib.gis.db import models as gisModels

import foodspot.helpers as helpers
import foodspot.constants as constants
import math


# Create your models here.

class UserLocation(models.Model):
	user = models.OneToOneField('User', related_name = 'lastLocation', unique = True)
	lat = models.FloatField()
	lng = models.FloatField()
	

class User(AbstractUser):
	fullName = models.CharField(max_length = 100, default = "")
	profileImage = models.ImageField(null = True, blank = True, upload_to = helpers.PathAndRenameFile('profiles/images'))
	facebookId = models.TextField(blank = True)
	birthDate = models.DateField(blank = True, null = True)
	credits = models.FloatField(blank = True, null = True)
	# gender = models.BooleanField(blank = True, null = True)
	class Meta:
		unique_together = ('email',)

	def hasTravelled(self, lat, lng):
		lastLocation = UserLocation.objects.filter(user = self).first()
		lat = float(lat)
		lng = float(lng)
		if lastLocation is None:
			UserLocation.objects.create(lat = lat, lng = lng, user = self)
			return True
		gcd = 6371 * math.acos(math.cos(math.radians(lastLocation.lat)) * math.cos(math.radians(lat))* math.cos(math.radians(lng) - math.radians(lastLocation.lng)) + math.sin(math.radians(lastLocation.lat)) * math.sin(math.radians(lat)))
		if gcd > float(20):
			lastLocation.lat = lat
			lastLocation.lng = lng
			lastLocation.save()
			return True
		else:
			return False


class LikeDislikeManager(models.Manager):
    use_for_related_fields = True
 
    def likes(self):
        # We take the queryset with records greater than 0
        return self.get_queryset().filter(vote__gt=0)
 
    def dislikes(self):
        # We take the queryset with records less than 0
        return self.get_queryset().filter(vote__lt=0)
 
    def sum_rating(self):
        # We take the total rating
        return self.get_queryset().aggregate(Sum('vote')).get('vote__sum') or 0


class LocationManager(models.Manager):
	def nearby(self, lat, lng, proximity):

		# distance formula
		gcd = """6371 * acos(cos(radians(%s)) * cos(radians(lat))* cos(radians(lng) - radians(%s)) +sin(radians(%s)) * sin(radians(lat))) """

		# using 'gcd' string in raw sql expression 
		return self.get_queryset()\
         			.exclude(lat = None)\
         			.exclude(lng = None)\
         			.annotate(distance = RawSQL(gcd, (lat,lng,lat)))\
         			.filter(distance__lt=proximity)\
         			.values_list('id', flat = True)\
         			.order_by('distance')


class Location(models.Model):
	objects = LocationManager()
	owner = models.ForeignKey('User', on_delete = models.CASCADE)
	lat = models.FloatField()
	lng = models.FloatField()
	# point = gisModels.PointField(null = True, blank = True, srid = 4326)
	streetAddress = models.CharField(max_length = 200, blank = True)
	city = models.CharField(max_length = 100, default = "Warangal")
	state = models.CharField(max_length = 100, default = "Telangana")
	landmark = models.CharField(max_length = 100, blank = True)
	pincode = models.CharField(max_length = 10, default = 506004)

class FoodSpotImage(models.Model):
	foodSpot = models.ForeignKey('FoodSpot', related_name = 'gallery')
	image = models.ImageField(null = True, blank = True, upload_to= helpers.PathAndRenameFile('foodspots'))


class FoodSpotVote(models.Model):
	class Meta:
		unique_together = ('owner', 'foodSpot')

	choices = (
		(-1, 'Dislike'),
		(1, 'Like'))
	value = models.SmallIntegerField(choices = choices, blank = True)
	owner = models.ForeignKey('User', blank = True, null = True)
	foodSpot = models.ForeignKey('FoodSpot', related_name='votes', blank = True)
	timestamp = models.DateTimeField(default = timezone.now, editable = False)

class FoodSpotComment(models.Model):
	text = models.CharField(max_length=1000)
	owner = models.ForeignKey('User', blank = True, default=User.objects.get(pk=1))
	foodSpot = models.ForeignKey('FoodSpot', related_name='comments')	
	timestamp = models.DateTimeField(default = timezone.now, editable = False)


class FoodSpotManager(models.Manager):
	def nearby(self, lat, lng, proximity):
		# get nearby locations ordered by increasing distance
		locationIds = Location.objects.nearby(lat,lng,proximity)	

		return self.get_queryset()\
					.filter(location__id__in = locationIds)

class FoodSpot(models.Model):
	objects = FoodSpotManager()
	owner = models.ForeignKey('User', on_delete = models.CASCADE, blank=True, null = True, default = User.objects.filter(pk=1).first())
	name = models.CharField(max_length = 100)
	rating = models.FloatField(null = True, blank = True)
	location = models.ForeignKey('Location', on_delete = models.CASCADE)
	contact = models.CharField(max_length=15, blank = True, null = True)
	description = models.CharField(max_length=2000, blank = True, null = True)
	timestamp = models.DateTimeField(default = timezone.now, editable = False)
	approved = models.BooleanField(default = False)
	preApproved = models.BooleanField(default = False)
	speciality = models.CharFied(max_length = 100, null = True, blank = True)
	nonVeg = models.BooleanField(default = False)
	veg = models.BooleanField(default = False)
	ownerRating = models.CharField(max_length=20, null = True, blank = True)
	openTime = models.TimeField(null = True, blank = True)
	closeTime = models.TimeField(null = True, blank = True)

	@staticmethod
	def post_save(sender, **kwargs):
		instance = kwargs.get('instance')
		created = kwargs.get('created')
		# check if the foodspot entry was just approved and add credits to owner's instance
		if instance.approved and instance.preApproved != instance.approved:
			owner = instance.owner
			owner.credits += constants.credits_per_new_foodspot;
	
	@staticmethod
	def remember_state(sender, **kwargs):
		instance = kwargs.get('instance')
		instance.previous_state = instance.state
	