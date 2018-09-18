"""dboeannotation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.urls import include, path
	2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from annotations import api_views
from rest_framework.authtoken import views
from rest_framework.documentation import include_docs_urls


router = routers.DefaultRouter()
router.register(r'users', api_views.UserViewSet)
router.register(r'categories', api_views.CategoryViewSet)
router.register(r'documents', api_views.Es_documentViewSet)
router.register(r'collections', api_views.CollectionViewSet)
router.register(r'annotations', api_views.AnnotationViewSet)

urlpatterns = [
	path('admin/', admin.site.urls),
	path('api/', include(router.urls)),
	path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
	path('', include_docs_urls(title='DBÖ annotation service rest api')),
	path('api/es-search/', api_views.es_search),
]
