import requests, time, twitter, sys


## Add checkSite comment here.

# if sunny and warm, return message about current temp and conditions, else
# return None.
def checkSite():
    URL = "https://www.metservice.com/towns-cities/locations/dunedin"
    try:
        page = requests.get(URL)
    except:
        print("The webpage is down.")
        return

    text = page.text
    start = "" # edit
    end = "" # edit
    size = 0 # edit
    status_start_index = text.index(start)
    status_end_index = text.index(end, status_start_index)
    status = text[status_start_index+size:status_end_index]
    current_temp = float(status)
    return current_temp

# If between daylight hours, sleep for one hour, else sleep until
# morning.
if __name__ == "__main__":
    api = twitter.Api(consumer_key='blank', consumer_secret='blank',
        access_token_key='blank', access_token_secret='blank')

    # The first command line argument can be used to tweet something out.
    if len(sys.argv) == 2:
        tweet = sys.argv[1].strip()
        print("Tweeting tweet:")
        print(tweet)
        api.PostUpdate(tweet)

    while True:

        response = checkSite()
        if response is not None:
            print("Tweeting tweet:")
            print(tweet)
            api.PostUpdate(tweet)
            time.sleep(3600)
