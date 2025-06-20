import requests

from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout

from webpage.forms import form_user_login


class ImprintView(TemplateView):
    template_name = "webpage/imprint.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            imprint_url = f"{settings.ACDH_IMPRINT_URL}{settings.REDMINE_ID}"
        except Exception as e:
            context["imprint_body"] = e
            return context
        r = requests.get(imprint_url)
        if r.status_code == 200:
            context["imprint_body"] = f"{r.text}"
        else:
            context[
                "imprint_body"
            ] = """
            On of our services is currently not available.\
            Please try it later or write an email to\
            acdh-ch-helpdesk@oeaw.ac.at; if you are service provide,\
            make sure that you provided ACDH_IMPRINT_URL and REDMINE_ID
            """
        return context


class GenericWebpageView(TemplateView):
    template_name = "webpage/index.html"

    def get_context_data(self, **kwargs):
        context = super(GenericWebpageView, self).get_context_data(**kwargs)
        context["apps"] = settings.INSTALLED_APPS
        return context

    def get_template_names(self):
        template_name = "webpage/{}.html".format(self.kwargs.get("template", "index"))
        try:
            loader.select_template([template_name])
            template_name = "webpage/{}.html".format(
                self.kwargs.get("template", "index")
            )
        except NameError:
            template_name = "webpage/index.html"
        return [template_name]


#################################################################
#               views for login/logout                          #
#################################################################


def user_login(request):
    if request.method == "POST":
        form = form_user_login(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd["username"], password=cd["password"])
            if user and user.is_active:
                login(request, user)
                return HttpResponseRedirect(request.GET.get("next", "/"))
            return HttpResponse("user does not exist")
    else:
        form = form_user_login()
        return render(request, "webpage/user_login.html", {"form": form})


def user_logout(request):
    logout(request)
    return render(request, "webpage/user_logout.html")


def handler404(request, exception):
    return render(request, "webpage/404-error.html", locals())
