from django.urls import path
from .views import SearchListView,RatingView
urlpatterns = [
    path('', SearchListView.as_view() , name="search"),
    path('rate/<int:pk>', RatingView.as_view(), name="rating"),
]