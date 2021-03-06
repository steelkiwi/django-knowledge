.. Django Knowledge documentation master file, created by
   sphinx-quickstart on Thu Feb 16 12:54:45 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


Welcome to django-knowledge's documentation!
=======================================

django-knowledge makes it easy to add an integrated support desk, help desk or 
knowledge base to your Django project with only a few lines of boilerplate code.
While we give you a generic design for free, you should just as easily be able 
to customize the look and feel of the app if you like.

**django-knowledge** was developed internally for `Zapier <https://zapier.com/>`_.
Check out a `live demo <http://django-knowledge.org/>`_.


At a glance:
------------

- Turn common questions or support requests into a **knowledge base**.
- Control **who sees what** with simple per object view permissions: *public* (everyone), 
  *private* (poster & staff), or *internal* (only staff).
- Assign questions and answers to **categories** for easy sorting.
- Staff get **moderation controls** or they can use the familiar *Django admin* to handle support requests.
- Allow **anonymous questions**, or require a standard Django user account (the default).
- Included base **templates and design** with prebundled HTML and CSS.
- Optionally **alert users** of new responses via email (or your own alert system).
- BSD license.


Contents:
--------------

.. toctree::
   :maxdepth: 2

   overview
   install
   development
   alerts
   customize
   performance
   settings


Links:
------

* View a `live demo <http://django-knowledge.org/>`_. This is the included stock design.
* Check out the `documentation <http://django-knowledge.readthedocs.org/>`_ at ReadTheDocs.
* Visit our `GitHub repo <https://github.com/zapier/django-knowledge>`_ and join the development!.


Screen Shots:
-------------

.. image:: images/thread.png
   :width: 100 %
   :alt: a common thread viewed by anonymous user

.. image:: images/thread-mod.png
   :width: 100 %
   :alt: a common thread viewed by a moderator (staff)

.. image:: images/ask.png
   :width: 100 %
   :alt: ask form

.. image:: images/home.png
   :width: 100 %
   :alt: the home page

.. image:: images/results.png
   :width: 100 %
   :alt: search results with ask form at bottom

.. image:: images/tests.png
   :alt: 100% coverage on tests
