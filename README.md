# twitbot-reminder

Twitbot written in Python in order to twit preconfigured reminders.

## Why?

The main reason is to use Python in a personal project and the Twitter API.

## Previous steps

It is necessary to create a twitter application, with its own oauth credentials. This way, the application can post tweets by itself.

In the link apps.twitter.com, you can create a new app. After creating the app, go to the the access tokens.

Save the following fields:

* Consumer Key (API Key)
* Consumer Secret (API Secret)
* Access Token
* Access Token Secret

The bot can publish the tweets through the account that created the application.

## Installation

The Python package "twitter" is required.

This project has been developed and tested using Python3.

## Execution

Create your own reminders. Currently, the remidners must be in a a json file. In the folder sample, you can find an example (reminders.json).

The format for each reminder is:

```json
 {
    "month": numeric from 1 (January) to 12 (December),
    "dayOfMonth": numeric from 1 to 31,
    "text": text with the message to tweet
 }
```

Change the config file (properties.json), with your twitter credentials and your twitter nickname.

```json
 {
   "connection": {
     "consumer-key": "text with the consumer-key",
     "consumer-secret": "text with the consumer-secret",
     "access-token": "text with the access-token",
     "access-token-secret": "text with the access-token-secret"
   },
   "me": "text with your nickname (with no '@' at the begining)"
   "greeting" : "text with the greeting."
 }
```

Each post will be composed by the greeting, the mention to you, and the text of the reminder.

To run the bot:

> python3 bot.py -c _config_

where _config_ is the folder containing reminders.json and properties.json (sample is the default folder)

## Next steps

* Store the reminders in a database.
* Store the published tweets to avoid duplicates.
* Answer to mentions with new tweets.



