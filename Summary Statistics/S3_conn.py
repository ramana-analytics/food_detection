from multiprocessing.connection import Client
import boto3  # pip install boto3

# # Let's use Amazon S3
# s3 = boto3.resource("s3")

# # Creating the low level functional client
client = boto3.client(
    's3',
    aws_access_key_id = 'AKIA4LEBWJVEL3RUNXWI',
    aws_secret_access_key = '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',
    region_name = 'us-east-1'
)
    
# # Creating the high level object oriented interface
resource = boto3.resource(
    's3',
    aws_access_key_id = 'AKIA4LEBWJVEL3RUNXWI',
    aws_secret_access_key = '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',
    region_name = 'us-east-1'
)


# import boto3
# s3 = boto3.resource('s3')
# s3.Bucket('arn:aws:s3:us-east-1:848528035144:accesspoint/fsuserupload').download_file('download.jpg', '/image_uploads/download.jpg')

# s3.Bucket('fsuserupload').download_file('download.jpg', '/image_uploads/download.jpg')

# Print out bucket names
# for bucket in resource.buckets.all():
#     print(bucket.name)

# file_name = "download.jpg"
# key = "image_uploads/" + file_name
# print(key)
# # s3 = boto3.client("s3")    
# client.upload_file(
#     Filename= file_name,
#     Bucket="fsuserupload",
#     Key= key,
# )

# # s3.download_file(
# #     Bucket="foodscription-py-app",
# #     Key="image_uploads/download.jpg", 
# #     Filename="downloadAWS2.jpg"
# # )