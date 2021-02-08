#!/usr/bin/env python                                            
#
# s3retrieve ds ChRIS plugin app
#
# (c) 2021 Fetal-Neonatal Neuroimaging & Developmental Science Center
#                   Boston Children's Hospital
#
#              http://childrenshospital.org/FNNDSC/
#                        dev@babyMRI.org
#

import os

from chrisapp.base import ChrisApp
import boto3


Gstr_title = """
      _____          _        _                
     |____ |        | |      (_)               
 ___     / /_ __ ___| |_ _ __ _  _____   _____ 
/ __|    \ \ '__/ _ \ __| '__| |/ _ \ \ / / _ \
\__ \.___/ / | |  __/ |_| |  | |  __/\ V /  __/
|___/\____/|_|  \___|\__|_|  |_|\___| \_/ \___|
                                               
                                               
"""

Gstr_synopsis = """

    NAME

       s3retrieve.py 

    SYNOPSIS

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

    BRIEF EXAMPLE

        * Bare bones execution

            docker run --rm -u $(id -u)                             \
                -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing      \
                fnndsc/pl-s3retrieve s3retrieve                        \
                /incoming /outgoing

    DESCRIPTION

        `s3retrieve.py` is an app to retrieve data of interest from Amazon S3 service.

    ARGS

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
"""


class S3RetrieveApp(ChrisApp):
    """
    Retrieve a file/folder from Amazon S3 service.
    """
    PACKAGE                 = __package__
    TITLE                   = 'S3 Retrieve'
    CATEGORY                = ''
    TYPE                    = 'ds'
    ICON                    = '' # url of an icon image
    MAX_NUMBER_OF_WORKERS   = 1  # Override with integer value
    MIN_NUMBER_OF_WORKERS   = 1  # Override with integer value
    MAX_CPU_LIMIT           = '' # Override with millicore value as string, e.g. '2000m'
    MIN_CPU_LIMIT           = '' # Override with millicore value as string, e.g. '2000m'
    MAX_MEMORY_LIMIT        = '' # Override with string, e.g. '1Gi', '2000Mi'
    MIN_MEMORY_LIMIT        = '' # Override with string, e.g. '1Gi', '2000Mi'
    MIN_GPU_LIMIT           = 0  # Override with the minimum number of GPUs, as an integer, for your plugin
    MAX_GPU_LIMIT           = 0  # Override with the maximum number of GPUs, as an integer, for your plugin

    # Use this dictionary structure to provide key-value output descriptive information
    # that may be useful for the next downstream plugin. For example:
    #
    # {
    #   "finalOutputFile":  "final/file.out",
    #   "viewer":           "genericTextViewer",
    # }
    #
    # The above dictionary is saved when plugin is called with a ``--saveoutputmeta``
    # flag. Note also that all file paths are relative to the system specified
    # output directory.
    OUTPUT_META_DICT = {}

    def define_parameters(self):
        """
        Define the CLI arguments accepted by this plugin app.
        Use self.add_argument to specify a new app argument.
        """
        self.add_argument('--bucket', dest='bucket', type=str, optional=False,
                          help='name of the Amazon S3 bucket')
        self.add_argument('--prefix', dest='prefix', type=str, default='', optional=True,
                          help='retrieve directory/file prefix path in s3')
        self.add_argument('--awskeyid', dest='awskeyid', type=str,
                          optional=False, help='aws access key id')
        self.add_argument('--awssecretkey', dest='awssecretkey',
                          type=str, optional=False, help='aws secret access key')

    def run(self, options):
        """
        Define the code to be run by this plugin app.
        """
        print(Gstr_title)
        print('Version: %s' % self.get_version())

        # get Amazon S3 credentials
        if options.awskeyid and options.awssecretkey:
            s3client = boto3.client(
                's3',
                aws_access_key_id=options.awskeyid,
                aws_secret_access_key=options.awssecretkey
            )
        else:
            s3client = boto3.client('s3')

        # get Amazon S3 path (s3 file storage key)
        prefix = options.prefix
        if not prefix: # path passed through CLI has priority over JSON meta file
            prefix = self.load_output_meta()['prefix']

        # download folder/file from Amazon S3
        item = {'Key': ''}
        while True:
            response = s3client.list_objects(Bucket=options.bucket, MaxKeys=200,
                                             Prefix=prefix, Marker=item['Key'])
            for item in response['Contents']:
                dirname = os.path.join(options.outputdir, os.path.dirname(item['Key']))
                if not os.path.exists(dirname):
                    os.makedirs(dirname)
                s3client.download_file(options.bucket, item['Key'],
                                       os.path.join(options.outputdir, item['Key']))
            if not response['IsTruncated']: break

    def show_man_page(self):
        """
        Print the app's man page.
        """
        print(Gstr_synopsis)
