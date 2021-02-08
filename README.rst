pl-s3retrieve
=============

.. image:: https://img.shields.io/docker/v/fnndsc/pl-s3retrieve
    :target: https://hub.docker.com/r/fnndsc/pl-s3retrieve

.. image:: https://img.shields.io/github/license/fnndsc/pl-s3retrieve
    :target: https://github.com/FNNDSC/pl-s3retrieve/blob/master/LICENSE

.. image:: https://github.com/FNNDSC/pl-s3retrieve/workflows/ci/badge.svg
    :target: https://github.com/FNNDSC/pl-s3retrieve/actions


.. contents:: Table of Contents


Abstract
--------

A ChRIS ds app to retrieve data of interest from Amazon S3 service


Description
-----------

``s3retrieve`` is a ChRIS-based application to retrieve file/folders from Amazon S3 service.


Usage
-----

.. code::

        python s3retrieve.py
            [-h] [--help]
            [--json]
            [--man]
            [--meta]
            [--savejson <DIR>]
            [-v <level>] [--verbosity <level>]
            [--version]
            <inputDir>
            <outputDir>
            --bucket <BUCKET>
            --prefix <PREFIX>
            --awskeyid <KEYID>
            --awssecretkey <SECRETKEY>


Arguments
~~~~~~~~~

.. code::

        [-h] [--help]
        If specified, show help message and exit.

        [--json]
        If specified, show json representation of app and exit.

        [--man]
        If specified, print (this) man page and exit.

        [--meta]
        If specified, print plugin meta data and exit.

        [--savejson <DIR>]
        If specified, save json representation file to DIR and exit.

        [-v <level>] [--verbosity <level>]
        Verbosity level for app. Not used currently.

        [--version]
        If specified, print version number and exit.

        <inputDir>
        Input directory.

        <outputDir>
        Output directory.

        --bucket <BUCKET>
        Name of the Amazon S3 bucket.

        [--prefix <PREFIX>]
        If specified, retrieve directory/file prefix path in s3.

        --awskeyid <KEYID>
        AWS access key id.

        --awssecretkey <SECRETKEY>
        AWS secret access key.


Getting inline help is:

.. code:: bash

    docker run --rm fnndsc/pl-s3retrieve s3retrieve --man

Run
~~~

You need you need to specify input and output directories using the `-v` flag to `docker run`.


.. code-block:: bash

    docker run --rm                                                         \
        -v /tmp/input:/incoming                                             \
        -v /tmp/output:/outgoing                                            \
        fnndsc/pl-s3retrieve                                                \
        s3retrieve --awskeyid KEYID --awssecretkey ACCESSKEY --bucket bch-fnndsc  \
        --prefix test \
        /incoming /outgoing \

The above will retrieve a copy of each file/folder inside the test "folder" in Amazon S3
storage into the local ``/outgoing`` directory. Some metadata files should have previously
been read from ``/incoming`` directory.

Development
-----------

Build the Docker container:

.. code:: bash

    docker build -t local/pl-s3retrieve .

Run unit tests:

.. code:: bash

    docker run --rm local/pl-s3retrieve nosetests


.. image:: https://raw.githubusercontent.com/FNNDSC/cookiecutter-chrisapp/master/doc/assets/badge/light.png
    :target: https://chrisstore.co
