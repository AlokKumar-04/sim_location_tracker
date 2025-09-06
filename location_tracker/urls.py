from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'location_tracker'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('api/search/', views.LocationSearchView.as_view(), name='search'),
    path('api/search/<int:search_id>/', views.get_search_result, name='search_result'),
    path(
        'accounts/login/',
        auth_views.LoginView.as_view(template_name="login.html"),
        name='login'
    ),
]