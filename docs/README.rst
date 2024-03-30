--------------------------
   Document Development
--------------------------

The documentation is written in reStructuredText. Once you are finished
making changes, you must build the documentation. To build the LedFx
documentation follow the steps outlined below:

.. note:: Alternatively, you may run ``make livehtml`` in place of ``make html`` to open a browser and view your changes in
          realtime.


Linux
-------

.. code:: console

    $ cd ~/ledfx/docs
    $ pip install -r requirements-docs.txt
    $ make html

macOS
-------

.. code:: console

    $ source ~/ledfx-venv/bin/activate
    $ cd ~/ledfx/docs
    $ pip install -r requirements-docs.txt
    $ make html


.. Extensions used by sphinx

.. _sphinx.ext.autodoc: https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html
.. _sphinx.ext.githubpages: https://www.sphinx-doc.org/en/master/usage/extensions/githubpages.html
.. _sphinxcontrib.httpdomain: https://sphinxcontrib-httpdomain.readthedocs.io/en/stable/
.. _sphinx_rtd_theme: https://sphinx-rtd-theme.readthedocs.io/en/latest/index.html