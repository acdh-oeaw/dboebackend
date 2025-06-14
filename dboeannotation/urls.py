from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from annotations import api_views
from belege import api_views as belege_api_views
from rest_framework.authtoken import views
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)
from django_spaghetti.views import Plate


router = routers.DefaultRouter()
router.register(r"users", api_views.UserViewSet)
router.register(r"categories", api_views.CategoryViewSet)
router.register(r"tags", api_views.TagViewSet)
router.register(r"documents", api_views.Es_documentViewSet)
router.register(r"collections", api_views.CollectionViewSet)
router.register(r"annotations", api_views.AnnotationViewSet)
router.register(r"lemmas", api_views.LemmaViewSet)
router.register(r"author_artikel", api_views.AutorArtikelViewSet)
router.register(r"article_edits", api_views.EditOfArticleViewSet)
router.register(r"bundeslaender", belege_api_views.BundesLandViewSet)
router.register(r"gregionen", belege_api_views.GRegionViewSet)
router.register(r"kregionen", belege_api_views.KRegionViewSet)
router.register(r"orte", belege_api_views.OrtViewSet)
router.register(r"belege", belege_api_views.BelegViewSet)
router.register(r"zitate", belege_api_views.CitationViewSet)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("api-token-auth/", views.obtain_auth_token),
    path("authenticate/", api_views.CustomObtainAuthToken.as_view()),
    path("project-info/", api_views.project_info),
    path("api/dboe-query/", api_views.dboe_query),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("data-model/", Plate.as_view()),
]
