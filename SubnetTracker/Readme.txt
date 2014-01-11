

The purpose of this file is to explain how to not only setup this project but also how
it's structure is setup.

Please note that the tarball also contains a git repository. You can view my history
and thought process by reviewing git commits.

Required Software
-----------------

This project only requires a few things:
1. ipaddress python library
2. Django 1.6
3. Python 2.5
4. PostgreSQL (or any other database of your choice, just make sure to modify settings.py accordingly)

Python and postgres can be installed from your distrobution's package manager.
The following command can install ipaddress:
'sudo pip install ipaddress'
or
'sudo easy_install ipaddress'

Django can be downloaded from https://www.djangoproject.com/.

Setup
-----

Once the required software is installed, follow these steps.
1. Create a database in Postgres and setup a user.
2. Modify the credentials in settings.py for the database settings.
3. Run './manage.py syncdb' to create the database tables, any questions it asks
are really not needed. The database is just used to store the required information.
There are no users.
4. Run './manage.py runserver' to run the server on localhost, port 8000.


Directory Structure
--------------------

The 'apps/' directory contains all the .py files which handle page rendering. Usually
with my Django projects, I make an 'apps' directory and then each 'app' (typically its
sub-url as well) is its own sub-directory. You can usually navigate the source code
like you would navigate the site. (eg, 'http://example.com/navigation/' would have
a sub-directory called 'navigation' in the apps directory.)
Each app is usually placed under the "INSTALLED_APPS" setting in settings.py.
In a larger application, each app will have it's own url.py to handle all the urls
under that 'sub-url' of the site. Because this site is small I did not need to do that
but by having each app handle urls themselves, it makes the codebase much more organized.
url.py can get pretty confusing when it gets large.

The 'templates/' directory contains all the templates for the entire site. Structured
similarly to the 'apps/' directory, usually the only non-app file is 'base.html' because
the other sub-applications are inheriting it. Again, templates follow URLs and most templates
will have descriptive names showing what their function is in the site.

The 'static/' directory works slightly different. I usually follow the 'js, img, css' structure
and then the app name. This sorts out javascript, cascading style sheets, and images to their
respective directories. This directory is considered "django static assets" and should be
heavily cached, minified, and served as static content by the web server or CDN.

The master 'url.py' either defines all site urls in a small site or it will manage all the apps
'sub-urls' and forward requests to the app's url.py.


Additional Notes
----------------

I chose to use a database because it was easier to do that than to get Django to
ignore storing things in a database. I was able to use models and get them working
within a half-hour or so.

Overall, this project was actually quite fun and interesting to work with.
I designed it with the mindset of having only the IT department use it, a
relatively small userbase that was not going to change by much.

I also created a git repository for this project. It actually saved me because
about half-way through my desktop had crashed and erased a few project files.
I did this mainly to keep track of my progress and to make sure I could go
back if I had to as well as prevent corruption from crashes.
