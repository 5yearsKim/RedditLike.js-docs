# Setup media with S3

RedditLike.js support media(images, videos) upload. To enable media feature, you need to setup s3 bucket.

1. Create S3 Bucket

You can setup S3 bucket following [this guide](https://docs.aws.amazon.com/AmazonS3/latest/userguide/creating-bucket.html).


2. Get access key and secret key for AWS account

You need `Access Key` and `Secret Key` to connect to AWS bucket. You can check your credentials with [this guide](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html).


3. Fill in `backend/.env` with above credentials. This credentials are required to generated [presigned URLS](https://docs.aws.amazon.com/AmazonS3/latest/userguide/ShareObjectPreSignedURL.html) for s3 object.

```sh
# aws
AWS_ACCESS_KEY_ID=
AWS_SECRET_KEY_ID=
AWS_BUCKET_NAME=
```

4. (Optional) Connect S3 with CloudFront.

Connect S3 bucket with CloudFront following [this guide](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/GettingStarted.SimpleDistribution.html).


5. Fill in `frontend/.env` with access end point, which is S3 bucket or CloudFront distribution domain.

```sh
...
NEXT_PUBLIC_RESOURCE_URL= # S3 or CloudFront endpoint
```



