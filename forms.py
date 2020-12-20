from django import forms
from django.utils.translation import ugettext as _
import json, glob, os

from .merge import merge


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
                    choices = list(zip(list(range(len(choices))), choices)),
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
        enterprise_policy = {}
        if self.is_valid():
            for option in self.options:
                if option['type'] == "boolean":
                    if self.cleaned_data[option['name']]:
                        for key in option['config']:
                            config[key] = option['config'][key]
                        addons += option.get('addons', [])
                        if 'files_inline' in option:
                            files_inline.update(option['files_inline'])
                        enterprise_policy = merge(enterprise_policy, option.get('enterprise_policy', {}))
                elif option['type'] == "choice":
                    choice = int(self.cleaned_data[option['name']])
                    for key in option['config'][choice]:
                        config[key] = option['config'][choice][key]
                    if "addons" in option:
                        addons += option['addons'][choice]
                    if 'files_inline' in option:
                        files_inline.update(option['files_inline'][choice])
                    enterprise_policy = merge(enterprise_policy, option.get('enterprise_policy', {}))
                elif option['type'] == "text":
                    if option.get('blank_means_default', False) and self.cleaned_data[option['name']] == "":
                        continue
                    else:
                        config[option['setting']] = self.cleaned_data[option['name']]
                    # TODO: support text fields for enterprise policies

        return config, addons, files_inline, enterprise_policy

def create_configform(id, name, options):
    class DynamicConfigForm(ConfigForm):
        pass
    DynamicConfigForm.id=id
    DynamicConfigForm.name=name
    DynamicConfigForm.options=options
    return DynamicConfigForm


PROFILES = {}
settings_path = os.path.dirname(__file__) + "/settings"
profiles_path = os.path.dirname(__file__) + "/profiles"
profile_files = glob.glob(profiles_path + "/*.json")
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
                if item.get("enterprise_policy_only", False):
                    if item.get('help_text'):
                        item['help_text'] += "<br />"
                    item['help_text'] += "<i>" + _("(enterprise policy download only)") + "</i>"
            options += data
        items[category] = options
    form_list = []
    for idx, name in enumerate(items):
        form_list.append(create_configform(id="form{0:d}".format(idx), name=name, options=items[name]))
    PROFILES[os.path.basename(profile_file)] = [profile_name, form_list]
