import argparse
from bucket_maker import BucketMaker

def command_line():
    """
    Manage the arguments from command line
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--website_name", help="add your website name here")
    parser.add_argument("-i", "--index_page", help="add your index page here")
    parser.add_argument("-e", "--error_page", help="add your error page here")
    parser.add_argument("-r", "--region", help="region where creating the bucket")
    parser.add_argument("-d", "--delete", help="Delete bucket", action="store_true")
    return parser.parse_args()

if __name__ == '__main__':

    args = command_line()
    maker = BucketMaker(args.website_name)
    if args.delete:
        maker.delete_bucket()
        print("Deleting complete")
    else:
        res, text = maker.create_website(args.index_page, args.error_page, args.region)
        if res:
            print("Uploading complete with url {}".format(text))
        else:
            print(text)
