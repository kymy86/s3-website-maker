import unittest
from moto import mock_s3
from bucket_maker import BucketMaker

class TestApp(unittest.TestCase):
    """
    Test Bucket Maker class
    """

    @mock_s3
    def test_create_bucket(self):
        """
        Test if creation goes fine
        """
        maker = BucketMaker("my-test-bucket-874")
        res, text = maker.create_website("index.html", "error.html", "eu-west-1")
        self.assertEqual(res, True)

    @mock_s3
    def test_delete_bucket(self):
        """
        Test if deletion process goes fine
        """
        maker = BucketMaker("my-test-bucket-874")
        res, text = maker.create_website("index.html", "error.html", "eu-west-1")
        res = maker.delete_bucket()
        self.assertTrue(res)
