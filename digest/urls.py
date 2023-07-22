from django.urls import path
from . import views

urlpatterns = [
    path('digest/', views.CreateDigestView.as_view()),
]
