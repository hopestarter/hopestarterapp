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

##  Authentication with social network identity via mobile app (_/o/auth/_)

TBD

This will require more work from client, to get an OAuth token from an external service like Facebook, then convert the token to one for the Hopestarter API, e.g.:

	$  curl -H “Authorization: Bearer facebook <facebook_token>” http://localhost:8000/api/auth/convert-token

## Upload an image (_/collector/uploadimage/_)

Images are uploaded to Amazon S3, using temporary credentials that are provided by the API upon request. The format of the response is JSON, e.g.

	$ curl -H "Authorization: Bearer <your_access_token>" http://localhost:8000/api/collector/uploadimage/
	{
		"access_key_id": "ACCESSKEY",
		"secret_access_key": "SECRETKEY",
		"session_token": "TOKEN",
		"bucket_name": "hopebucket",
		"bucket_prefix": "uploads/70e03e9b-242a-49a6-85fa-cba18dabeebd/userid/"
	}

The keys and token attributes correspond to the attributes of the
[AWSSessionCredentials](http://docs.aws.amazon.com/AWSAndroidSDK/latest/javadoc/com/amazonaws/auth/AWSSessionCredentials.html)
class in the Android AWS SDK. The app should upload the image to the bucket
under the prefix specified and using the filename of it's choosing. E.g. the S3
URL might be:

	s3://hopebucket/uploads/70e03e9b-242a-49a6-85fa-cba18dabeebd/123456/myfamily.jpg


## Submit a new user position (_/collector/mark/_)

Important: This operation requires a token the `set-location` scope (see example above). We submit a _POST_ request to the API which includes location data in JSON, e.g.

	{
		"created": "2012-08-22T16:20:09.822",
		"point": {
			"type": "point",
			"coordinates": [1000, 1000]
		},
		"image_url": "s3://hopebucket/uploads/70e03e9b-242a-49a6-85fa-cba18dabeebd/123456/myfamily.jpg"
	}

	$ curl -H "Authorization: Bearer <your_access_token>" -X POST -H "Content-Type: application/json" -d "$JSON_BODY"  http://localhost:8000/api/collector/mark/

The server responds with `202 Created` upon succesfull validation of the data.

Error messages: TBD
