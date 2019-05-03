#                                                            _
# S3 Retrieve ds app
#
# (c) 2016 Fetal-Neonatal Neuroimaging & Developmental Science Center
#                   Boston Children's Hospital
#
#              http://childrenshospital.org/FNNDSC/
#                        dev@babyMRI.org
#

import os

# import the Chris app superclass
from chrisapp.base import ChrisApp
import boto3


class S3RetrieveApp(ChrisApp):
    """
    Retrieve a file/folder from Amazon S3 service.
    """
    AUTHORS         = 'FNNDSC (dev@babyMRI.org)'
    SELFPATH        = os.path.dirname(os.path.abspath(__file__))
    SELFEXEC        = os.path.basename(__file__)
    EXECSHELL       = 'python3'
    TITLE           = 'S3 Retrieve'
    CATEGORY        = ''
    TYPE            = 'ds'
    DESCRIPTION     = 'An app to retrieve data of interest from Amazon S3 service'
    DOCUMENTATION   = 'http://wiki'
    LICENSE         = 'Opensource (MIT)'
    VERSION         = '0.1.1'
    MAX_NUMBER_OF_WORKERS = 1  # Override with integer value
    MIN_NUMBER_OF_WORKERS = 1  # Override with integer value
    MAX_CPU_LIMIT = ''  # Override with millicore value as string, e.g. '2000m'
    MIN_CPU_LIMIT = ''  # Override with millicore value as string, e.g. '2000m'
    MAX_MEMORY_LIMIT = ''  # Override with string, e.g. '1Gi', '2000Mi'
    MIN_MEMORY_LIMIT = ''  # Override with string, e.g. '1Gi', '2000Mi'
    MIN_GPU_LIMIT = 0  # Override with the minimum number of GPUs, as an integer, for your plugin
    MAX_GPU_LIMIT = 0  # Override with the maximum number of GPUs, as an integer, for your plugin

    # Fill out this with key-value output descriptive info (such as an output file path
    # relative to the output dir) that you want to save to the output meta file when
    # called with the --saveoutputmeta flag
    OUTPUT_META_DICT = {}

    def define_parameters(self):
        """
        Define the CLI arguments accepted by this plugin app.
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



# ENTRYPOINT
if __name__ == "__main__":
    app = S3RetrieveApp()
    app.launch()
