from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from forms import *
from django import forms
from django.http import HttpResponse
import os
import zipfile
from StringIO import StringIO



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
        if not i == len(FormClasses) - 1:  # last item
            form.next = FormClasses[i+1].id
        else:
            form.next = "finish"
        forms.append(form)
    return forms, invalid_data


def main(request):
    form_classes = PROFILES.get(request.session.get("profile", sorted(PROFILES)[0]), ["empty", []])[1]
    forms, invalid_data = get_forms(request, form_classes)

    # are all forms finished?
    finished = True
    for form in forms:
        if not form.is_valid():
            finished = False
            break

    if request.POST:
        if request.POST.get("profile", None):
            profile_name = request.POST.get("profile", "default")
            request.session.clear()
            if profile_name in PROFILES:
                request.session['profile'] = profile_name
                form_classes = PROFILES.get(profile_name)[1]
                forms, invalid_data = get_forms(request, form_classes)
            return redirect(reverse(main) + "#" + forms[0].id)
        # start over again
        elif request.POST.get("reset", None) == "reset":
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
        prefs_js, addons, files_inline = generate_prefsjs_and_addonlist(forms, False)
        return render(request, "main.html", {
            'profiles': [(name, PROFILES[name][0]) for name in sorted(PROFILES)],
            'active_profile': request.session.get('profile'),
            'forms': forms,
            'prefs_js': prefs_js,
            'filenames': addons + files_inline.keys(),
            'finished': finished
        })

def generate_prefsjs_and_addonlist(forms, prefsjs_only):
    config = {}
    addons = []
    files_inline = {}
    for form in forms:
        form_config, form_addons, files_inline = form.get_config_and_addons()
        for key in form_config:
            config[key] = form_config[key]
        addons += form_addons
    addons = sorted(addons)

    prefs = ""
    if addons and not prefsjs_only:
        # allow preinstalled addons in the profile
        config['extensions.autoDisableScopes'] = 14
    for key in sorted(config):
        value = config[key]
        if isinstance(value, basestring):
            value = '"{0}"'.format(value)
        elif isinstance(value, bool):
            value = "true" if value else "false"
        else:
            value = str(value)
        prefs += 'user_pref("{key}", {value});\r\n'.format(
            key=key, value=value)

    return prefs, addons, files_inline

def download(request, what):
    form_classes = PROFILES.get(request.session.get("profile", sorted(PROFILES)[0]), ["empty", []])[1]
    forms, invalid_data = get_forms(request, form_classes)
    prefsjs_only = False
    prefsjs_text = False
    addons_only = False
    if what == "prefs.js":
        prefsjs_only = True
    elif what == "prefs.js.txt":
        prefsjs_only = True
        prefsjs_text = True
    elif what == "addons.zip":
        addons_only = True

    if invalid_data:
        return redirect(reverse(main) + "#finish")

    prefs, addons, files_inline = generate_prefsjs_and_addonlist(forms, prefsjs_only)

    if not prefsjs_only:
        memoryFile = StringIO()
        zip_file = zipfile.ZipFile(memoryFile, "w", zipfile.ZIP_DEFLATED)
        if not addons_only:
            zip_file.writestr("prefs.js", prefs,
                              compress_type=zipfile.ZIP_DEFLATED)

        for addon in addons:
            zip_file.write(os.path.join("extensions", addon),
                           compress_type=zipfile.ZIP_DEFLATED)

        for file in files_inline:
            zip_file.writestr(file, files_inline[file],
                              compress_type=zipfile.ZIP_DEFLATED)
        zip_file.close()

        memoryFile.seek(0)
        response = HttpResponse(memoryFile.read(),
                                content_type="application/zip")
        response['Content-Disposition'] = 'attachment; filename="profile.zip"'
    else:
        response = HttpResponse(prefs, content_type="text/plain")
        if prefsjs_text:
            response['Content-Disposition'] = 'filename="prefs.js"'
        else:
            response['Content-Disposition'] = 'attachment; filename="prefs.js"'

    return response
