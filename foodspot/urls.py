from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.authtoken import views as rest_framework_authtoken_views
from django.conf import settings
import foodspot.views as views, foodspot.api_views as api_views
import foodspot.tweepyViews as tweepyViews
from django.conf.urls.static import static

apiRouter = routers.DefaultRouter()
apiRouter.register(r'users', api_views.UserViewSet)
apiRouter.register(r'foodspots/vote', api_views.FoodSpotVoteViewSet)
apiRouter.register(r'foodspots/comment', api_views.FoodSpotCommentViewSet)
apiRouter.register(r'foodspots', api_views.FoodSpotViewSet)
apiRouter.register(r'tweepy', tweepyViews.TweepyViewSet, base_name="tweepy")



urlpatterns = [
	# url(r'^api/tweepy', tweepyViews.TweepyView.as_view()),
	url(r'^api/login/', rest_framework_authtoken_views.obtain_auth_token),
	# url(r'^api/logout/', api_views.Logout.as_view()),
	url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
	url(r'^api/', include(apiRouter.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)