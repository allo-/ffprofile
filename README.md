The repo contains the source code for the Firefox Profilemaker at [ffprofile.com](https://ffprofile.com).

The code is also intended to serve as an option to generate profiles locally and should work with the simple django testserver by creating a project, installing the app and running `manage.py runserver`.

For the functions installing addons, you need to create a folder "extensions" from where you run the django project and place there the XPIs.
The Extension needs to have the name of its install.rdf / manifest.json file.

Currently they are:

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

Things, that will not be included in the main project:

- Some cool addons. The addons list should be short and mostly privacy addons.
- Your favourite performance setting. It's not the scope of the project and not all people need the same performance settings.

You're welcome to create an own [profile](profiles/) for such settings or fork the whole project.
For that, you can check the [installation](INSTALL.md) procedure.
