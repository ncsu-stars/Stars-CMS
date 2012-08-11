STARS CMS
=========

Stars-CMS is a content management system designed specifically for use with/as a STARS SLC website.  The CMS is written in Python using Django and includes the following features:
 * management of member profiles, SLC projects, and member blogs;
 * cross-referencing of related content for current academic (e.g., projects automatically link to participating members);
 * generation of longitudinal project histories for members;
 * online editing of profiles, projects, and blogs;
 * differing levels of access for member, project coordinators, and SLC leaders; and
 * use of Django's admin interface for low-level database manipulation.

The CMS is packaged as a Django app but may be deployed as a full website.  This software currently runs the STARS SLC website at North Carolina State University.

Installation
------------

### App Installation

There are two solutions:

1. Download the application by running `https://github.com/ncsu-stars/Stars-CMS.git` in your project directory. 

2. Run `pip install stars-cms` and add `cms` to your `INSTALLED_APPS`

### Create your virtual environment

Make sure you have pip and virtualenv installed on your system already
  
  1. Change into the cloned project directory (where this README is contained)
  2. Run the following: ``virtualenv --no-site-packages --distribute ve``
  3. Active the virtual environment by running: ``source ve/bin/activate``
  4. Install the requirements by running: ``pip install -r requirements.txt``

### Settings

Take a look at `settings.py.example` for example project settings.

### URLs

Use ``(r'^', include('cms.urls', namespace='cms'))`` to forward all URLs to the CMS.

### Run your server

You can run the development server inside the virtual environment: ``python manage.py runserver``

There should be no errors and you should be able to visit the website at: ``http://localhost:8000``

Contributing
------------

Feel free to fork the project and add features you feel are necessary. We will consider any bug-fixes or feature implementations for merging.
