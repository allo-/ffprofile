from django import forms
from django.utils.translation import ugettext as _

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
        if self.is_valid():
            for option in self.options:
                if option['type'] == "boolean":
                    if self.cleaned_data[option['name']]:
                        for key in option['config']:
                            config[key] = option['config'][key]
                        addons += option['addons']
                elif option['type'] == "choice":
                    choice = int(self.cleaned_data[option['name']])
                    for key in option['config'][choice]:
                        config[key] = option['config'][choice][key]
                    addons += option['addons'][choice]
                elif option['type'] == "text":
                    config[option['setting']] = self.cleaned_data[option['name']]

        return config, addons

def create_configform(id, name, options):
    class DynamicConfigForm(ConfigForm):
        pass
    DynamicConfigForm.id=id
    DynamicConfigForm.name=name
    DynamicConfigForm.options=options
    return DynamicConfigForm

annoyances_options = [
    {
        'name': 'newtabpage_intro',
        'type': 'boolean',
        'label': _(u'Disable new tab page intro'),
        'help_text': _(u'Disable the intro to the newtab page on the first run'),
        'initial': True,
        'config': 
        {
            'browser.newtabpage.introShown': True
        },
        'addons': []
    },
    {
        'name': 'pocket_intro',
        'type': 'boolean',
        'label': _(u'Disable pocket intro.'),
        'help_text': None,
        'initial': True,
        'config': 
        {
            'browser.toolbarbuttons.introduced.pocket-button': True
        },
        'addons': []
    },
    {
        'name': 'aboutconfig_warning',
        'type': 'boolean',
        'label': _(u'Disable about:config warning.'),
        'help_text': None,
        'initial': True,
        'config': 
        {
            'general.warnOnAboutConfig': False
        },
        'addons': []
    },
    {
        'name': 'default_browser',
        'type': 'boolean',
        'label': _(u'Disable checking if Firefox is the default browser'),
        'help_text': None,
        'initial': True,
        'config': 
        {
            'browser.shell.checkDefaultBrowser': False
        },
        'addons': []
    },
    {
        'name': 'heartbeat',
        'type': 'boolean',
        'label': _(u'Disable Heartbeat Userrating'),
        'help_text': _('With Firefox 37, Mozilla integrated the <a href="https://wiki.mozilla.org/Advocacy/heartbeat">Heartbeat</a> '
            'system to ask users from time to time about their experience with Firefox.'),
        'initial': True,
        'config': 
        {
            'browser.selfsupport.url': ""
        },
        'addons': []
    },
]

AnnoyancesForm = create_configform(id="annoyances", name=_(u'Annoyances'),
    options=annoyances_options)


class FirefoxTrackingForm(forms.Form):
    id = "firefox_tracking"
    name = _(u"Firefox Tracking")
    form_name = forms.CharField(initial="firefox_tracking", widget=forms.widgets.HiddenInput)
    telemetry = forms.BooleanField(
        label=_(u"Disable Telemetry"),
        help_text=_(u'The <a href="https://support.mozilla.org/en-US/kb/share-telemetry-data-mozilla-help-improve-firefox">telemetry feature</a> '
            'sends data about the performance and responsiveness of Firefox to Mozilla.'),
        initial=True, required=False)
    health_report = forms.BooleanField(
        label=_(u"Disable health report"),
        help_text=_(u'Disable sending <a href="https://www.mozilla.org/en-US/privacy/firefox/#health-report">Firefox health reports</a> to Mozilla'),
        initial=True, required=False)
    addon_data = forms.BooleanField(
        label=_(u"Opt out metadata updates"),
        help_text=_(u'Firefox sends data about installed addons as <a href="https://blog.mozilla.org/addons/how-to-opt-out-of-add-on-metadata-updates/">metadata updates</a>, so Mozilla is able to recommend you other addons.'),
        initial=True, required=False)
    phishing_protection = forms.BooleanField(
        label=_(u"Disable phishing protection"),
        help_text=_(u'The phishing protection contacts google with an unique key:'
        ' <a href="http://electroholiker.de/?p=1594">wrkey</a>.'),
        initial=True, required=False)
    newtab_preload = forms.BooleanField(
        label=_(u"Disable preloading of the new tab page."),
        help_text=_(u'By default Firefox preloads the new tab page (with website thumbnails) in the background before it is even opened.'),
        initial=True, required=False)

    def get_config_and_addons(self):
        config = {}
        if self.is_valid():
            if self.cleaned_data['health_report']:
                config['toolkit.telemetry.enabled'] = False
                config['datareporting.healthreport.service.enabled'] = False
                # see https://bugzilla.mozilla.org/show_bug.cgi?id=1195552#c4
                config['datareporting.policy.dataSubmissionEnabled'] = False
            if self.cleaned_data['phishing_protection']:
                config['browser.safebrowsing.enabled'] = False
                config['browser.safebrowsing.malware.enabled'] = False
            if self.cleaned_data['health_report']:
                config['datareporting.healthreport.uploadEnabled'] = False
                config['datareporting.healthreport.uploadEnabled'] = False
                config['datareporting.policy.dataSubmissionEnabled'] = False
            if self.cleaned_data['addon_data']:
                config['extensions.getAddons.cache.enabled'] = False
            if self.cleaned_data['newtab_preload']:
                config['browser.newtab.preload'] = False
        return config, []


class TrackingForm(forms.Form):
    id  ="tracking"
    name = "Website Tracking"
    form_name = forms.CharField(initial="tracking", widget=forms.widgets.HiddenInput)

    dnt = forms.BooleanField(
        label=_(u'Enable Do-not-Track'),
        help_text=_(u'With the do not track feature, you tell websites, that you do not want to be tracked. '
            'Most websites ignore this, so you need other privacy options as well.'),
        initial=True, required=False)
    trackingprotection = forms.BooleanField(
        label=_(u'Enable Mozilla Trackingprotection'),
        help_text=_(u'Firefox has a builtin <a href="https://wiki.mozilla.org/Security/Tracking_protection">tracking protection</a>, which blocks a list of known tracking sites.'),
        initial=True, required=False)
    ping = forms.BooleanField(
        label=_(u'Disable Browser Pings'),
        help_text=_(u'Firefox sends <a href="http://kb.mozillazine.org/Browser.send_pings">"ping" requests</a>, '
            'when a website requests to be informed when a user clicks on a link.'),
        initial=True, required=False)
    beacon = forms.BooleanField(
        label=_(u'Disable Beacons'),
        help_text=_(u'The <a href="https://w3c.github.io/beacon/">Beacon</a> feature allows websites to send tracking data after you left the website.'),
        initial=True, required=False)
    dom_battery = forms.BooleanField(
        label=_(u'Disable the Battery API'),
        help_text=_(u'Firefox allows websites to read the charge level of the battery. This may be used for fingerprinting.'),
        initial=True, required=False)

    def get_config_and_addons(self):
        config = {}
        if self.is_valid():
            if self.cleaned_data['dnt']:
                config['privacy.donottrackheader.enabled'] = True
                config['privacy.donottrackheader.value'] = 1
            if self.cleaned_data['trackingprotection']:
                config['privacy.trackingprotection.enabled'] = True
                config['privacy.trackingprotection.pbmode.enabled'] = True
            if self.cleaned_data['ping']:
                config['browser.send_pings'] = False
            if self.cleaned_data['beacon']:
                config['beacon.enabled'] = False
            if self.cleaned_data['dom_battery']:
                config['dom.battery.enabled'] = False
        return config, []

privacy_options = [
    {
        'name': 'useragent',
        'type': 'text',
        'label': _(u'Fake another Useragent'),
        'help_text': _('Using a <a href="https://techblog.willshouse.com/2012/01/03/most-common-user-agents/">popular useragent string</a> '
            'avoids to attract attention i.e. with an Iceweasel UA. (keep blank to use the default)'),
        'initial': "",
        'setting': 'general.useragent.override',
    },
    {
        'name': 'cookies',
        'type': 'choice',
        'label': _(u'Block Cookies'),
        'help_text': _('Block 3rd-Party cookies or even all cookies.'),
        'initial': 1,
        'choices': [
            "Allow all Cookies",
            "Block Cookies, which are not from the site you\'re visiting. You will rarely notice that something is missing, but it hugely improves your privacy.",
            "Block all Cookies. Many sites will not work without cookies."
        ],
        'config': [
            {
            },
            {
                'network.cookie.cookieBehavior': 1,
            },
            {
                'network.cookie.cookieBehavior': 2,
            },
        ],
        'addons': [[], [], []],
    },
    {
        'name': 'referer',
        'type': 'choice',
        'label': _(u'Block Referer'),
        'help_text': _(u'Firefox tells a website, from which site you\'re coming '
            '(the so called <a href="http://kb.mozillazine.org/Network.http.sendRefererHeader">referer</a>).'),
        'initial': 0,
        'choices': [
            _(u'Always disable referer'),
            _(u'Allow only when clicking a link'),
            _(u'Allow for links and loaded images')
        ],
        'config': [
            {
                'network.http.sendRefererHeader': 0,
            },
            {
                'network.http.sendRefererHeader': 1,
            },
            {
            },
        ],
        'addons': [[], [], []],
    },
    {
        'name': 'dom_storage',
        'type': 'boolean',
        'label': _(u'Disable DOM storage'),
        'help_text': _(u'Disables DOM storage, which enables so called "supercookies". Some modern sites will not fully not work (i.e. missing "save" functions).'),
        'initial': False,
        'config': 
        {
            'dom.storage.enabled': False
        },
        'addons': []
    },
    {
        'name': 'indexed_db',
        'type': 'boolean',
        'label': _(u'Disable IndexedDB'),
        'help_text': _(u'<a href="http://www.w3.org/TR/IndexedDB/">IndexedDB</a> is a way, websites can store structured data. This can be '
            '<a href="http://arstechnica.com/apple/2010/09/rldguid-tracking-cookies-in-safari-database-form/">abused for tracking</a>, too. '
            'Disabling may be a problem with some webapps like tweetdeck.'),
        'initial': True,
        'config': 
        {
            'dom.indexedDB.enabled': False
        },
        'addons': []
    },
    {
        'name': 'prefetch_next',
        'type': 'boolean',
        'label': _(u'Disable Link Prefetching'),
        'help_text': _(u'Firefox prefetches the next site on some links, so the site is loaded even when you never click.'),
        'initial': True,
        'config': 
        {
            'network.prefetch-next': False,
            'network.dns.disablePrefetch': True,
        },
        'addons': []
    },
    {
        'name': 'webrtc',
        'type': 'boolean',
        'label': _(u'Disable WebRTC'),
        'help_text': _(u'Disables the WebRTC function, which gives away your local ips.'),
        'initial': True,
        'config': 
        {
            'media.peerconnection.enabled': False,
        },
        'addons': []
    },
    {
        'name': 'search_suggest',
        'type': 'boolean',
        'label': _(u'Disable Search Suggestions'),
        'help_text': _(u'Firefox suggests search terms in the search field. This will send everything typed or pasted '
            'in the search field to the chosen search engine, even when you did not press enter.'),
        'initial': False,
        'config': 
        {
            'browser.search.suggest.enabled': False,
        },
        'addons': []
    },
    {
        'name': 'search_keyword',
        'type': 'boolean',
        'label': _(u'Disable Search Keyword'),
        'help_text': _(u'When you mistype some url, Firefox starts a search even from urlbar. '
            'This feature is useful for quick searching, but may harm your privacy, when it\'s unintended.'),
        'initial': False,
        'config': 
        {
            'keyword.enabled': False,
        },
        'addons': []
    },
    {
        'name': 'fixup_urls',
        'type': 'boolean',
        'label': _(u'Disable Fixup URLs'),
        'help_text': _(u'When you type "something" in the urlbar and press enter, Firefox tries "something.com", if Fixup URLs is enabled.'),
        'initial': False,
        'config': 
        {
            'browser.fixup.alternate.enabled': False,
        },
        'addons': []
    },
]

PrivacyForm = create_configform(id='privacy', name=_(u'Privacy'), options=privacy_options)


class SecurityForm(forms.Form):
    id = 'security'
    name = _(u'Security')
    form_name = forms.CharField(initial='security', widget=forms.widgets.HiddenInput)

    webgl = forms.BooleanField(
        label=_(u'Disable WebGL'),
        help_text=_(u'Disables the WebGL function, to prevent websites from <a href="https://isc.sans.edu/forums/diary/Time+to+disable+WebGL/10867">(ab)using the full power of the graphics card</a>. '
            'Some interactive websites will not work, mostly games.'),
        initial=False, required=False)
    disable_autoupdate = forms.BooleanField(
        label=_(u'Disable automatic updates.'),
        help_text=_(u'Updates are no longer installed automatically. You will still be notified when an update is available and can install it. Avoids getting a new (maybe addon incompatible) version.'),
        initial=True, required=False)
    disable_updatecheck = forms.BooleanField(
        label=_(u'Disable searching for updates.'),
        help_text=_(u'Disable searching for updates. <b>Caution:</b> You may not notice, when there is an (security) update available.'),
        initial=False, required=False)

    def get_config_and_addons(self):
        config = {}
        if self.is_valid():
            if self.cleaned_data['webgl']:
                config['webgl.disabled'] = True
            if self.cleaned_data['disable_autoupdate']:
                config['app.update.auto'] = False
            if self.cleaned_data['disable_updatecheck']:
                config['app.update.enabled'] = False
        return config, []


bloatware_options = [
    {
        'name': 'pocket',
        'type': 'boolean',
        'label': _(u'Disable Pocket integration.'),
        'help_text': _(u'For monetizing Firefox, Mozilla included the '
            '<a href="https://getpocket.com/">Pocket</a> addon by default.'),
        'initial': False,
        'config': 
        {
            'browser.pocket.enabled': False
        },
        'addons': []
    },
    {
        'name': 'hello',
        'type': 'boolean',
        'label': _(u'Disable Mozilla Hello.'),
        'help_text': _(u'To show what WebRTC can do, Mozilla created a VoIP client '
            'called <a href=https://www.mozilla.org/en-US/firefox/hello/"">hello</a>.'
            ' Most users do not need it.'),
        'initial': False,
        'config': 
        {
            'loop.enabled': False
        },
        'addons': []
    },
    {
        'name': 'pdfjs',
        'type': 'boolean',
        'label': _(u'Disable the Firefox PDF-Reader'),
        'help_text': _(u'Mozilla integrated a pdf reader. It works good for a quick preview, but is too slow for reading longer documents.'),
        'initial': False,
        'config': 
        {
            'pdfjs.disabled': True
        },
        'addons': []
    },
    {
        'name': 'eme_drm',
        'type': 'boolean',
        'label': _(u'Disable DRM (EME) in Firefox'),
        'help_text': _(u'Disable the <a href="http://www.w3.org/TR/encrypted-media/">encrypted media extensions</a> in HTML5. '
            'If you have a strong stance on rejecting DRM. '
            '(<a href="http://www.pcworld.com/article/2155440/firefox-will-get-drm-copy-protection-despite-mozillas-concerns.html">Article about EME and its unique identifier</a>)'),
        'initial': False,
        'config': 
        {
            'media.eme.enabled': False,
            'media.gmp-eme-adobe.enabled': False,
        },
        'addons': []
    }
]

BloatwareForm = create_configform(id="bloatware", name=_(u"Bloatware"),
    options=bloatware_options)


addon_options = [
    {
        'name': 'canvasblocker',
        'type': 'boolean',
        'label': _(u'Install <a href="https://addons.mozilla.org/en-US/firefox/addon/canvasblocker/">CanvasBlocker</a> extension.'),
        'help_text': _(u'Blocks the JS-API for the &lt;canvas&gt; element to prevent <a href="https://en.wikipedia.org/wiki/Canvas_fingerprinting">Canvas-Fingerprinting</a>.'),
        'initial': True,
        'config': {},
        'addons': ['CanvasBlocker@kkapsner.de.xpi']
    },
    {
        'name': 'google_redirect_cleaner',
        'type': 'boolean',
        'label': _(u'Install <a href="https://addons.mozilla.org/de/firefox/addon/google-no-tracking-url/">Google Redirects Fixer &amp; Tracking Remover</a> extension.'),
        'help_text': _(u'Rewrites URLs from the google result pages to direct links instead redirect urls with tracking.'),
        'initial': True,
        'config': {},
        'addons': ['jid1-zUrvDCat3xoDSQ@jetpack.xpi']
    },
    {
        'name': 'https_everywhere',
        'type': 'boolean',
        'label': _(u'Install <a href="https://addons.mozilla.org/en-US/firefox/addon/https-everywhere/">HTTPS Everywhere</a> extension.'),
        'help_text': _(u'HTTPS Everywhere is a Firefox extension that  enables HTTPS encryption automatically on sites that support it.'),
        'initial': True,
        'config': {},
        'addons': ['https-everywhere@eff.org.xpi']
    },
    {
        'name': 'ublock',
        'type': 'boolean',
        'label': _(u'Install <a href="https://addons.mozilla.org/en-US/firefox/addon/ublock-origin/">uBlock Origin</a> extension.'),
        'help_text': _(u'Efficient blocker, which does not only block ads, but also supports Anti-Tracking and Anti-Malware Blocklists'),
        'initial': True,
        'config': {},
        'addons': ['uBlock0@raymondhill.net.xpi']
    },
    # TODO: here could be some setting for good privacy lists for ublock as default
    {
        'name': 'umatrix',
        'type': 'boolean',
        'label': _(u'Install <a href="https://addons.mozilla.org/en-US/firefox/addon/umatrix/">uMatrix</a> extension.'),
        'help_text': _(u'A content blocker for advanced users, which blocks requests to thirdparty domains. Big privacy gain, but you will need to configure exception rules for many sites.'),
        'initial': False,
        'config': {},
        'addons': ['uMatrix@raymondhill.net.xpi']
    },
    {
        'name': 'xclear',
        'type': 'boolean',
        'label': _(u'Install <a href="https://addons.mozilla.org/en-US/firefox/addon/xclear/">xclear</a> extension.'),
        'help_text': _(u'Adds a little [x] icon to urlbar and searchbar to clear the text.'),
        'initial': False,
        'config': {},
        'addons': ['xclear@as-computer.de.xpi']
    },
]

AddonForm = create_configform(id="addons", name=_(u"Addons"),
    options=addon_options)
