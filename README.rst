#############
pl-s3retrieve
#############


Abstract
========

A Chris 'ds' plugin to retrieve file/folders from Amazon S3 service.

Preconditions
=============

This plugin requires input and output directories as a precondition.

Run
===

Using ``docker run``
--------------------

Assign an "input" directory to ``/incoming`` and an output directory to ``/outgoing``

.. code-block:: bash

    docker run --rm                                                         \
        -v /tmp/input:/incoming                                             \
        -v /tmp/output:/outgoing                                            \
        fnndsc/pl-s3retrieve                                                \
        s3retrieve.py --awskeyid KEYID --awssecretkey ACCESSKEY --bucket bch-fnndsc --prefix test /incoming /outgoing

The above will retrieve a copy of each file/folder inside the test "folder" in Amazon S3
storage into the local ``/outgoing`` directory. Some metadata files should have previously
been read from ``/incoming`` directory.

Make sure that the host ``/tmp/input`` directory is world readable and ``/tmp/output``
directory is world writable!