import boto3

# Create an S3 access object
s3 = boto3.client("s3")

s3.upload_file(
    Filename="/Users/vaibhavkesarwani/Desktop/ORM Session/upload.txt",
    Bucket="test1234567891234567",
    Key="Vaibhav Uploaded here",
)