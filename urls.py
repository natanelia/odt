from django.conf.urls import url, include
from odt.api import router
from odt.api.views import *
from odt import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^__model-sync__/', model_sync),
    url(r'^generate-config/', views.generate_config, name='odt.views.generate_config'),
]