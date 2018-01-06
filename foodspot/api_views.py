from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from braces.views import CsrfExemptMixin
from rest_framework import permissions
from rest_framework import status
from django.conf import settings
from serializers import (
		UserSerializer, 
		LocationSerializer, 
		FoodSpotSerializer, 
		UserSerializerForPut, 
		UserSerializerForPublicGet,
		FoodSpotVoteSerializer,
		FoodSpotCommentSerializer
	)
import foodspot.constants as constants
from models import User, Location, FoodSpot, FoodSpotVote, FoodSpotComment
from permissions import IsCreationOrIsAuthenticated, IsAuthenticated, IsOwnerOrReadOnly
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from django.utils.translation import ugettext as _
from pyfcm import FCMNotification


class UserViewSet(viewsets.ModelViewSet):

	queryset = User.objects.all()
	serializer_class = UserSerializer
	permission_classes = (IsCreationOrIsAuthenticated, IsOwnerOrReadOnly)

	def get_serializer_class(self):

		serializer_class = self.serializer_class

		if self.request.method == 'PUT':
			serializer_class = UserSerializerForPut
		elif self.request.method == 'GET' and not self.request.user.is_staff:
			serializer_class = UserSerializerForPublicGet

		return serializer_class

	def get_permissions(self):

		if self.request.method == 'DELETE':
			return [permissions.IsAdminUser()]
		return super(UserViewSet, self).get_permissions()



class FoodSpotViewSet(viewsets.ModelViewSet):
	queryset = FoodSpot.objects.all()
	serializer_class = FoodSpotSerializer
	permission_classes = (IsOwnerOrReadOnly,IsAuthenticated)

	#override perform_create method to pass current logged in user as owner of the entity
	def perform_create(self, serializer):
		#create method of the serializer will now receive additional fields 'owner', 'gallery' in validated_data dict
		serializer.save(owner=self.request.user, gallery = self.request.FILES)

	def get_queryset(self):
		queryset = FoodSpot.objects.all()
		username = self.request.query_params.get('username', None)
		if(username is not None):
			queryset = queryset.filter(owner__username = username)
		return queryset

	@list_route(url_path='search', permission_classes=(IsAuthenticated,))
	def search(self, request):
		return self.list(request)

	@list_route(url_path='travel', permission_classes=(IsAuthenticated,))
	def travel(self, request):
		errors = {}
		lat = request.query_params.get('lat')
		lng = request.query_params.get('lng')
		firebaseId = request.query_params.get('firebaseId')
		if lat is None:
			errors['lat'] = 'lat is required'
		if lng is None:
			errors['lng'] = 'lng is required'
		if firebaseId is None:
			errors['firebaseId'] = 'firebaseId is required'
		if len(errors) is not 0:
			return Response(errors,status=status.HTTP_400_BAD_REQUEST)

		if not request.user.hasTravelled(lat, lng):
			return Response({'detail' : 'user not travelled' },status=status.HTTP_200_OK)

		pushService = FCMNotification(api_key = constants.FCM_SERVER_KEY)
		data = {
			"title" : "Wandoof",
			"message" : "Checkout this place nearby!",
			"foodspot" : 1,
			"image" : "http://c8.alamy.com/comp/CEB75Y/vans-good-food-shop-in-middleton-street-llandrindod-wells-CEB75Y.jpg"
		}
		result = pushService.notify_single_device(registration_id = firebaseId, data_message = data)
		return Response({'detail' : 'notification sent' },status=status.HTTP_200_OK)

	# override default 'list' APIView method to get list of FoodSpots
	def list(self, request):
	 	"""
    		lat -- User latitude
    		lng -- User longitude
    		maxDistance -- maximum distance allowed b/w user and the foodspots
    		keyword -- Search Keyword
    	""" 
		
		lat = request.query_params.get('lat')
		lng = request.query_params.get('lng')
		maxDistance = request.query_params.get('maxDistance')
		maxDistance = maxDistance if maxDistance is not None else constants.DEFAULT_MAX_DISTANCE
		keyword = request.query_params.get('keyword')
		username = request.query_params.get('username')

		if username is None:
			if lat is None or lng is None:
				return Response({ 'error' : 'lat and lng fields are both required'},status=status.HTTP_400_BAD_REQUEST)
			foodspots = FoodSpot.objects.nearby(lat,lng,maxDistance)
		else:
			foodspots = FoodSpot.objects.filter(owner__username = username)

		page = self.paginate_queryset(foodspots)
		if page is not None:
			serializer = self.get_serializer(page, many=True)
			return self.get_paginated_response(serializer.data)
		serializer = self.get_serializer(foodspots, many=True)
		return Response(serializer.data)


class FoodSpotVoteViewSet(viewsets.ModelViewSet):
 	queryset = FoodSpotVote.objects.all()
 	serializer_class = FoodSpotVoteSerializer
 	permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)

 	def perform_create(self, serializer):
 		print self.request.user.username
 		serializer.save(owner = self.request.user)

class FoodSpotCommentViewSet(viewsets.ModelViewSet):
	queryset = FoodSpotComment.objects.all()
	serializer_class = FoodSpotCommentSerializer
	permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)

	def perform_create(self, serializer):
		serializer.save(owner = self.request.user)

