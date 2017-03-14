from django import forms
from django.utils.translation import ugettext as _
import json, glob, os

# current structure:
# - FirefoxTracking: builtin features, which send data to Mozilla,
#   google and other thirdparties
# - WebsiteTracking: Features, which are made for tracking (i.e. ping, beacons)
#   or may used for it (i.e. battery api)
# - Privacy: General privacy related settings like referer, cookies, etc.
#   which may be harmless or needed (i.e. cookies)
# - Security: No direct privacy problems, but maybe security issues
#   (i.e. webgl may hang Firefox)
# - Bloatware: Settings, which disable unwanted features like hello or pocket
# - Annoyances: Settings, which disable first-run
#   "did you know, here is our new tab page" popups.
#
# TODO: WebsiteTracking could be split into Tracking (ping, beacon, ...) and
#       Fingerprinting (battery, canvas, ...), when there are more settings.



class ConfigForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ConfigForm, self).__init__(*args, **kwargs)
        self.fields['form_name'] = forms.CharField(initial=self.id, widget=forms.widgets.HiddenInput)
        for option in self.options:
            if option['type'] == "boolean":
                self.fields[option['name']] = forms.BooleanField(
                    label=option['label'],
                    help_text=option['help_text'],
                    initial=option['initial'], required=False)
            if option['type'] == "choice":
                choices = option['choices']
                self.fields[option['name']] = forms.ChoiceField(
                    label=option['label'],
                    help_text=option['help_text'],
                    choices = zip(range(len(choices)), choices),
                    initial=option['initial'], required=False)
            elif option['type'] == "text":
                self.fields[option['name']] = forms.CharField(
                    label=option['label'],
                    help_text=option['help_text'],
                    initial=option['initial'], required=False)

    def get_config_and_addons(self):
        config = {}
        addons = []
        files_inline = {}
        if self.is_valid():
            for option in self.options:
                if option['type'] == "boolean":
                    if self.cleaned_data[option['name']]:
                        for key in option['config']:
                            config[key] = option['config'][key]
                        addons += option['addons']
                        if 'files_inline' in option:
                            files_inline.update(option['files_inline'])
                elif option['type'] == "choice":
                    choice = int(self.cleaned_data[option['name']])
                    for key in option['config'][choice]:
                        config[key] = option['config'][choice][key]
                    addons += option['addons'][choice]
                    if 'files_inline' in option:
                        files.update(option['files_inline'][choice])
                elif option['type'] == "text":
                    if option.get('blank_means_default', False) and self.cleaned_data[option['name']] == "":
                        continue
                    else:
                        config[option['setting']] = self.cleaned_data[option['name']]

        return config, addons, files_inline

def create_configform(id, name, options):
    class DynamicConfigForm(ConfigForm):
        pass
    DynamicConfigForm.id=id
    DynamicConfigForm.name=name
    DynamicConfigForm.options=options
    return DynamicConfigForm


PROFILES = {}
settings_path = os.path.dirname(__file__) + "/settings"
profile_files = glob.glob(settings_path + "/*.profile.json")
for profile_file in profile_files:
    profile_name, profile = json.load(open(profile_file, "r"))
    items = {}
    for category in profile:
        options = []
        for file in profile[category]:
            data = json.load(open(settings_path + "/" + file, "r"))
            for item in data:
                item['label'] = _(item['label'] or "")
                item['help_text'] = _(item['help_text'] or "")
            options += data
        items[category] = options
    form_list = []
    for idx, name in enumerate(items):
        form_list.append(create_configform(id="form{0:d}".format(idx), name=name, options=items[name]))
    PROFILES[os.path.basename(profile_file)] = [profile_name, form_list]
