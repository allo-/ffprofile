from django.shortcuts import render
from forms import *
from django import forms


def get_form(request, FormClass):

    name = FormClass.id
    data = request.session.get(name+"_data", None)
    print "posted name", request.POST.get("form_name", "")
    print "name", name
    if request.POST.get("form_name", "") == name:
        data = request.POST
        print "post", name
    form = FormClass(data)
    if form.is_valid():
        request.session[name+"_data"] = data
    return form

def main(request):
    annoyances_form = get_form(request, AnnoyancesForm)
    privacy_form = get_form(request, PrivacyForm)
    features_form = get_form(request, FeaturesForm)
    bloatware_form = get_form(request, BloatwareForm)
    forms = [privacy_form, bloatware_form, annoyances_form, features_form]
    finished = True
    for form in forms:
        if not form.is_valid():
            finished = False
            break

    return render(request, "main.html", {
        'forms': forms,
        'finished': finished
    })
