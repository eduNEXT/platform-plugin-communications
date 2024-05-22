Platform Plugin Communications
##############################

|ci-badge| |license-badge| |status-badge|


Purpose
*******

Open edX plugin that extends email capabilities for the platform. The following
features are included:

1. Adds new endpoint to search students in a course by username, email or full
   name.
2. Enables sending targeted emails to individual students or teams within a
   course by extending the existing ``send_email`` functionality in
   edx-platform.

This plugin has been created as an open source contribution to the Open edX
platform and has been funded by the Unidigital project from the Spanish
Government - 2023.

Compatibility Notes
===================

+------------------+--------------+
| Open edX Release | Version      |
+==================+==============+
| Palm             | >= 0.3.0     |
+------------------+--------------+
| Quince           | >= 0.3.0     |
+------------------+--------------+
| Redwood          | >= 0.3.0     |
+------------------+--------------+

The settings can be changed in ``platform_plugin_communications/settings/common.py``
or, for example, in tutor configurations.

**NOTE**: the current ``common.py`` works with Open edX Palm, Quince and
Redwood version.


Getting Started
***************

Developing
==========

1. One Time Setup
-----------------

Clone the repository:

.. code-block:: bash

  git clone git@github.com:eduNEXT/platform-plugin-communications.git
  cd platform-plugin-communications

Set up a virtualenv with the same name as the repo and activate it. Here's how
you might do that if you have ``virtualenv`` set up:

.. code-block:: bash

  virtualenv -p python3.8 platform-plugin-communications

2. Every time you develop something in this repository
------------------------------------------------------

Activate the virtualenv. Here's how you might do that if you're using
``virtualenv``:

.. code-block:: bash

  source platform-plugin-communications/bin/activate

Grab the latest code:

.. code-block:: bash

  git checkout main
  git pull

Install/Update the dev requirements:

.. code-block:: bash

  make requirements

Run the tests and quality checks (to verify the status before you make any
changes):

.. code-block:: bash

  make validate

Make a new branch for your changes:

.. code-block:: bash

  git checkout -b <your_github_username>/<short_description>

Using your favorite editor, edit the code to make your change:

.. code-block:: bash

  vim ...

Run your new tests:

.. code-block:: bash

  pytest ./path/to/new/tests

Run all the tests and quality checks:

.. code-block:: bash

  make validate

Commit all your changes, push your branch to github, and open a PR:

.. code-block:: bash

  git commit ...
  git push

Deploying
==========

Tutor environments
------------------

To use this plugin in a Tutor environment, you must install it as a requirement of the ``openedx`` image. To achieve this, follow these steps:

.. code-block:: bash

    tutor config save --append OPENEDX_EXTRA_PIP_REQUIREMENTS=git+https://github.com/edunext/platform-plugin-communications@vX.Y.Z
    tutor images build openedx

Then, deploy the resultant image in your environment.

Setting Up
**********

To use correctly the plugin, you need to do the next steps:

1. **Enable Bulk Email in you Open edX instance**

   You must create bulk email flag in the Django admin panel. You can access to
   Django Admin panel in the next URL: ``<lms_host>/admin/bulk_email/bulkemailflag/``.
   Then, you need to create a new flag with both checkboxes checked:

   - Enabled: ✅
   - Require course email auth: ✅

2. **Enable Bulk Email in the course**

   You must enable bulk email in the course. You can access to Django Admin
   panel in the next URL: ``<lms_host>/admin/bulk_email/courseauthorization/``.
   Then, you need to create a new course authorization with the following
   values:

   - Course ID: ID of the course.
   - Email enabled: ✅

3. **Activate teams in your Open edX instance**

   You must add the ``ENABLE_TEAMS`` in your LMS settings (development or
   production). For example, you can create a YAML plugin with the following
   content:

   .. code-block:: yaml

    name: teams-settings
    version: 0.1.0
    patches:
      openedx-common-settings: |
        FEATURES["ENABLE_TEAMS"] = True

4. **Activate teams app**

   You must create a waffle flag in the Django admin panel. You can access to
   Django Admin panel in the next URL: ``<lms_host>/admin/waffle/flag/``. Then,
   you need to create a new flag with the following values:

   - Name: ``teams.enable_teams_app``
   - Everyone: ``Yes``
   - Superusers: ``True``

Using the plugin's APIs
***********************

Now, you can use the plugin. The next endpoints are available:

- POST ``/<lms_host>/platform-plugin-communications/<course_id>/api/send_email/``:
  Same email capabilities as the ``send_email`` endpoint in edx-platform but with
  and additional parameter ``extra_targets``.

  **Path parameters**

  - ``course_id``: ID of the course.

  **Body parameters**

  Same parameters as the ``send_email`` endpoint in edx-platform but with an additional
  parameter:

  - ``extra_targets``: Specifies additional targets to send the email to. It is
    a JSON object with the properties ``emails`` and ``teams``. The property
    ``emails`` is a list of user emails and the property ``teams`` is a list of
    team IDs.

    Example request:

    .. code-block:: json

      {
        ...
        "extra_targets": {"emails": ["john@doe.com"], "teams": ["team-bd5bef08149e41e58de24aa60e18c233"]}
      }

- GET ``/<lms_host>/platform-plugin-communications/<course_id>/api/search_learners/``: List all
  students in the course that match the query. The result list has a object for each
  student with the properties ``username``, ``email`` and ``name``.

  **Path parameters**

  - ``course_id``: ID of the course.

  **Query parameters**

  - ``query``: Query to search learners. It can be a username, email or full
    name.
  - ``page``: Page number of the results.
  - ``page_size``: Number of results per page.

  Example response:

  .. code-block:: json

    {
      "course_id": "course-v1:eduNEXT+Communications+Demo",
      "page": "1",
      "pages": 1,
      "page_size": 1,
      "total": 1,
      "results": [
        {
          "username": "johndoe",
          "email": "john@doe.com",
          "name": "John Doe"
        }
      ]
    }


Getting Help
************

If you're having trouble, we have discussion forums at `discussions`_ where you
can connect with others in the community.

Our real-time conversations are on Slack. You can request a
`Slack invitation`_, then join our `community Slack workspace`_.

For anything non-trivial, the best path is to open an `issue`_ in this
repository with as many details about the issue you are facing as you
can provide.

For more information about these options, see the `Getting Help`_ page.

.. _discussions: https://discuss.openedx.org
.. _Slack invitation: https://openedx.org/slack
.. _community Slack workspace: https://openedx.slack.com/
.. _issue: https://github.com/eduNEXT/platform-plugin-communications/issues
.. _Getting Help: https://openedx.org/getting-help


License
*******

The code in this repository is licensed under the AGPL 3.0 unless otherwise noted.

Please see `LICENSE.txt <LICENSE.txt>`_ for details.


Contributing
************

Contributions are very welcome. Please read `How To Contribute`_ for details.

This project is currently accepting all types of contributions, bug fixes,
security fixes, maintenance work, or new features.  However, please make sure
to have a discussion about your new feature idea with the maintainers prior to
beginning development to maximize the chances of your change being accepted.
You can start a conversation by creating a new issue on this repo summarizing
your idea.

.. _How To Contribute: https://openedx.org/r/how-to-contribute


Reporting Security Issues
*************************

Please do not report security issues in public. Please email security@edunext.co.

.. It's not required by our contractor at the moment but can be published later
.. .. |pypi-badge| image:: https://img.shields.io/pypi/v/platform_plugin_communications.svg
    :target: https://pypi.python.org/pypi/platform_plugin_communications/
    :alt: PyPI

.. |ci-badge| image:: https://github.com/eduNEXT/platform-plugin-communications/actions/workflows/ci.yml/badge.svg?branch=main
    :target: https://github.com/eduNEXT/platform-plugin-communications/actions
    :alt: CI

.. |license-badge| image:: https://img.shields.io/github/license/eduNEXT/platform-plugin-communications.svg
    :target: https://github.com/eduNEXT/platform-plugin-communications/blob/main/LICENSE.txt
    :alt: License

.. TODO: Choose one of the statuses below and remove the other status-badge lines.
.. .. |status-badge| image:: https://img.shields.io/badge/Status-Experimental-yellow
.. |status-badge| image:: https://img.shields.io/badge/Status-Maintained-brightgreen
.. .. |status-badge| image:: https://img.shields.io/badge/Status-Deprecated-orange
.. .. |status-badge| image:: https://img.shields.io/badge/Status-Unsupported-red
