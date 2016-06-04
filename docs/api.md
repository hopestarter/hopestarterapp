# API Spec (prelim)

The API is accessible via HTTP (over HTTPS in production) and all API resources are assumed to be
under a particular base URL. This base API endpoint URL should be configurable
via some developer option, i.e. it should not require rebuilding the app to use
a different endpoint. For example it could be one of these:

* https://api.hopestarter.org/
* https://www.hopestarter.org/api/
* http://localhost:8000/api/

In the following examples we will use the third option.

## Versioning

TBD

Probably a _Accept_ header with a JSON based MIME type which includes the version, like GitHub.

## Authentication with user credentials via mobile app


For user authentication in the API we use OAuth 2.0 with bearer tokens. A valid token authenticates the client's user and authorizes the client to act on behalf of the user based on the token scope. Valid token scopes are:

1. `update-profile`
1. `set-location`

The URLs we will use are:

### Token request (_/o/token/_)

We use the [Resource owner password credentials](http://tools.ietf.org/html/rfc6749#section-4.3) flow of OAuth 2.0. Given a Client ID and Secret (common between users of the mobile app) the app will:

1. ask the user for their username and password
2. issue a POST request, e.g.:

    $ curl -X POST -d "grant_type=password&username=<user_name>&password=<password>&scope=set-location" -u"<client_id>:<client_secret>" http:///localhost:8000/api/o/token/
	{
		"access_token": "<your_access_token>",
		"token_type": "Bearer",
		"expires_in": 36000,
		"refresh_token": "<your_refresh_token>",
        "scope": "set-location"
	}

3. Save the token to application storage for future API requests.
4. Use the token in request to the server e.g.:

	$ curl -H "Authorization: Bearer <your_access_token>" -X GET http://localhost:8000/api/some/api/method/


If you want to request a token with multiple scopes separate the scopes with a space character, e.g. in URL encoding: `scope=update-profile%20set-location`.

##  Authentication with social network identity via mobile app (_/o/auth/_)

TBD

This will require more work from client, to get an OAuth token from an external service like Facebook, then convert the token to one for the Hopestarter API, e.g.:

	$  curl -H “Authorization: Bearer facebook <facebook_token>” http://localhost:8000/api/auth/convert-token

## Upload an image (_/collector/uploadimage/_)

Images are uploaded to Amazon S3, using temporary credentials that are provided by the API upon request. The format of the response is JSON, e.g.

	$ curl -H "Authorization: Bearer <your_access_token>" http://localhost:8000/api/collector/uploadimage/
	{
		"credentials": {
			"SecretAccessKey": "DN+sl0x70vEeOQ/SnZ2bIw3kCffNmZShYdugPev6",
			"SessionToken": "AQoDYXdzEIr//////////wEa4AOKXpr4sdNUC9kmBQtq37tysrkhVVh4KisYbK6uuwYv7lMo+8OTBOMlinT+Xvl76bffICkPR4bzmYFy1BsbwNs9igbwshrlmbbGqo76PGg5xaj3zad/1nNNZDm0j15DWnF46a1Z+mdupnzWxLo2UAxMBkH9XhCOGDj9Ggha9fkvp6zSUjBE+KDZAcd5qQu7O+238Mkxiv+7Oay4U3cr3v6M1aDJMUFq5UCP3xKjyny2cNOfwTMiyPK0GXypeua5mAWdawaxKB0AO/a/11Xih63mgHR+uFZT0yaAbctkE+Mj0iyD5OfPBQP2Eo8AqjJIf8R0IMvvB2oRlaN26ELl1hNZbVKICLKd2Uj6asPeav2G/X4lJaAL6lM6dekqThr0X0BJdhlVbhtMhZWt6ZdxcWZY8aUeIL2R006OMmVDo55kxD+UGRk4MV7uxU8rk3wc2Ucxh/jMHuN5tISt2fDNao0/XarzHhgtU8cVjskmchfeHSx/PhRD/+EY8gDAb/lwGcXZHJVgkdBK64IRQtQhBdgmcTkI/PhndsrMxWmtK9XzCOTFsX9zlXlq4vh7QCggy0glqpLCC9pNxgSW4DRM8GYoNQrEX8zlqauSNK6PSmEw6tDpotO7M8AxMaln5iaKDO8gpdGLtgU=",
			"Expiration": "2016-02-16T09:30:17Z",
			"AccessKeyId": "ASIAIEOLIJYCF7GLM53Q"
		},
		"bucket": {
			"region": "eu-west-1",
			"prefix": "uploads/d6ba9804-6632-472e-8318-ce4f66a4970a/",
			"name": "hopebucket"
		}
	}

The keys and token attributes correspond to the attributes of the
[AWSSessionCredentials](http://docs.aws.amazon.com/AWSAndroidSDK/latest/javadoc/com/amazonaws/auth/AWSSessionCredentials.html)
class in the Android AWS SDK. The app should upload the image to the bucket
under the prefix specified and using the filename of it's choosing. E.g. the S3
URL might be:

	s3://hopebucket/uploads/70e03e9b-242a-49a6-85fa-cba18dabeebd/123456/myfamily.jpg

For example with the AWS CLI tool you can do:

	env AWS_ACCESS_KEY_ID=ASIAIEOLIJYCF7GLM53Q \
 		AWS_SECRET_ACCESS_KEY="DN+sl0x70vEeOQ/SnZ2bIw3kCffNmZShYdugPev6" \
		AWS_SESSION_TOKEN="AQoDYXdzEIr//////////wEa..."  \
		 aws s3 cp ~/Downloads/HappyFace.jpg s3://hopebucket/uploads/d6ba9804-6632-472e-8318-ce4f66a4970a/smileyface.jpg


## Submit a new user position (_/collector/mark/_)

Important: This operation requires a token the `set-location` scope (see example above). We submit a _POST_ request to the API which includes location data in JSON, e.g.

	{
		"created": "2012-08-22T16:20:09.822+00:00",
		"point": {
			"type": "point",
			"coordinates": [1000, 1000]
		},
        "picture": [
            {
                "url": "s3://staginghopestarterimageupload/uploads/4d45d9f3-956f-4939-972c-cd33b0bd945c/profile.jpg"
            }
        ]
	}

	$ curl -H "Authorization: Bearer <your_access_token>" -X POST -H "Content-Type: application/json" -d "$JSON_BODY"  http://localhost:8000/api/collector/mark/

The server responds with `202 Created` upon succesfull validation of the data.

Request attributes:
* `created`: an ISO formatted timestamp of when this position was recorded (timezone information is required, for example above, the timezone is UTC).
* `point`: a Geo-JSON formatted feature specification. `type` is required to be `point`.
* `picture`: a list of S3 URLs of previously uploaded images.
* `text`: a free text description of the event


## Read user's past positions (_/collector/mark/_)

```
curl -s -H "Authorization: Bearer LLXoqcMuxm3QPIYhmL9I1SJp7oNMD5" http://127.0.0.1:8000/api/collector/mark/ | python -m json.tool
{
    "count": 8,
    "next": null,
    "previous": null,
    "results": {
        "features": [
            {
                "geometry": {
                    "coordinates": [
                        1000.0,
                        1000.0
                    ],
                    "type": "Point"
                },
                "properties": {
                    "created": "2016-08-22T16:20:09.822000Z",
                    "text": "Finally we arrived..",
                    "picture": [
                        {
                            "url": "https://d2uc1tz5ijwlrf.cloudfront.net/images/medium/uploads/4d45d9f3-956f-4939-972c-cd33b0bd945c/profile.jpg"
                        }
					]
                },
                "type": "Feature"
            },
            {
                "geometry": {
                    "coordinates": [
                        123.0,
                        123.0
                    ],
                    "type": "Point"
                },
                "properties": {
                    "created": "2012-08-22T16:20:09.822000Z",
                    "text": "Still not there yet..",
                    "picture": [
                        {
                            "url": "https://d2uc1tz5ijwlrf.cloudfront.net/images/medium/uploads/4d45d9f3-956f-4939-972c-cd33b0bd945c/profile.jpg"
                        }
					]
                },
                "type": "Feature"
            },
			...
		]
	}
}
```

Filtering on the `created` field is possible. Also ordering based on the `created` field. TODO add some examples.


## Edit user profile (_/user/profile/_)

To use this endpoint you need a token with `update-profile` scope.

### _GET /user/profile/_

    * Request:
    * Response:
    {
        "created": "2016-02-17T09:22:30.052142Z",
        "modified": "2016-02-17T09:22:30.052153Z",
        "name": "foo",
        "surname": "bar",
        "bitcoin": "xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    }

### _PUT /user/profile/_

    * Request:
    {
        "surname": "mama"
    }
    * Response
    {
        "created": "2016-02-17T09:22:30.052142Z",
        "modified": "2016-02-17T09:26:19.062675Z",
        "name": "foo",
        "surname": "mama",
        "bitcoin": "xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    }


Error messages: TBD
