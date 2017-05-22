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
        -e AWS_ACCESS_KEY_ID=KEYID                                          \
        -e AWS_SECRET_ACCESS_KEY=ACCESSKEY                                  \
        -v $(pwd)/out:/incoming                                             \
        -v $(pwd)/out2:/outgoing                                            \
        fnndsc/pl-s3retrieve                                                \
        s3retrieve.py --bucket bch-fnndsc --s3path test /incoming /outgoing

The above will retrieve a copy of each file/folder inside the test "folder" in Amazon S3
storage into the local ``/outgoing`` directory. Some metadata files should have previously
been read from ``/incoming`` directory.

Make sure that the host ``$(pwd)/out`` directory is world readable and ``$(pwd)/out2``
directory is world writable!