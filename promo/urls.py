from django.urls import path
from . import views


urlpatterns = [
    path('', views.PromoGenerationView.as_view(), name='new.index'),
]