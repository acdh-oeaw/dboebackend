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
from rest_framework_swagger.views import get_swagger_view


schema_view = get_swagger_view(title='DBÖ annotation service rest api')

router = routers.DefaultRouter()
router.register(r'users', api_views.UserViewSet)
router.register(r'categories', api_views.CategoryViewSet)
router.register(r'tags', api_views.TagViewSet)
router.register(r'documents', api_views.Es_documentViewSet)
router.register(r'collections', api_views.CollectionViewSet)
router.register(r'annotations', api_views.AnnotationViewSet)
router.register(r'lemmas', api_views.LemmaViewSet)
router.register(r'author_artikel', api_views.AutorArtikelViewSet)
router.register(r'article_edits', api_views.EditOfArticleViewSet)

urlpatterns = [
	path('admin/', admin.site.urls),
	path('api/', include(router.urls)),
	path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
	path('api-token-auth/', views.obtain_auth_token),
    path('authenticate/', api_views.CustomObtainAuthToken.as_view()),
    path('project-info/', api_views.project_info),
	path('version/', api_views.version_info),
	#path('', include_docs_urls(title='DBÖ annotation service rest api')),
	path('', schema_view),
	path('api/dboe-query/', api_views.dboe_query),
]
