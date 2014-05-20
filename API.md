
[Source](https://web.archive.org/web/20140426192326/http://tobiass.eu/api-doc.html "Permalink to AudioAddict API documentation - revision 4")

# AudioAddict API documentation - revision 4

### Table of contents

1. Introduction
2. Accessing the API
    1. Addresses and headers
    2. Returned data
    3. Security
3. Resources
    1. About channels
    2. Channels
    3. Track history
    4. Events
    5. Using the batch_update resource
    6. Users
    7. Voting
    8. Favorites
    9. Trial
    10. Other stuff
4. Appendix
    1. Streamlists
    2. Validating listen keys

### 1\. Introduction

AudioAddict Inc. is the company behind the internet radio streaming services Digitally Imported, Sky.fm, JazzRadio.com and RockRadio.com. They have a RESTful API in place, but sadly, it lacks an official documentation. This has been a pain in the ass for a lot of people who wanted to build applications for listening to these streams. That's why I decided to make an unofficial documentation myself. Please note that since this API is not public, everything can change and break at any time! Fortunately, this doesn't happen very often.

Network   | Listen host
----------|------------
di        | listen.di.fm
sky       | listen.sky.fm
jazzradio | listen.jazzradio.com
rockradio | listen.rockradio.com

### 2\. Accessing the API

#### 2.1. Addresses and headers

The API server is located at api.audioaddict.com. A regular request's URL would look like http://api.audioaddict.com/v1/di/track_history. v1 stands for the API's version number. This is always the same. di stands for the streaming network. It's basically the part of the network's domain before the dot (di.fm, jazzradio.com). track_history is a resource, it returns a JSON string with information about the last-played track for the network's channels. Learn more about the resources below.

IMPORTANT: A lot of requests require an Authorization header:

`Authorization: Basic ZXBoZW1lcm9uOmRheWVpcGgwbmVAcHA=`

This is basically the same as using the username "ephemeron" and password "dayeiph0ne@pp".

Some requests require another host name, namely listen.di.fm. This host also supports HTTPS, but there's no need for it. A regular request's URL for this host would look like http://listen.di.fm/public3/trance. In case you want information about another network, replace di.fm with the domain of the network you want to use.

Some requests require a request method that might not always be available, cross-domain JSONP requests for example. The API offers a feature that allows you to fake a request method. When you need to make a DELETE request with JSONP, just add the GET parameter _method to the URL and set it to DELETE. For example: http://api.audioaddict.com/v1/di/tracks/6/vote/1?_method=DELETE&amp;api_key=key will delete a vote. The api_key parameter that is usually sent over DELETE, is now sent over GET.

#### 2.2. Returned data

Every request returns a JSON-encoded object, a string describing an error, or nothing (this is indicated with a "HTTP 204 No Content" status code). These strings can be decoded on almost all platforms. Here are some examples of useful libraries for platforms that don't have a JSON parser built in:

* [JSON.NET][1] : A high-performance JSON parser and writer for .NET. .NET has a built-in JSON parser but this is not available in all .NET versions. Besides, this library delivers [a lot more performance][2] than built-in parsers.

* [JSON.simple][3] : JSON parser and writer for Java.

For some requests, other data types are possible. This can be done by adding an extension to the URL. http://listen.di.fm/public3/trance.pls is an example of this.
All requests support the JSONP data type. This is basically a JSON-encoded object put in a JavaScript function's parameter. The function name must always be given by the GET parameter callback, for example: http://listen.di.fm/public3/trance.jsonp?callback=processStreams.

#### 2.3. Security

The API server supports HTTPS. Use it when you're sending or receiving sensitive information like passwords and such.

### 3\. Resources

#### 3.1. About channels

The streamlist parameter is a key that describes a stream quality and format. These are different for each network. Please see the Streamlists chapter in the appendix for more information.
The key parameter is a key that describes a channel. It's usually just the channel name in lowercase with spaces trimmed, but there are some exceptions.
As of this writing (2014-05-18), `public3` is the only streamlist common across all four networks.  It's used a number of times in this document for quick checks.

#### 3.2. Channels

##### Getting channel information

This request returns a JSON-encoded array with channel objects in it. Every channel object has these fields: key, id, name, description and playlist.

&nbsp; | &nbsp;
-------|-------
Host   | listen.di.fm
HTTPS? | No
URL    | http://listen.di.fm/[streamlist]

##### Getting channel playlists

This request returns a JSON-encoded array with stream URLs in it. The streams are in the bitrate and format specified by the streamlist. The key parameter is the channel's key.
Read more about streamlists in the dedicated chapter.

&nbsp; | &nbsp;
-------|-------
Host   | listen.di.fm
HTTPS? | No
URL    | http://listen.di.fm/[streamlist]/[key]

Possible data types
JSON, JSONP, PLS, ASX (NOTE: The ASX type gives wrong URLs)

Optional parameter
A listen key, the listen key will be appended to all URLs. Example: `trance?[listen_key]`

##### Getting detailed information about channels

This is possible with the batch_update resource, read on!

* * *

#### 3.3. Track history

##### Getting now playing tracks for all channels

This returns an array with track history objects.

&nbsp; | &nbsp;
-------|-------
Host   | api.audioaddict.com
HTTPS? | No
URL    | http://api.audioaddict.com/v1/[NETWORK]/track_history

##### Getting track history for a single channel

This returns an array with track history objects.

&nbsp; | &nbsp;
-------|-------
Host   | api.audioaddict.com
HTTPS? | No
URL    | http://api.audioaddict.com/v1/[NETWORK]/track_history/channel/[channel_id]

##### [Getting information about a single track][4]

* * *

#### 3.4. Events

##### Getting upcoming events for a network

This returns a JSON-encoded array with event objects in it.

&nbsp; | &nbsp;
-------|-------
Host   | api.audioaddict.com
HTTPS? | No
URL    | http://api.audioaddict.com/v1/[NETWORK]/events

##### Getting upcoming events for a channel

This returns a JSON-encoded array with event objects in it. id is the channel's id.

&nbsp; | &nbsp;
-------|-------
Host   | api.audioaddict.com
HTTPS? | No
URL    | http://api.audioaddict.com/v1/[NETWORK]/events/channel/[id]

* * *

#### 3.5. Using the batch_update resource

A DI crew member once said:

> "The batch update request is used for mobile apps to avoid making many API calls, but you are welcome to use it for the time being. With that said, theres no guarantee this won't change moving forward. As I've always said, we do plan on releasing an official API in the future, but theres a lot more involved than just exposing a few REST urls and our API is still evolving."

The batch_update resource can be used for getting a lot of data at once. Here's a list of data in the batch_update's JSON including their location.

* Detailed information about channels - /channel_filters/0/channels/ - array of extended channel objects
* The track objects of the tracks that are currently playing on each channel - /track_history/ - object of track objects, with the channel's id as key.
* Stream URLs for all channels (of specified streamlists) - /streamlists/[key]/channels/index/streams/index/url - index stands for an array's element. key is the streamlist's key.
* Loads of links to assets and channel art - /assets - also in the detailed channel objects (see first item in this list).
* All upcoming events - /events - an array containing event objects.

&nbsp; | &nbsp;
-------|-------
Host   | api.audioaddict.com
HTTPS? | No
URL    | http://api.audioaddict.com/v1/[NETWORK]/mobile/batch_update

Required parameter
A comma-seperated list of streamlists to be included in the data. The list must be given as a GET or POST parameter with the key stream_set_key.

* * *

#### 3.6. Users

##### Logging in

This data contains the listen_key, api_key, the name of the user, whether the user has a premium subscription, and some more.

This returns a JSON-encoded object with information about the user.

&nbsp; | &nbsp;
-------|-------
Host   | api.audioaddict.com
HTTPS? | Yes
URL    | https://api.audioaddict.com/v1/[NETWORK]/members/authenticate

Required parameters
The request must be POST, api_key or username and password must be sent in POST or GET.

##### Registering

This returns a JSON-encoded object with information about the created user.

&nbsp; | &nbsp;
-------|-------
Host   | api.audioaddict.com
HTTPS? | Yes
URL    | https://api.audioaddict.com/v1/[NETWORK]/members

Required parameters
The request must be POST, member[email], member[first_name], member[last_name], member[password] and member[password_confirmation] must be sent in POST or GET.

##### Confirming

This confirms an account. confirmation_token is in the JSON object returned after registering.

&nbsp; | &nbsp;
-------|-------
Host   | www.di.fm
HTTPS? | No
URL    | http://www.di.fm/member/confirm/[confirmation_token]

* * *

#### 3.7. Voting

##### Voting

Track history objects contain a field called track_id. This is important for voting. When you get the track history array per channel, the objects also contain the field votes. This object has two elements called down and up. The values assigned to these keys are integers, these represent the number of up/down votes for a particular track.

##### Getting information about a single track

This returns a JSON-encoded object with information about a single track including the number of votes and whether the track is a mix.

&nbsp; | &nbsp;
-------|-------
Host   | api.audioaddict.com
HTTPS? | No
URL    | http://api.audioaddict.com/v1/[NETWORK]/tracks/[track_id]

This sets a vote for a track to up or down. channel_id stands for the channel the track is or was playing on. NOTE: This feature is available for all networks, even though the voting isn't implemented in those websites.
It returns a JSON-encoded object with the elements up and down, specifying the updated number of votes.

&nbsp; | &nbsp;
-------|-------
Host   | api.audioaddict.com
HTTPS? | Yes
URL    | https://api.audioaddict.com/v1/[NETWORK]/tracks/[track_id]/vote/[channel_id]/[up/down]

Required parameter
The api_key in POST, or the username and password in POST.

##### Retracting a vote

It returns a JSON-encoded object with the elements up and down, specifying the updated number of votes.

&nbsp; | &nbsp;
-------|-------
Host   | api.audioaddict.com
HTTPS? | Yes
URL    | http://api.audioaddict.com/v1/[NETWORK]/tracks/[track_id]/vote/[channel_id]

Required parameter
The api_key in DELETE, or the username and password in DELETE.

* * *

#### 3.8. Favorites

All accounts can keep favorite channels.

##### Reading favorite channels with the listen_key

This returns a playlist with the channel's name in the Title fields. Easy to parse manually.

&nbsp; | &nbsp;
-------|-------
Host   | listen.di.fm
HTTPS? | No
URL    | http://listen.di.fm/public3/favorites.pls?[listen_key]

##### Writing favorite channels with the listen_key

This is not possible.

##### Reading favorite channels with the api_key or username and password

This returns a JSON-encoded array with favorite objects it in. These objects contain position and channel_id elements.

&nbsp; | &nbsp;
-------|-------
Host   | api.audioaddict.com
HTTPS? | Yes
URL    | https://api.audioaddict.com/v1/[NETWORK]/members/1/favorites/channels

Required parameter
The api_key, or the username and password. POST and GET are both allowed.

##### Writing favorite channels with the api_key or username and password

This returns the same data kind of data as above.

&nbsp; | &nbsp;
-------|-------
Host   | api.audioaddict.com
HTTPS? | Yes
URL    | https://api.audioaddict.com/v1/[NETWORK]/members/1/favorites/channels?api_key=[api_key]

Required parameter
Raw JSON payload in POST, in the following format:

```
{"favorites": [
                {"position":1, "channel_id":1},
                {"position":2, "channel_id":2}
              ]
}
```

This header is required:

`Content-Type: application/json`

##### Removing or adding channels

This returns the favorite object of the new channel or HTTP 204 No Content.

&nbsp; | &nbsp;
-------|-------
Host   | api.audioaddict.com
HTTPS? | Yes
URL    | https://api.audioaddict.com/v1/[NETWORK]/members/1/favorites/channel/[channel_id]

Required parameter
Making a POST request adds the channel, making a DELETE request removes it. api_key or username and password in POST/DELETE or GET.

##### Reading favorite channels with the username and password; alternative

This returns a playlist with the channel's name in the Title fields. Easy to parse manually.

&nbsp; | &nbsp;
-------|-------
Host   | listen.di.fm
HTTPS? | The HTTPS certificate is invalid on this domain, that's why this method is not recommended.)
URL    | https://listen.di.fm/public3/favorites.pls?username=[username]&amp;password=[password]

#### 3.9. Trial

AudioAddict offers a free 7-day premium trial period for all accounts.

##### Checking whether a trial is allowed

This returns a JSON-encoded object with one element called allowed, with a value of true or false. It's false when the trial has been activated before.

&nbsp; | &nbsp;
-------|-------
Host   | api.audioaddict.com
HTTPS? | Yes
URL    | https://api.audioaddict.com/v1/[NETWORK]/members/1/subscriptions/trial_allowed/premium-pass?api_key=[api_key] or https://api.audioaddict.com/v1/[NETWORK]/members/1/subscriptions/trial_allowed/premium-pass?username=[username]&amp;password=[password]

##### Activating a trial

This returns HTTP 204 No Content on success, or HTTP 422 Unprocessable Entry on failure, along with a JSON-encoded error message.

&nbsp; | &nbsp;
-------|-------
Host   | api.audioaddict.com
HTTPS? | Yes
URL    | https://api.audioaddict.com/v1/[NETWORK]/members/1/subscriptions/trial/premium-pass?api_key=[api_key] or https://api.audioaddict.com/v1/[NETWORK]/members/1/subscriptions/trial/premium-pass?username=[username]&amp;password=[password]

Required parameter
The request must be POST, and the api_key or username and password must be sent as POST or as a GET parameter.

#### 3.10. Other stuff

##### Send a "Reset password" email

Returns HTTP 204 No Content.

&nbsp; | &nbsp;
-------|-------
Host   | api.audioaddict.com
HTTPS? | Yes
URL    | https://api.audioaddict.com/v1/[NETWORK]/members/send_reset_password

Required parameter
The request must be POST, and the username must be sent as POST or as a GET parameter.

##### Some info about prices

&nbsp; | &nbsp;
-------|-------
Host   | api.audioaddict.com
HTTPS? | No
URL    | http://api.audioaddict.com/v1/[NETWORK]/plans/premium-pass

### 4\. Appendix

:

#### 4.1. Streamlists

Streamlists are lists of stream URLs. All streams in a streamlist have the same format and bitrate.  While there's a fair degree of overlap in the names and formats, they're not uniform across all networks.

I've been unable to find any API endpoint that enumerates all of a network's streamlists, hence having to include them in here.  The names were obtained by inspecting the websites, as well as using a debugging HTTP proxy with the iOS and Android Apps.

##### All Streamlist Names

***All data is as of 2014-05-20***

Streamlist name         | Bitrate      | Codec
------------------------|--------------|--------------
public1                 | VARIES       | aac
~~public2~~             | ~~VARIES~~   | ~~aac~~
public3                 | VARIES       | mp3
public5                 | VARIES       | mp3
&nbsp;                  | &nbsp;       | &nbsp;
~~premium_low~~         | ~~40k~~      | ~~aac~~
premium_medium          | 64k          | aac
premium                 | 128k         | aac
premium_high            | 256k         | mp3
&nbsp;                  | &nbsp;       | &nbsp;
android_low             | 40k          | aac
android                 | 64k          | aac
~~android_high~~        | ~~64k~~      | ~~aac~~
~~android_premium_low~~ | ~~40k~~      | ~~aac~~
android_premium_medium  | 64k          | aac
android_premium         | 128k         | aac
android_premium_high    | 256k         | mp3
&nbsp;                  | &nbsp;       | &nbsp;
appleapp_low            | 40k          | aac
appleapp                | 64k          | aac
~~appleapp_high~~       | ~~64k~~      | ~~aac~~
appleapp_premium_medium | 64k          | aac
appleapp_premium        | 128k         | aac
appleapp_premium_high   | 256k         | mp3

Notes:

* ~~struckthrough~~ streams (e.g. ~~android_high~~) are either ***INVALID*** or malformed on one or more networks.
* The `public*` streams are a bit of a mess.  See the individual networks details.
* `public3` is a relatively safe default for dev/testing.  It's mp3 and is present on all networks.  *Caveat*: `public3` is 64k mp3 on Jazz, but 96k mp3 everywhere else.
* `public5` appears to have previously been 40k wma.  It's now a duplicate of `public3`.
* `android_high` and `appleapp_high` should be avoided.  For Jazz & Rock, they are outright invalid (i.e., you get an HTTP 500 response).  For Sky and DI, they are just duplicates of `android`/`appleapp` (64k aac).  The Sky and DI metadata in batch_update says they're going to be removed soon.


##### di/Digitally Imported
* `android_high` and `appleapp_high` are valid but should be avoided. The metadata implies they're deprecated.
* `android_premium_low` and `premium_low` appear safe.

Streamlist name         | Bitrate      | Codec
------------------------|--------------|--------------
public1                 | 64k          | aac
public2                 | 40k          | aac
public3                 | 96k          | mp3
public5                 | 96k          | mp3
&nbsp;                  | &nbsp;       | &nbsp;
android_premium_low     | 40k          | aac
premium_low             | 40k          | aac
&nbsp;                  | &nbsp;       | &nbsp;
~~android_high~~        | ~~64k~~      | ~~aac~~
~~appleapp_high~~       | ~~64k~~      | ~~aac~~


##### Sky
* `public2` is ***INVALID*** for Sky
* `android_high` and `appleapp_high` are valid but should be avoided. The metadata implies they're deprecated.
* `android_premium_low` and `premium_low` appear safe.

Streamlist name         | Bitrate      | Codec
------------------------|--------------|--------------
public1                 | 40k          | aac
public3                 | 96k          | mp3
public5                 | 96k          | mp3
&nbsp;                  | &nbsp;       | &nbsp;
android_premium_low     | 40k          | aac
premium_low             | 40k          | aac
&nbsp;                  | &nbsp;       | &nbsp;
~~android_high~~        | ~~64k~~      | ~~aac~~
~~appleapp_high~~       | ~~64k~~      | ~~aac~~


##### RockRadio
* `android_high` and `appleapp_high` are ***INVALID*** for RockRadio
* `android_premium_low` and `premium_low` should be considered ***INVALID*** for RockRadio.  batch_update returns metadata but no streaming URLs.

Streamlist name         | Bitrate      | Codec
------------------------|--------------|--------------
public1                 | 40k          | aac
public2                 | 64k          | aac
public3                 | 96k          | mp3
public5                 | 96k          | mp3


##### JazzRadio
* `android_high` and `appleapp_high` are ***INVALID*** for JazzRadio
* `public2` is ***INVALID*** for JazzRadio
* `android_premium_low` and `premium_low` appear safe.

Streamlist name         | Bitrate      | Codec
------------------------|--------------|--------------
public1                 | 40k          | aac
public3                 | 64k          | mp3
public5                 | 64k          | mp3
&nbsp;                  | &nbsp;       | &nbsp;
android_premium_low     | 40k          | aac
premium_low             | 40k          | aac


#### 4.2. Validating listen keys

There's no good way to do this, therefore it's better to let users log in using their email and password. If it's really required, here's a way:

1. Try to download the favorites playlist: http://[LISTEN_HOST]/public3/favorites?[listen_key]. If this fails, the key is invalid.
2. Try to connect to a premium stream, if this fails, the key is not premium.

I use [this Java class][5] for validating listen keys in my app, feel free to use it.

[1]: https://web.archive.org/web/20140426192326/http%3A/james.newtonking.com/projects/json-net.aspx
[2]: https://web.archive.org/web/20140426192326/http%3A/james.newtonking.com/images/jsonperformance.png
[3]: https://web.archive.org/web/20140426192326/https%3A/code.google.com/p/json-simple/
[4]: https://web.archive.org/web/20140426192326/http%3A/tobiass.eu/api-doc.html#trackinfo
[5]: https://web.archive.org/web/20140426192326/http%3A/pastebin.com/E7p9vMFU
