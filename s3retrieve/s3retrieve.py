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
import json


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
    VERSION         = '0.1'

    def define_parameters(self):
        self.add_argument('--bucket', dest='bucket', type=str, optional=False,
                          help='name of the Amazon S3 bucket')
        self.add_argument('--s3path', dest='s3path', type=str, default='', optional=True,
                          help='retrieve directory/file path in s3')

    def run(self, options):
        # get the path on Amazon S3
        s3path = options.s3path
        if not s3path: # path passed through CLI has priority over JSON file
            s3_path_file = os.path.join(options.inputdir, 's3path.json')
            if os.path.exists(s3_path_file):
                with open(s3_path_file) as path_file:
                    data = json.load(path_file)
                s3path = data['s3path']

        # download folder/file from Amazon S3
        s3client = boto3.client('s3')
        item = {'Key': ''}
        while True:
            response = s3client.list_objects(Bucket=options.bucket, MaxKeys=200,
                                             Prefix=s3path, Marker=item['Key'])
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
