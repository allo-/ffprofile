from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from forms import *
from django import forms
from django.http import HttpResponse
import os
import zipfile
from StringIO import StringIO


FORMS = [FirefoxTrackingForm, TrackingForm, PrivacyForm, SecurityForm,
         BloatwareForm, AnnoyancesForm, FeaturesForm]

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
    forms, invalid_data = get_forms(request, FORMS)

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

def download(request):
    forms, invalid_data = get_forms(request, FORMS)
    prefsjs_only = request.POST.get("prefsjs_only", False)

    if invalid_data:
        return redirect(reverse(main) + "#finish")

    config = {}
    addons = []
    for form in forms:
        form_config, form_addons = form.get_config_and_addons()
        for key in form_config:
            config[key] = form_config[key]
        addons += form_addons

    memoryFile = StringIO()

    prefs = ""
    if addons and not prefsjs_only:
        config['extensions.autoDisableScopes'] = 0  # allow preinstalled addons
    for key in config:
        value = config[key]
        if isinstance(value, basestring):
            value = '"{0}"'.format(value)
        elif isinstance(value, bool):
            value = "true" if value else "false"
        else:
            value = str(value)
        prefs += 'user_pref("{key}", {value});\r\n'.format(key=key, value=value)

    if not prefsjs_only:
        zip_file = zipfile.ZipFile(memoryFile, "w", zipfile.ZIP_DEFLATED)
        zip_file.writestr("prefs.js", prefs, compress_type=zipfile.ZIP_DEFLATED)

        for addon in addons:
            zip_file.write(os.path.join("extensions", addon),
                compress_type=zipfile.ZIP_DEFLATED)
        zip_file.close()

        memoryFile.seek(0)
        response = HttpResponse(memoryFile.read(), content_type="application/zip")
        response['Content-Disposition'] = 'attachment; filename="profile.zip"'
    else:
        response = HttpResponse(prefs, content_type="text/plain")
        response['Content-Disposition'] = 'attachment; filename="prefs.js"'

    return response
