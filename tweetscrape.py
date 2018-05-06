import tweepy
import datetime

auth = tweepy.OAuthHandler("2DDepQNXr4h3Uubm5TolYq34t", "gxiJ3OGLxikjhFPLawruYk8WHVtX4eFbqZ6rqndUqqm7aC27ev")
auth.set_access_token("931147713885949952-2aBpA6uBrxp7RsfShe6giz93AI07YFf", "U2mYjfd365tarRZnxTnNwtcOCFHyyj7rOTXJmbC01EDu3")

api = tweepy.API(auth)
trump = "@realDonaldTrump"

dates=[]
text=[]
end_date =  datetime.datetime.utcnow() - datetime.timedelta(days=3600)
for status in tweepy.Cursor(api.user_timeline, id=trump).items():
	dates.append(status.created_at)
	text.append(status.text)
	if status.created_at < end_date:
		break
print(dates[-1])
print(len(text))
companies = ["ecorp", "shell", "verizon"]
companyTweet = {}
for company in companies:
	for c, tweet in enumerate(text):
		if company in tweet:
			companyTweet[dates[c]] = company
print(companyTweet)