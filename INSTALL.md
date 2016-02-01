Quickstart for a Testserver:

- Create a virtual environment: ``virtualenv venv;cd venv;source bin/activate``.
- Install django: ``pip install django>=1.8,<1.9``
- Create a project: ``django-admin.py startproject project;cd project``
- Link the project (TODO: add a setup.py): ``ln -s /path/to/firefox-profilemaker profilemaker``.
- Install requirements: ``pip install -r profilemaker/requirements.txt``.
- Edit ``project/settings.py`` (from the venv ``project/project/settings.py``)
  - ``INSTALLED_APPS``: Add ``'profilemaker', 'bootstrap3', 'jquery',``
- Edit ``project/urls.py``:
  - Add import: ``from django.contrib.staticfiles.urls import staticfiles_urlpatterns``
  - Add urlpattern: ``url(r'', include('profilemaker.urls')),``
  - Add after the urlpatterns: ``urlpatterns += staticfiles_urlpatterns()``
- Start with ``./manage.py runserver``
- Optional: To avoid using bootstrap from a CDN add: ``BOOTSTRAP3 = {'base_url': '/static/bootstrap/'}`` (and install bootstrap into the ``STATIC_ROOT``)

