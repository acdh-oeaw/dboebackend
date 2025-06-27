from django.views.generic.detail import DetailView

from belege.models import Beleg


class BelegDetailView(DetailView):
    model = Beleg
    content_type = "application/xml"
    template_name = "belege/beleg_detail.j2"
