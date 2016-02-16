AWS related stuff
=================


Setting up access
-----------------

First method is configuring via the AWS CLI:

1. Install the AWS CLI (e.g. `brew install awscli`).
2. Run `aws configure` and add your credentials. Use `--profile` if you have multiple profiles.

Second method is exporting the variables in the environment, e.g.:

    export AWS_ACCESS_KEY_ID=ASIAIEOLIJYCF7GLM53Q
    export AWS_SECRET_ACCESS_KEY="DN+sl0x70vEeOQ/SnZ2bIw3kCffNmZShYdugPev6"


Configuring image resizing Lambda function
------------------------------------------


```
cd src/lambda
zip -r ../lambda.zip *
```

Upload the `lambda.zip` file to the AWS Lambda console. Tada!
