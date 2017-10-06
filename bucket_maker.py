import os
import re
import json
import mimetypes
import boto3
from botocore import exceptions

class BucketMaker:

    __PATH__ = 'files'

    def __init__(self, bucket_name):
        self.__client = boto3.client("s3")
        self.__bucket_name = bucket_name

    def __get_bucket_policy(self):
        """
        Return the bucket policy to make all objects in it
        public accessible
        """
        bucket_policy = {
            'Version':'2012-10-17',
            'Statement':[{
                'Sid':'PublicReadGetObject',
                'Effect':'Allow',
                'Principal':'*',
                'Action':["s3:GetObject"],
                'Resource':'arn:aws:s3:::%s/*' % self.__bucket_name
            }]
        }
        return json.dumps(bucket_policy)

    def __upload_file(self, filename, keyname):
        """
        Upload a file on the bucket
        """
        mimetypes.init()
        mime_type = mimetypes.guess_type(filename)
        if mime_type[0] is not None:
            print("Uploading {}".format(keyname))
            self.__client.upload_file(filename,
                                      self.__bucket_name,
                                      keyname,
                                      ExtraArgs={'ContentType':mime_type[0]})

    def __bucket_exists(self):
        """
        Chek if the bucket exists
        """
        try:
            self.__client.head_bucket(Bucket=self.__bucket_name)
            return True
        except exceptions.ClientError as Error:
            return False

    def upload(self):
        """
        Upload recursively all files and folders in the __PATH__
        directory
        """
        for root, dirs, files in os.walk(self.__PATH__):
            for filename in files:
                if not filename.startswith("."):
                    local_p = os.path.join(root, filename)
                    keyname = re.sub(r'files\/', '', local_p)
                    self.__upload_file(local_p, keyname)

    def __build_url(self, region):
        """
        Return the website URL
        """
        return "http://"+self.__bucket_name+".s3-website-"+region+".amazonaws.com"

    def delete_bucket(self):
        """
        If bucket exists, remove it
        """
        if self.__bucket_exists():
            bucket = boto3.resource('s3').Bucket(self.__bucket_name)
            bucket.objects.all().delete()
            bucket.delete()
            return True

    def create_bucket(self, index, error, region):
        """
        Create a bucket and enable the website hosting
        feature
        """

        self.__client.create_bucket(
            ACL='public-read',
            Bucket=self.__bucket_name,
            CreateBucketConfiguration={
                'LocationConstraint':region
            }
        )

        self.__client.put_bucket_policy(
            Bucket=self.__bucket_name,
            Policy=self.__get_bucket_policy())

        self.__client.put_bucket_website(
            Bucket=self.__bucket_name,
            WebsiteConfiguration={
                "ErrorDocument":{
                    'Key':error
                },
                "IndexDocument":{
                    'Suffix':index
                }
            }
        )

    def create_website(self, index_page, error_page, region):
        """
        If bucket not yet exists, create it by enabling the
        website feature.
        """

        if not self.__bucket_exists():
            try:
                self.create_bucket(index_page, error_page, region)
                print("Uploading files....")
                self.upload()
                return True, self.__build_url(region)
            except exceptions.ClientError as cerror:
                return False, cerror
