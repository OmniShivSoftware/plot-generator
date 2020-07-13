#!/bin/bash
set -eo pipefail
echo "Bucket name for Lambda artifacts:"
read artifact_bucket
aws cloudformation package --template-file template.yml --s3-bucket $artifact_bucket --output-template-file out.yml
aws cloudformation deploy --template-file out.yml --stack-name plot-generator --capabilities CAPABILITY_NAMED_IAM
