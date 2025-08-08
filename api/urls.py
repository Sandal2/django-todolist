from django.urls import path
from api.views import MainPageAPIView

app_name = 'api'

urlpatterns = [
    path('dates/', MainPageAPIView.as_view(), name='api_dates',)
]
