Quickstart for a Testserver:

- Create a virtual environment: ``virtualenv venv;cd venv;source bin/activate``.
- Install requirements: ``pip install -r requirements.txt``.
- Create a project: ``django-admin.py startproject project;cd project``
- Link the project (TODO: add a setup.py): ``ln -s /path/to/firefox-profilemaker profilemaker``.
- Edit ``project/settings.py`` (from the venv ``project/project/settings.py``)
  - ``INSTALLED_APPS``: Add ``'profilemaker', 'bootstrap3', 'jquery',``
- Edit ``project/urls.py`` and replace by:
```python
from django.conf.urls import include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    url(r'', include("profilemaker.urls")),
]
urlpatterns += staticfiles_urlpatterns()
```
- Init db with ``./manage.py migrate``
- Start with ``./manage.py runserver``
- Optional: To avoid using bootstrap from a CDN add: ``BOOTSTRAP3 = {'base_url': '/static/bootstrap/'}`` (and install bootstrap into the ``STATIC_ROOT``)
