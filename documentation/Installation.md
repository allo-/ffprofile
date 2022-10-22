
# Installation

*Quickstart guide on how to setup a test-server.*

<br>

## Requirements

*The following tools need to be present.*

<br>

-   **[VirtualEnv]**

-   **[Python]**

<br>
<br>

## Manual Steps

<br>

1.  Create a virtual environment.

    ```sh
    virtualenv venv;source venv/bin/activate
    ```
    
    <br>
    
2.  Install the requirements.

    ```sh
    pip install -r requirements.txt
    ```
    
    <br>
    
3.  Create a new project.

    ```sh
    django-admin.py startproject project;cd project
    ```
    
    <br>
    
4.  Link the project.

    ```sh
    ln -s /path/to/firefox-profilemaker profilemaker
    ```
    
    <br>
    
5.  Edit the settings at:

    `project/settings.py`
    
    or with **venv** at:
    
    `project/project/settings.py`
    
    <br>
    
6.  For  `INSTALLED_APPS`  add:
    
    ```
    'profilemaker', 'bootstrap3', 'jquery',
    ```
    
    <br>
    
7.  Replace  `project/urls.py`  with:

    ```python
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    from django.conf.urls import include , url

    urlpatterns = [ url(r'', include("profilemaker.urls")) ]
    urlpatterns += staticfiles_urlpatterns()
    ```
    
    <br>
    
8.  Initialize the database.

    ```sh
    ./manage.py migrate
    ```
    
    <br>
    
9.  Start the server.
    
    ```sh
    ./manage.py runserver
    ```
    
<br>

### Optional

To avoid using bootstrap from a CDN add:

```
BOOTSTRAP3 = { 'base_url' : '/static/bootstrap/' }
```

and install bootstrap into  `STATIC_ROOT`

<br>
<br>

## Automatic Setup

***This will remove the  `venv`  &  `project`  folders.***

<br>

1.  Install the environment.

    ```sh
    make install
    ```
    
    <br>
    
2.  Manually edit the following file <br>
    as described in the manual steps:

    `project/settings.py`
    
    <br>
    
3.  Start the server.

    ```sh
    make run
    ```
    
    <br>
    
-   Clean the project.

    ```sh
    make remove
    ```

<br>
<br>

## Docker

*Use the following commands to control your docker container.*

<br>

#### Build the docker image.

```sh
make build
```

<br>

#### Run the container.

```sh
make up
```

<br>

#### Stop the container.

```sh
make down
```

<br>

#### Open a shell in the container.

```sh
make shell
```

<br>

### Note

The addons should be placed in the  `/extensions/`  folder as well.

<br>


<!----------------------------------------------------------------------------->

[VirtualEnv]: https://virtualenv.pypa.io/en/latest/
[Python]: https://www.python.org/
