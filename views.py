from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from forms import *
from django import forms


def get_forms(request, FormClasses):

    forms = []
    invalid_data = False
    for i in range(len(FormClasses)):
        FormClass = FormClasses[i]
        name = FormClass.id
        session_data = request.session.get(name+"_data", None)
        if request.POST.get("form_name", "") == name:
            post_data = request.POST
            form = FormClass(post_data)
            if not form.is_valid():
                invalid_data = True
            # we save the invalid data anyway,
            # so the state which forms were valid is correct
            request.session[name+"_data"] = post_data
        else:
            form = FormClass(session_data)
        if not i == len(FormClasses) -1:  # last item
            form.next = FormClasses[i+1].id
        else:
            form.next = "finish"
        forms.append(form)
    return forms, invalid_data

def main(request):
    forms, invalid_data = get_forms(request,
        [PrivacyForm, BloatwareForm, AnnoyancesForm, FeaturesForm])

    # are all forms finished?
    finished = True
    for form in forms:
        if not form.is_valid():
            finished = False
            break

    if request.POST:
        # start over again
        if request.POST.get("reset", None) == "reset":
            request.session.clear()

        # redirect to the current form or to the next one?
        next = request.POST.get("next", "")
        form_name = request.POST.get("form_name", "")
        if next and not invalid_data:
            return redirect(reverse(main) + "#" + next)
        else:
            return redirect(reverse(main) + "#" + form_name)
    else:
        # nothing posted, just render the current page
        return render(request, "main.html", {
            'forms': forms,
            'finished': finished
        })
