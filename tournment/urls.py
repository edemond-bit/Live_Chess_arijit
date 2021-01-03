from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet, basename='user')
# router.register(r'tournament', views.LeaveViewSet, basename='tournament')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('api1/', include(router.urls)),
    path('get_all/', views.TournamentViewSet, name="tournament"),
]