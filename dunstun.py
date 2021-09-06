import requests, time, twitter, sys, json
from datetime import date

def season(some_date):
    """Returns the current season."""
    autumn = range(80, 172) # 21 March - 20 June
    winter = range(173, 266) # 21 June - 22 September
    spring = range(267, 256) # 23 September - 21 December
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

if __name__ == "__main__":

    api = twitter.Api(consumer_key='blank', consumer_secret='blank',
        access_token_key='blank', access_token_secret='blank')

    # The first command line argument can be used to send a tweet.
    if len(sys.argv) == 2:
        tweet = sys.argv[1].strip()
        print("Tweeting tweet:")
        print(tweet)
        api.PostUpdate(tweet)

    while True:
        current_season = season(date.today())
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
            tweet = time.asctime() + " It's a dunner stunner today! A beautiful " + response["temp"] + "° outside."
        else:
            tweet = time.asctime() + " It's " + response["temp"] + "° outside in Dunedin today."

        print("Tweeting tweet:")
        print(tweet)
        # api.PostUpdate(tweet)
        time.sleep(60)