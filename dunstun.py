import requests, time, twitter, sys, json
    
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
        response = getSiteResponse()
        if int(response["temp"]) > 15 and float(response["rainfall"]) == 0.0:
            tweet = time.asctime() + " It's a dunner stunner today! A nice " + response["temp"] + "° outside."
            print("Tweeting tweet:")
            print(tweet)
            api.PostUpdate(tweet)
        time.sleep(60)