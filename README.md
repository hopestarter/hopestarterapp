hopestarter.org webapp
======================

A django app for the hopestarter.org webapp

# Usage and testing

## Docker
If you have docker installed, you can build an image and launch a container ready for you to use and test changes by using the scripts ./docker/build_image.py and ./docker/start_container. build_image.py must be called from the project's root directory. 

The former script does just what it says in its name by using the dockerfiles named 1.BinaryDeps, 2.PythonDeps, 3.Ansible and 4.ServerSetup. The later starts a container with the resulting image with some sensible defaults like port mappings and storage volumes.

## Virtualenvwrapper
If you are using virtualenvwrapper and it's properly configured, just do:

```bash
mkvirtualenv <project_name>
```

To test install the dependencies:

```bash
pip install -r requirements/test.txt
pip install -r requirements/api.txt
```

## Configuration

Export the `PGUSER` and `PGPASS` environment variables:

```
export PGUSER=hopestarter
export PGPASS=secret
```

Run the ansible play book to create local db:

```
cd plays
export PGUSER=geotest
export PGPASS=geotest
export PGDATABASE=geotest
ansible-playbook -i inventory/local local.yml
```

Last, run `./manage.py syncdb` from within the `src` directory.


## Test fixtures

Optionally load the fixtures as follows:

```
./manage.py loaddata hopestarter/fixtures/auth.yaml
./manage.py loaddata hopebase/fixtures/data.yaml
./manage.py loaddata hopespace/fixtures/data.yaml
```

## Running the website

Execute `./manage.py runserver` from within the `src` directory.

## Running the API

Execute `./manage_api.py runserver` from within the `src` directory.


## Mac OSX dependencies

```
brew install postgis gdal geos virtualenv
```

