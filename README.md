S3 Website Maker
============

Command line app to create a website on a S3 bucket.

## Quickstart

1. Install [awscli]() command utility
2. Copy all the website files in the **files** directory
3. Run the python cli app **app.py** with the following params:

[awscli]:https://aws.amazon.com/cli/

`--website-name`: name of the bucket where the website will be hosted
`--index-page`: the index page of your website
`--error-page`: the error page of your website
`--region`: the region where the bucker will be created

**N.B.** All the params are required.

## Example

`python app.py --website-name my-bucket --index-page index.html --error-page error.html --region eu-west-1`

## Delete a bucket

To delete a bucket previously created, you can prepend the `--delete` option:

`python app.py --website-name my-bucket --index-page index.html --error-page error.html --region eu-west-1 --delete`





