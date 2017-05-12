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
    SELFPATH        = os.path.dirname(__file__)
    SELFEXEC        = os.path.basename(__file__)
    EXECSHELL       = 'python3'
    TITLE           = 'S3 Retrieve'
    CATEGORY        = ''
    TYPE            = 'ds'
    DESCRIPTION     = 'An app to retrieve data of interest from Amazon S3 service'
    DOCUMENTATION   = 'http://wiki'
    LICENSE         = 'Opensource (MIT)'
    VERSION         = '0.1'

    def define_parameters(self):
        self.add_parameter('--bucket', action='store', dest='dir', type=str, default='./',
                           optional=False, help='name of the Amazon S3 bucket')
        self.add_parameter('--s3path', action='store', dest='dir', type=str,
                           optional=False, help='retrieve directory/file path in s3')

    def run(self, options):
        s3client = boto3.client('s3')
        # this doesn't consider truncated response!
        # https://boto3.readthedocs.io/en/latest/reference/services/s3.html#S3.Client.list_objects
        response = s3client.list_objects(Bucket=options.bucket, Prefix=options.s3path)
        for key in response[Contents]:
            s3client.download_file(options.bucket, key,
                                   os.path.join(options.outputdir, options.s3path))



# ENTRYPOINT
if __name__ == "__main__":
    app = S3RetrieveApp()
    app.launch()
