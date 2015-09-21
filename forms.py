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
    heartbeat = forms.BooleanField(
        label='Disable Heartbeat Userrating',
        help_text='With Firefox 37, Mozilla integrated the <a href="https://wiki.mozilla.org/Advocacy/heartbeat">Heartbeat</a> '
            'system to ask users from time to time about their experience with firefox.',
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
            if self.cleaned_data['heartbeat']:
                config['browser.selfsupport.url '] = ""
        return config, []


class FirefoxTrackingForm(forms.Form):
    id="firefox_tracking"
    name="Firefox Tracking"
    form_name = forms.CharField(initial="firefox_tracking", widget=forms.widgets.HiddenInput)
    telemetry = forms.BooleanField(
        label="Disable Telemetry",
        help_text='The <a href="https://support.mozilla.org/en-US/kb/share-telemetry-data-mozilla-help-improve-firefox">telemetry feature</a> '
            'sends data about the performance and responsiveness of firefox to mozilla.',
        initial=True, required=False)
    health_report = forms.BooleanField(
        label="Disable health report",
        help_text='Disable sending <a href="https://www.mozilla.org/en-US/privacy/firefox/#health-report">Firefox health reports</a> to mozilla',
        initial=True, required=False)
    addon_data = forms.BooleanField(
        label="Opt out metadata updates",
        help_text='Firefox sends data about installed addons as <a href="https://blog.mozilla.org/addons/how-to-opt-out-of-add-on-metadata-updates/">metadata updates</a>, so mozilla is able to recommend you other addons.',
        initial=True, required=False)
    phishing_protection = forms.BooleanField(
        label="Disable phishing protection",
        help_text='The phishing protection contacts google with an unique key:'
        ' <a href="http://electroholiker.de/?p=1594">wrkey</a>.',
        initial=True, required=False)

    def get_config_and_addons(self):
        config = {}
        if self.is_valid():
            if self.cleaned_data['health_report']:
                config['toolkit.telemetry.enabled'] = False
            if self.cleaned_data['phishing_protection']:
                config['browser.safebrowsing.enabled'] = False
                config['browser.safebrowsing.malware.enabled'] = False
            if self.cleaned_data['health_report']:
                config['datareporting.healthreport.uploadEnabled'] = False
                config['datareporting.healthreport.uploadEnabled'] = False
                config['datareporting.policy.dataSubmissionEnabled'] = False
            if self.cleaned_data['addon_data']:
                config['extensions.getAddons.cache.enabled'] = False
        return config, []


class TrackingForm(forms.Form):
    id="tracking"
    name="Website Tracking"
    form_name = forms.CharField(initial="tracking", widget=forms.widgets.HiddenInput)

    dnt = forms.BooleanField(
        label='Enable Do-not-Track',
        help_text='With the do not track feature, you tell websites, that you do not want to be tracked. '
            'Most websites ignore this, so you need other privacy options as well.',
        initial=True, required=False)
    trackingprotection = forms.BooleanField(
        label='Enable Mozilla Trackingprotection',
        help_text='Firefox has a builtin <a href="https://support.mozilla.org/en-US/kb/tracking-protection-firefox">tracking protection</a>, which blocks a list of known tracking sites.',
        initial=True, required=False)
    ping = forms.BooleanField(
        label='Disable Browser Pings',
        help_text='Firefox sends <a href="http://kb.mozillazine.org/Browser.send_pings">"ping" requests</a>, '
            'when a website requests to be informed when a user clicks on a link.',
        initial=True, required=False)
    beacon = forms.BooleanField(
        label='Disable Beacons',
        help_text='The <a href="https://w3c.github.io/beacon/">Beacon</a> feature allows websites to send tracking data after you left the website.',
        initial=True, required=False)

    def get_config_and_addons(self):
        config = {}
        if self.is_valid():
            if self.cleaned_data['dnt']:
                config['privacy.donottrackheader.enabled'] = True
                config['privacy.donottrackheader.value'] = 1
            if self.cleaned_data['trackingprotection']:
                config['privacy.trackingprotection.enabled'] = True
            if self.cleaned_data['ping']:
                config['browser.send_pings'] = False
            if self.cleaned_data['beacon']:
                config['beacon.enabled'] = False
        return config, []

class PrivacyForm(forms.Form):
    id='privacy'
    name='Privacy'
    form_name = forms.CharField(initial='privacy', widget=forms.widgets.HiddenInput)

    useragent = forms.CharField(
        label='Fake another Useragent',
        help_text='Using a <a href="https://techblog.willshouse.com/2012/01/03/most-common-user-agents/">popular useragent string</a> '
            'avoids to attract attention i.e. with an Iceweasel UA. (keep blank to use the default)',
        initial="", required=False)
    thirdparty_cookies = forms.BooleanField(
        label='Block thirdparty cookies',
        help_text='Block cookies, which are not from the site you\'re visiting. '
            'You will rarely notice that something is missing, but it hugely improves your privacy.',
        initial=True, required=False)
    all_cookies = forms.BooleanField(
        label='Block all cookies',
        help_text='Block all cookies. Many sites will not work without cookies.',
        initial=False, required=False)
    referer = forms.ChoiceField(
        label='Block Referer',
        help_text='Firefox tells a website, from which site you\'re coming '
            '(the so called <a href="http://kb.mozillazine.org/Network.http.sendRefererHeader">referer</a>).',
        choices = [(0, 'Disable'), (1, 'Allow only when clicking a link'), (2, 'Allow for links and loaded images')],
        initial=0, required=False,
    )
    dom_storage = forms.BooleanField(
        label='Disable DOM storage',
        help_text='Disables DOM storage, which enables so called "supercookies". Some modern sites will not fully not work (i.e. missing "save" functions).',
        initial=False, required=False)
    indexed_db = forms.BooleanField(
        label='Disable IndexedDB',
        help_text='<a href="http://www.w3.org/TR/IndexedDB/">IndexedDB</a> is a way, websites can store structured data. This can be '
            '<a href="http://arstechnica.com/apple/2010/09/rldguid-tracking-cookies-in-safari-database-form/">abused for tracking</a>, too. '
            'Disabling may be a problem with some webapps like tweetdeck.',
        initial=True, required=False)
    prefetch = forms.BooleanField(
        label='Disable Link Prefetching',
        help_text='Firefox prefetches the next site on some links, so the site is loaded even when you never click.',
        initial=True, required=False)
    webrtc = forms.BooleanField(
        label='Disable WebRTC',
        help_text='Disables the WebRTC function, which gives away your local ips.',
        initial=True, required=False)
    search_suggest = forms.BooleanField(
        label='Disable Search Suggestions',
        help_text='Firefox suggests search terms in the search field. This will send everything typed or pasted '
            'in the search field to the chosen search engine, even when you did not press enter.',
        initial=False, required=False)
    keyword_search = forms.BooleanField(
        label='Disable Search Keyword',
        help_text='When you mistype some url, firefox starts a search even from urlbar. '
            'This feature is useful for quick searching, but may harm your privacy, when it\'s unintended.',
        initial=False, required=False)
    fixup_url = forms.BooleanField(
        label='Disable Fixup URLs',
        help_text='When you type "something" in the urlbar and press enter, firefox tries "something.com", if Fixup URLs is enabled.',
        initial=False, required=False)

    def get_config_and_addons(self):
        config = {}
        if self.is_valid():
            if self.cleaned_data['useragent']:
                config['general.useragent.override'] = self.cleaned_data['useragent']
            if self.cleaned_data['all_cookies']:
                config['network.cookie.cookieBehavior'] = 2
            elif self.cleaned_data['thirdparty_cookies']:
                config['network.cookie.cookieBehavior'] = 1
            if self.cleaned_data['referer']:
                config['network.http.sendRefererHeader'] = self.cleaned_data['referer']
            if self.cleaned_data['dom_storage']:
                config['dom.storage.enabled'] = False
            if self.cleaned_data['indexed_db']:
                config['dom.indexedDB.enabled'] = False
            if self.cleaned_data['prefetch']:
                config['network.prefetch-next'] = False
                config['network.dns.disablePrefetch'] = True
            if self.cleaned_data['search_suggest']:
                config['browser.search.suggest.enabled'] = False
            if self.cleaned_data['webrtc']:
                config['media.peerconnection.enabled'] = False
            if self.cleaned_data['keyword_search']:
                config['keyword.enabled'] = False
            if self.cleaned_data['fixup_url']:
                config['browser.fixup.alternate.enabled'] = False
        return config, []


class SecurityForm(forms.Form):
    id='security'
    name='Security'
    form_name = forms.CharField(initial='security', widget=forms.widgets.HiddenInput)

    webgl = forms.BooleanField(
        label='Disable WebGL',
        help_text='Disables the WebGL function, to prevent websites from <a href="https://isc.sans.edu/forums/diary/Time+to+disable+WebGL/10867">(ab)using the full power of the graphics card</a>. '
            'Some interactive websites will not work, mostly games.',
        initial=False, required=False)

    def get_config_and_addons(self):
        config = {}
        if self.is_valid():
            if self.cleaned_data['webgl']:
                config['webgl.disabled'] = True
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
    pdfjs = forms.BooleanField(
        label='Disable the Firefox PDF-REader',
        help_text='Mozilla integrated a pdf reader. It works good for a quick preview, but is too slow for reading longer documents.',
        initial=False, required=False)

    def get_config_and_addons(self):
        config = {}
        if self.is_valid():
            if self.cleaned_data['pocket']:
                config['browser.pocket.enabled'] = False
            if self.cleaned_data['hello']:
                config['loop.enabled'] = False
            if self.cleaned_data['pdfjs']:
                config['pdfjs.disabled'] = True
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
