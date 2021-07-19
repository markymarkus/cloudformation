#!/bin/bash
s3_bucket_name=my-s3-bucket

mkdir layer
cd layer
python3 -m venv env
source env/bin/activate
mkdir python
pip3 install -r ../requirements.txt  -t python
zip -r requests_layer.zip ./python
deactivate
aws s3 cp requests_layer.zip s3://$s3_bucket_name

echo Layer zip created to s3://$s3_bucket_name/requests_layer.zip 
