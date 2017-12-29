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
from models import User, Location, FoodSpot, FoodSpotVote, FoodSpotComment
from permissions import IsCreationOrIsAuthenticated, IsAuthenticated, IsOwnerOrReadOnly
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from django.utils.translation import ugettext as _


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
	permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

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

	# override default 'list' APIView method to get list of FoodSpots
	def list(self, request):
	 	"""
    		lat -- User latitude
    		lng -- User longitude
    		keyword -- Search Keyword
    	""" 
		
		lat = request.query_params.get('lat')
		lng = request.query_params.get('lng')
		username = request.query_params.get('username')

		if username is None:
			if lat is None or lng is None:
				return Response({ 'error' : 'lat and lng fields are both required'},status=status.HTTP_400_BAD_REQUEST)
			foodspots = FoodSpot.objects.nearby(lat,lng,2)
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

