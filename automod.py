import sys
import time
import logging
import json
import praw
import thread
 
# Reddit functions
def getReddit(settings):
    """Get a reference to Reddit."""
    r = praw.Reddit(user_agent=settings["reddit_ua"])
    try:
        r.login(settings["reddit_username"], settings["reddit_password"])
    except:
        logging.exception("Error logging into Reddit.")
        exitApp()
    return r
 
def getSubreddit(settings, reddit):
    """Get the subreddit."""
    return reddit.get_subreddit(settings["reddit_subreddit"])
 
def submitContent(subreddit, title, link):
    """Submit a link to a subreddit."""
    logging.info("Submitting %s (%s)", (title, link))
    try:
        subreddit.submit(title, url=link)
    except praw.errors.APIException:
        logging.exception("Error on link submission.")
 
# Main functions
def loadSettings():
    """Load settings from file."""
    try:
        settingsFile = open("settings.json", "r")
    except IOError:
        logging.exception("Error opening settings.json.")
        exitApp()
   
    settingStr = settingsFile.read()
    settingsFile.close()
 
    try:
        settings = json.loads(settingStr)
    except ValueError:
        logging.exception("Error parsing settings.json.")
        exitApp()
   
    # Check integrity
    if (len(settings["reddit_username"]) == 0):
        logging.critical("Reddit username not set.")
        exitApp()
 
    if (len(settings["reddit_password"]) == 0):
        logging.critical("Reddit password not set.")
        exitApp()
 
    if (len(settings["reddit_subreddit"]) == 0):
        logging.critical("Subreddit not set.")
        exitApp()
 
    if (len(settings["reddit_ua"]) == 0):
        logging.critical("Reddit bot user agent not set.")
        exitApp()
 
    if (len(settings["youtube_account"]) == 0):
        logging.critical("YouTube account not set.")
        exitApp()
 
    settings["repost_protection"] = bool(settings["repost_protection"])
 
    # Get last upload position
    try:
        lastUploadFile = open("lastupload.txt", "r")
        lastUpload = lastUploadFile.read()
        lastUploadFile.close()
 
        settings["youtube_lastupload"] = lastUpload
    except IOError:
        logging.info("No last uploaded video found.")
        settings["youtube_lastupload"] = None
 
    return settings

def exitApp():
    sys.exit(1)
 
def runBot():
	# Test commit
	
    """Start a run of the bot."""
    logging.info("Starting bot.")
    settings = loadSettings()
 
    # Get reddit stuff
    logging.info("Logging into Reddit.")
    reddit = getReddit(settings)
    sr = getSubreddit(settings, reddit)
   
    logging.info("Done!")
 
if __name__ == "__main__":
    max_time = int(60)
    start_time = time.time()  # remember when we started
    while (time.time() - start_time) < max_time:
        logging.basicConfig()
 
        try:
            runBot()
        except SystemExit:
            logging.info("Exit called.")
        except:
            logging.exception("Uncaught exception.")
 
    logging.shutdown()