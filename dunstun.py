import os, requests, twitter, sys, json, datetime, pytz

API_KEY =  os.environ.get('API_KEY')
API_SECRET = os.environ.get('API_SECRET')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_SECRET = os.environ.get('ACCESS_SECRET')

def season(some_date):
    """Returns the current season."""
    autumn = range(80, 172) # 21 March - 20 June
    winter = range(173, 266) # 21 June - 22 September
    spring = range(267, 361) # 23 September - 21 December
    # Summer is anything else.
    day = some_date.timetuple().tm_yday

    if day in autumn:
        return "autumn"
    elif day in winter:
        return "winter"
    elif day in spring:
        return "spring"
    else:
        return "summer"
    
    
def getSiteResponse():
    """Return the three hour forecast from metservice.co.nz."""
    URL = "http://metservice.com/publicData/"
    
    URL = ''.join([URL, "localObs_", "dunedin"])
    try:
        page = requests.get(URL)
    except:
        print("The webpage is down.")
        return

    return json.loads(page.text)["threeHour"]

def post_tweet(request):

    api = twitter.Api(consumer_key=API_KEY, consumer_secret=API_SECRET,
        access_token_key=ACCESS_TOKEN, access_token_secret=ACCESS_SECRET)

    nz_date = datetime.datetime.now(tz=pytz.timezone("Pacific/Auckland"))
    current_season = season(nz_date)
    response = getSiteResponse()

    if current_season == "summer":
        base_temp = 20
    elif current_season == "autumn":
        base_temp = 15
    elif current_season == "winter":
        base_temp = 14
    elif current_season == "spring":
        base_temp = 15

    if int(response["temp"]) >= base_temp and float(response["rainfall"]) == 0.0:
        tweet = nz_date.ctime() + " It's a dunner stunner today! A beautiful " + response["temp"] + "° outside."
    else:
        tweet = nz_date.ctime() + " It's " + response["temp"] + "° outside in Dunedin today."

    print("Tweeting tweet:")
    print(tweet)
    api.PostUpdate(tweet)
    x = {"tweet": tweet,
        "base_temp": base_temp,
        "temp": response["temp"],
        "rainfall": response["rainfall"],
        "season": current_season}
    return json.dumps(x)

if __name__ == "__main__":
    post_tweet({})