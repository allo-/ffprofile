from django import forms
from django.utils.translation import ugettext as _

# current structure:
# - FirefoxTracking: builtin features, which send data to mozilla,
#   google and other thirdparties
# - WebsiteTracking: Features, which are made for tracking (i.e. ping, beacons)
#   or may used for it (i.e. battery api)
# - Privacy: General privacy related settings like referer, cookies, etc.
#   which may be harmless or needed (i.e. cookies)
# - Security: No direct privacy problems, but maybe security issues
#   (i.e. webgl may hang firefox)
# - Bloatware: Settings, which disable unwanted features like hello or pocket
# - Annoyances: Settings, which disable first-run
#   "did you know, here is our new tab page" popups.
#
# TODO: WebsiteTracking could be split into Tracking (ping, beacon, ...) and
#       Fingerprinting (battery, canvas, ...), when there are more settings.

class AnnoyancesForm(forms.Form):
    id = 'annoyances'
    name = _(u'Annoyances')
    form_name = forms.CharField(initial='annoyances', widget=forms.widgets.HiddenInput)

    newtabpage_intro = forms.BooleanField(
        label=_(u'Disable new tab page intro'),
        help_text=_(u'Disable the intro to the newtab page on the first run'),
        initial=True, required=False)
    pocket_intro = forms.BooleanField(
        label=_(u'Disable pocket intro'),
        initial=True, required=False)
    aboutconfig_warning = forms.BooleanField(
        label=_(u'Disable about:config warning'),
        initial=True, required=False)
    default_browser = forms.BooleanField(
        label=_(u'Disable checking if Firefox is the default browser'),
        initial=True, required=False)
    heartbeat = forms.BooleanField(
        label=_(u'Disable Heartbeat Userrating'),
        help_text=_(u'With Firefox 37, Mozilla integrated the <a href="https://wiki.mozilla.org/Advocacy/heartbeat">Heartbeat</a> '
            'system to ask users from time to time about their experience with firefox.'),
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
    id = "firefox_tracking"
    name = _(u"Firefox Tracking")
    form_name = forms.CharField(initial="firefox_tracking", widget=forms.widgets.HiddenInput)
    telemetry = forms.BooleanField(
        label=_(u"Disable Telemetry"),
        help_text=_(u'The <a href="https://support.mozilla.org/en-US/kb/share-telemetry-data-mozilla-help-improve-firefox">telemetry feature</a> '
            'sends data about the performance and responsiveness of firefox to mozilla.'),
        initial=True, required=False)
    health_report = forms.BooleanField(
        label=_(u"Disable health report"),
        help_text=_(u'Disable sending <a href="https://www.mozilla.org/en-US/privacy/firefox/#health-report">Firefox health reports</a> to mozilla'),
        initial=True, required=False)
    addon_data = forms.BooleanField(
        label=_(u"Opt out metadata updates"),
        help_text=_(u'Firefox sends data about installed addons as <a href="https://blog.mozilla.org/addons/how-to-opt-out-of-add-on-metadata-updates/">metadata updates</a>, so mozilla is able to recommend you other addons.'),
        initial=True, required=False)
    phishing_protection = forms.BooleanField(
        label=_(u"Disable phishing protection"),
        help_text=_(u'The phishing protection contacts google with an unique key:'
        ' <a href="http://electroholiker.de/?p=1594">wrkey</a>.'),
        initial=True, required=False)
    newtab_preload = forms.BooleanField(
        label=_(u"Disable preloading of the new tab page."),
        help_text=_(u'By default firefox preloads the new tab page (with website thumbnails) in the background before it is even opened.'),
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

class PrivacyForm(forms.Form):
    id = 'privacy'
    name = _(u'Privacy')
    form_name = forms.CharField(initial='privacy', widget=forms.widgets.HiddenInput)

    useragent = forms.CharField(
        label=_(u'Fake another Useragent'),
        help_text=_(u'Using a <a href="https://techblog.willshouse.com/2012/01/03/most-common-user-agents/">popular useragent string</a> '
            'avoids to attract attention i.e. with an Iceweasel UA. (keep blank to use the default)'),
        initial="", required=False)
    thirdparty_cookies = forms.BooleanField(
        label=_(u'Block thirdparty cookies'),
        help_text=_(u'Block cookies, which are not from the site you\'re visiting. '
            'You will rarely notice that something is missing, but it hugely improves your privacy.'),
        initial=True, required=False)
    all_cookies = forms.BooleanField(
        label=_(u'Block all cookies'),
        help_text=_(u'Block all cookies. Many sites will not work without cookies.'),
        initial=False, required=False)
    referer = forms.ChoiceField(
        label=_(u'Block Referer'),
        help_text=_(u'Firefox tells a website, from which site you\'re coming '
            '(the so called <a href="http://kb.mozillazine.org/Network.http.sendRefererHeader">referer</a>).'),
        choices = [(0, _(u'Disable')), (1, _(u'Allow only when clicking a link')), (2, _(u'Allow for links and loaded images'))],
        initial=0, required=False,
    )
    dom_storage = forms.BooleanField(
        label=_(u'Disable DOM storage'),
        help_text=_(u'Disables DOM storage, which enables so called "supercookies". Some modern sites will not fully not work (i.e. missing "save" functions).'),
        initial=False, required=False)
    indexed_db = forms.BooleanField(
        label=_(u'Disable IndexedDB'),
        help_text=_(u'<a href="http://www.w3.org/TR/IndexedDB/">IndexedDB</a> is a way, websites can store structured data. This can be '
            '<a href="http://arstechnica.com/apple/2010/09/rldguid-tracking-cookies-in-safari-database-form/">abused for tracking</a>, too. '
            'Disabling may be a problem with some webapps like tweetdeck.'),
        initial=True, required=False)
    prefetch = forms.BooleanField(
        label=_(u'Disable Link Prefetching'),
        help_text=_(u'Firefox prefetches the next site on some links, so the site is loaded even when you never click.'),
        initial=True, required=False)
    webrtc = forms.BooleanField(
        label=_(u'Disable WebRTC'),
        help_text=_(u'Disables the WebRTC function, which gives away your local ips.'),
        initial=True, required=False)
    search_suggest = forms.BooleanField(
        label=_(u'Disable Search Suggestions'),
        help_text=_(u'Firefox suggests search terms in the search field. This will send everything typed or pasted '
            'in the search field to the chosen search engine, even when you did not press enter.'),
        initial=False, required=False)
    keyword_search = forms.BooleanField(
        label=_(u'Disable Search Keyword'),
        help_text=_(u'When you mistype some url, firefox starts a search even from urlbar. '
            'This feature is useful for quick searching, but may harm your privacy, when it\'s unintended.'),
        initial=False, required=False)
    fixup_url = forms.BooleanField(
        label=_(u'Disable Fixup URLs'),
        help_text=_(u'When you type "something" in the urlbar and press enter, firefox tries "something.com", if Fixup URLs is enabled.'),
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


class BloatwareForm(forms.Form):
    id = "bloatware"
    name = _(u"Bloatware")
    form_name = forms.CharField(initial="bloatware", widget=forms.widgets.HiddenInput)
    pocket = forms.BooleanField(
        label=_(u'Disable Pocket integration.'),
        help_text=_(u'For monetizing firefox, mozilla included the '
            '<a href="https://getpocket.com/">Pocket</a> addon by default.'),
        initial=False, required=False)
    hello = forms.BooleanField(
        label=_(u'Disable Mozilla Hello.'),
        help_text=_(u'To show what WebRTC can do, mozilla created a VoIP client '
        'called <a href=https://www.mozilla.org/en-US/firefox/hello/"">hello</a>. Most users do not need it.'),
        initial=False, required=False)
    pdfjs = forms.BooleanField(
        label=_(u'Disable the Firefox PDF-Reader'),
        help_text=_(u'Mozilla integrated a pdf reader. It works good for a quick preview, but is too slow for reading longer documents.'),
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


class AddonForm(forms.Form):
    id = "addons"
    name = _(u"Addons")
    form_name = forms.CharField(initial="addons", widget=forms.widgets.HiddenInput)
    canvasblocker = forms.BooleanField(
        label=_(u'Install <a href="https://addons.mozilla.org/en-US/firefox/addon/canvasblocker/">CanvasBlocker</a> extension.'),
        help_text=_(u'Blocks the JS-API for the &lt;canvas&gt; element to prevent <a href="https://en.wikipedia.org/wiki/Canvas_fingerprinting">Canvas-Fingerprinting</a>.'),
        initial=True, required=False)
    google_redirect_cleaner = forms.BooleanField(
        label=_(u'Install <a href="https://addons.mozilla.org/de/firefox/addon/google-no-tracking-url/">Google Redirects Fixer &amp; Tracking Remover</a> extension.'),
        help_text=_(u"Rewrites URLs from the google result pages to direct links instead redirect urls with tracking."),
        initial=True, required=False)
    ublock = forms.BooleanField(
        label=_(u'Install <a href="https://addons.mozilla.org/en-US/firefox/addon/ublock-origin/">uBlock Origin</a> extension.'),
        help_text=_(u"Efficient blocker, which does not only block ads, but also supports Anti-Tracking and Anti-Malware Blocklists"),
        initial=True, required=False)
    umatrix = forms.BooleanField(
        label=_(u'Install <a href="https://addons.mozilla.org/en-US/firefox/addon/umatrix/">uMatrix</a> extension.'),
        help_text=_(u"A content blocker for advanced users, which blocks requests to thirdparty domains. Big privacy gain, but you will need to configure exception rules for many sites."),
        initial=False, required=False)
    xclear = forms.BooleanField(
        label=_(u'Install <a href="https://addons.mozilla.org/en-US/firefox/addon/xclear/">xclear</a> extension.'),
        help_text=_(u"Adds a little [x] icon to urlbar and searchbar to clear the text."),
        initial=False, required=False)

    def get_config_and_addons(self):
        addons = []
        if self.is_valid():
            if self.cleaned_data['xclear']:
                addons.append("xclear@as-computer.de.xpi")
            if self.cleaned_data['canvasblocker']:
                addons.append("CanvasBlocker@kkapsner.de.xpi")
            if self.cleaned_data['google_redirect_cleaner']:
                addons.append("jid1-zUrvDCat3xoDSQ@jetpack.xpi")
            if self.cleaned_data['ublock']:
                addons.append("uBlock0@raymondhill.net.xpi")
            if self.cleaned_data['umatrix']:
                addons.append("uMatrix@raymondhill.net.xpi")
        return {}, addons
