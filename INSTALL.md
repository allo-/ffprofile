# Quickstart for a Testserver:

## Prerequisite

Both `python` and `virtualenv` are already installed

## Manual procedure

- Create a virtual environment: ``virtualenv venv;source venv/bin/activate``.
- Install requirements: ``pip install -r requirements.txt``.
- Create a project: ``django-admin.py startproject project;cd project``
- Link the project (TODO: add a setup.py): ``ln -s /path/to/firefox-profilemaker profilemaker``.
- Edit ``project/settings.py`` (from the venv ``project/project/settings.py``)
  - Add `import os` and `from dotenv import load_dotenv` to load `.env` variables from environment
  - ``INSTALLED_APPS``: Add ``'profilemaker', 'bootstrap3', 'jquery',``
  - ``ALLOWED_HOSTS`` : Specify your allowed hosts, for example, `['*']`, to grant access from all hosts.
  - ``CSRF_TRUSTED_ORIGINS`` : Specify your trusted origins, for instance, `['*']`, to permit access from all hosts.
  - ``SECRET_KEY`` : Update this field with your unique secret key. You can generate one using the command base64 /dev/urandom | head -c50
- Edit ``project/urls.py`` and replace by:
```python
from django.urls import include, path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("", include("profilemaker.urls")),
]

urlpatterns += staticfiles_urlpatterns()
```
- Init db with ``./manage.py migrate``
- Start with ``./manage.py runserver``
- Optional: To avoid using bootstrap from a CDN add: ``BOOTSTRAP3 = {'base_url': '/static/bootstrap/'}`` (and install bootstrap into the ``STATIC_ROOT``)

## Automatic procedure

> :warning: Installation will remove `venv` & `project` forlders

- Install the environment: `make install`
  - Manually edit ``project/settings.py`` (as mentionned during the install)
- Run the server: `make run`
- Clean the project: `make remove`

## Docker

- `make build`: build the docker image
- `make up`: run the container
- `make down`: stop the container
- `make shell`: open a shell on the running container

> :information_source: The addons should be placed in the `extensions` folder as well
