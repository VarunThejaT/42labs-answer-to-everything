# trial to upload the files to s3 bucket 
import boto3
s3 = boto3.resource('s3')
BUCKET = "42labs-audio-files"
# uploading search.py file as a sample 
s3.Bucket(BUCKET).upload_file("search.py", "sample_upload.py")