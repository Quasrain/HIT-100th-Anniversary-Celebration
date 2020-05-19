from django.conf.urls import url
from . import views
 
urlpatterns = [
    url('addComment', views.addComment),
    url('selectComment', views.selectComment),
    url('lottery', views.lottery),
    url('like', views.like)
]