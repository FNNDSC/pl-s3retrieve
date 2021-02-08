
from unittest import TestCase
from unittest import mock
from s3retrieve.s3retrieve import S3RetrieveApp


class S3RetrieveAppTests(TestCase):
    """
    Test S3RetrieveApp.
    """
    def setUp(self):
        self.app = S3RetrieveApp()

    def test_run(self):
        """
        Test the run code.
        """
        args = []
        if self.app.TYPE == 'ds':
            args.append('inputdir') # you may want to change this inputdir mock
        args.append('outputdir')  # you may want to change this outputdir mock
        args.append('--bucket')
        args.append('bch-fnndsc')
        args.append('--awskeyid')
        args.append('KEYID')
        args.append('--awssecretkey')
        args.append('ACCESSKEY')
        args.append('--prefix')
        args.append('test')


        # you may want to add more of your custom defined optional arguments to test
        # your app with
        # eg.
        # args.append('--custom-int')
        # args.append(10)

        options = self.app.parse_args(args)
        #self.app.run(options)

        # write your own assertions
        self.assertEqual(options.outputdir, 'outputdir')
