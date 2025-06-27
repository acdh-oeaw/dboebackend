from django.urls import path

from belege.views import BelegDetailView

app_name = "belege"

urlpatterns = [
    path("<str:pk>/", BelegDetailView.as_view(), name="beleg-detail"),
]
