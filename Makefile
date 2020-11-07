SHELL = bash
.ONESHELL:

.PHONY: run
run:
	@echo Run server
	. venv/bin/activate
	./project/manage.py runserver

.PHONY: install
install: remove
	@echo Create python virtual environment
	python3 -m venv venv
	. venv/bin/activate
	@echo Install dependencies
	pip install -r requirements.txt
	make -s create-project

.PHONY: create-project
create-project:
	@echo Create django project
	django-admin.py startproject project
	@echo Create symlink
	ln -s ${CURDIR} project/profilemaker
	@echo Edit "'project/project/settings.py'"
	printf '%s\n' \
		"" \
		"INSTALLED_APPS = [" \
		"    'django.contrib.admin'," \
		"    'django.contrib.auth'," \
		"    'django.contrib.contenttypes'," \
		"    'django.contrib.sessions'," \
		"    'django.contrib.messages'," \
		"    'django.contrib.staticfiles'," \
		"    'profilemaker'," \
		"]" \
		>> project/project/settings.py
	@echo Edit "'project/project/urls.py'"
	printf '%s\n' \
		"" \
		"from django.conf.urls import include, url" \
		"from django.contrib.staticfiles.urls import staticfiles_urlpatterns" \
		"" \
		"urlpatterns = [" \
		"    url(r'', include(\"profilemaker.urls\"))," \
		"] + urlpatterns + staticfiles_urlpatterns()" \
		>> project/project/urls.py
	@echo Init db
	cd project
	./manage.py migrate

.PHONY: remove
remove:
	@echo "Erase 'venv' & 'project' directories"
	rm -rf venv project

.PHONY: up
up:
	docker run -d --rm --name profilemaker -p 8000:8000 -v ${PWD}/extensions:/code/extensions firefox-profilemaker:latest

.PHONY: down
down:
	docker stop profilemaker

.PHONY: build
build:
	docker build . -t firefox-profilemaker:latest

.PHONY: shell
shell:
	docker exec -it profilemaker /bin/sh
