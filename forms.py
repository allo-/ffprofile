from django import forms


class AnnoyancesForm(forms.Form):
    id='annoyances'
    name='Annoyances'
    form_name = forms.CharField(initial='annoyances', widget=forms.widgets.HiddenInput)

    newtabpage_intro = forms.BooleanField(
        label='Disable new tab page intro',
        help_text='Disable the intro to the newtab page on the first run',
        initial=True, required=False)
    pocket_intro = forms.BooleanField(
        label='Disable pocket intro',
        initial=True, required=False)
    aboutconfig_warning = forms.BooleanField(
        label='Disable about:config warning',
        initial=True, required=False)
    default_browser = forms.BooleanField(
        label='Disable checking if Firefox is the default browser',
        initial=True, required=False)

    def get_config_and_addons(self):
        config = {}
        if self.is_valid():
            if self.cleaned_data['newtabpage_intro']:
                config['browser.newtabpage.introShown'] = True
            if self.cleaned_data['pocket_intro']:
                config['browser.toolbarbuttons.introduced.pocket-button'] = True
            if self.cleaned_data['aboutconfig_warning']:
                config['general.warnOnAboutConfig'] = False
            if self.cleaned_data['default_browser']:
                config['browser.shell.checkDefaultBrowser'] = False
        return config, []



class PrivacyForm(forms.Form):
    id="privacy"
    name="Privacy"
    form_name = forms.CharField(initial="privacy", widget=forms.widgets.HiddenInput)
    phishing_protection = forms.BooleanField(
        label="Disable phishing protection",
        help_text='The phishing protection contacts google with an unique key:'
        ' <a href="http://electroholiker.de/?p=1594">wrkey</a>.',
        initial=True, required=False)
    health_report = forms.BooleanField(
        label="Disable health report",
        help_text='Disable sending ''<a href="https://www.mozilla.org/en-US/privacy/firefox/#health-report">Firefox health reports</a> to mozilla',
        initial=True, required=False)

    def get_config_and_addons(self):
        config = {}
        if self.is_valid():
            if self.cleaned_data['phishing_protection']:
                config['browser.safebrowsing.enabled'] = False
                config['browser.safebrowsing.malware.enabled'] = False
            if self.cleaned_data['health_report']:
                config['datareporting.healthreport.uploadEnabled'] = False
        return config, []


class BloatwareForm(forms.Form):
    id="bloatware"
    name="Bloatware"
    form_name = forms.CharField(initial="bloatware", widget=forms.widgets.HiddenInput)
    pocket = forms.BooleanField(
        label='Disable Pocket integration.',
        help_text='For monetizing firefox, mozilla included the '
            '<a href="https://getpocket.com/">Pocket</a> addon by default.',
        initial=False, required=False)
    hello = forms.BooleanField(
        label='Disable Mozilla Hello.',
        help_text='To show what WebRTC can do, mozilla created a VoIP client '
        'called <a href=https://www.mozilla.org/en-US/firefox/hello/"">hello</a>. Most users do not need it.',
        initial=False, required=False)

    def get_config_and_addons(self):
        config = {}
        if self.is_valid():
            if self.cleaned_data['pocket']:
                config['browser.pocket.enabled'] = False
            if self.cleaned_data['hello']:
                config['loop.enabled'] = False
        return config, []


#class FeaturesForm(forms.Form):
#    id="features"
#    name="Useful Features"
#    form_name = forms.CharField(initial="features", widget=forms.widgets.HiddenInput)
#    xclear = forms.BooleanField(
#        label='Install <a href="https://addons.mozilla.org/en-US/firefox/addon/xclear/">xclear</a> extension.',
#        help_text="Adds a little [x] icon to urlbar and searchbar to clear the text.",
#        initial=False, required=False)
#
#    def get_config_and_addons(self):
#        addons = []
#        if self.is_valid():
#            if self.cleaned_data['xclear']:
#                addons = ["xclear.xpi"]
#        return {}, addons
