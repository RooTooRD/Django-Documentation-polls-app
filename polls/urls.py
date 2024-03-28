from django.urls import path
from . import views

app_name = "polls"

urlpatterns = [
    path('', views.index.as_view(), name="index"),
    path('<int:pk>/', views.detail.as_view(), name="detail"),
    path('<int:pk>/result', views.result.as_view(), name="result"),
    path('<int:question_id>/vote', views.action, name="vote"),
]