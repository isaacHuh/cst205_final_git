import twitter

consumer_key = 'RFGVvCnGc7rcZ9kMa33VGoEe3'
consumer_secret = 'z8kXM3hhsOqfBUMHKewEBqBQZNvqHAfa4hEixQfgafgK2D8Ek9'
access_token = '1070516661717889027-rvZZIfCDoN0IKfUghpae4377bS3UIH'
access_secret = 'pMMBBeuH6YaQmNYhpPTREl5Pke43rtA0QcF6ZXOg6n99U'

api = twitter.Api(consumer_key=consumer_key,
                consumer_secret=consumer_secret,
                access_token_key=access_token,
                access_token_secret=access_secret)

print(api.VerifyCredentials())
post_update = api.PostUpdates(status='interesting')
print(post_update)
new_message = api.PostDirectMessage(screen_name'', text'')
print(new message)
