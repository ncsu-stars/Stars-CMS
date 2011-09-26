STARS CMS
=========

This is a CMS written in Django specifically for STARS SLC's. This CMS is used at North Carolina State University

Installation
------------

### Create your virtual environment

Make sure you have pip and virtualenv installed on your system already

#. Change into the cloned project directory (where this README is contained)
#. Run the following: ``virtualenv --no-site-packages --distribute ve``
#. Active the virtual environment by running: ``source ve/bin/activate``
#. Install the requirements by running: ``pip install -r requirements.txt``

### Run your server

You can run the development server inside the virtual environment: ``python manage.py run server``

There should be no errors and you should be able to visit the website at: ``http://localhost:8000``

Contributing
------------

Feel free to fork the project and add features you feel are necessary. We will consider any bug-fixes or feature implementations for merging.