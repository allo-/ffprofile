# Firefox Profilemaker

The Firefox profile maker is a web application for creating Firefox profiles with preconfigured defaults. The focus lies on privacy and removing unnecessary features. It disables intrusive features like telemetry, allows disabling web features that may be used for fingerprinting the browser, and contains some additional options for controversial features like Pocket.


If you are just looking to create a profile, you can find the service running this code at [ffprofile.com](https://ffprofile.com). This repository contains the code to run your own instance, i.e., to add your own settings to it or simply so you don't have to trust the website but can generate your profile locally.

The project and website are not affiliated with or endorsed by Mozilla.

## Installation

The project uses python Django. For running it locally, the Django test server should be sufficient. The project doesn't use database features, but it requires the session framework, which uses, depending on the configuration, a database backend. Using the simple SQLite database is sufficient.

After creating a Django project and adding the app, one needs to provide the Firefox addons that will be included in profiles as XPI files in a `extensions` folder at the path from where you run the project.
The Extensions need to be named like in their `install.rdf` / `manifest.json` file because otherwise Firefox won't install them.

The current URLs and names are:

- [CanvasBlocker@kkapsner.de.xpi](https://addons.mozilla.org/firefox/addon/canvasblocker/)
- [jid1-zUrvDCat3xoDSQ@jetpack.xpi](https://addons.mozilla.org/firefox/addon/google-no-tracking-url/)
- [https-everywhere@eff.org.xpi](https://addons.mozilla.org/firefox/addon/https-everywhere/)
- [uBlock0@raymondhill.net.xpi](https://addons.mozilla.org/firefox/addon/ublock-origin/)
- [uMatrix@raymondhill.net.xpi](https://addons.mozilla.org/firefox/addon/umatrix/)
- [jid1-MnnxcxisBPnSXQ@jetpack.xpi](https://addons.mozilla.org/en-US/firefox/addon/privacy-badger17/)
- [CookieAutoDelete@kennydo.xpi](https://addons.mozilla.org/en-US/firefox/addon/cookie-autodelete/)
- [jid1-BoFifL9Vbdl2zQ@jetpack.xpi](https://addons.mozilla.org/en-US/firefox/addon/decentraleyes/)
- [{74145f27-f039-47ce-a470-a662b129930a}.xpi](https://addons.mozilla.org/en-US/firefox/addon/clearurls/)
- [{c607c8df-14a7-4f28-894f-29e8722976af}.xpi](https://addons.mozilla.org/en-US/firefox/addon/temporary-containers/)
- [@testpilot-containers.xpi](https://addons.mozilla.org/en-US/firefox/addon/multi-account-containers/)

## About the project

The project aims to provide a way to create a profile with privacy defaults, but instead of importing a long user.js file without knowing what the options do, every option should have a short description, and the users should be able to understand why they would want to enable or disable the option and what are the possible side effects. There is no one-size-fits-all, so the tool aims to provide a wizard to create a *personalized* profile.

Keeping it simple enough implies that it cannot contain everything. If there are too many options, people will not have the time to read every description and weigh the cost and benefits. So I try to keep the project focused on the relevant privacy options.

Some things we currently do not include are:

- Many very useful add-ons. I try to keep the list short because add-ons can slow down the browser, they may be insecure, and there are just too many great addons to include them all.
- Your favorite performance settings and similar optimizations. Often they are a trade-off and not easy to understand. Power users can still change them themself (and get them from one of the many great user.js files other people provide), but the average user is probably better off with the defaults.
- Larger UI/UX changes. They are personal choices, and too many to include them all.
- Options that are already easy to configure. If Firefox already asks for permission before doing something the first time, it is probably unnecessary to have a preconfigured answer.

This should not prevent you from creating such settings. There is already basic support for [profiles](profiles/), and it is planned to add a function to choose multiple profiles, e.g., `security`, `privacy`, `classic ui` or similar combinations. When it is implemented, such settings can be included in secondary profiles.

The bug tracker contains some `infrastructure` issues for these things and some issues tagged as `other profile?` which may be implemented sometime.

You're also welcome to add the options in an own fork. That's one of the reasons why the project is provided as open source. I may then pick up some of the options you implement at a later point in time.
