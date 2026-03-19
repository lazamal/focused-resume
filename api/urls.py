from django.urls import path
from . import views
from .views import AnalyzeCV

urlpatterns = [
    # path('', views.index, name = "index"),
    path('analyze/', AnalyzeCV.as_view(), name='analyze')
]