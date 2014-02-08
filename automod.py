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
 
# Main functions
def loadSettings():
    """Load settings from file."""
    try:
        settingsFile = open(sys.argv[1], "r")
    except IOError:
        logging.exception("Error opening settings.")
        exitApp()
   
    settingStr = settingsFile.read()
    settingsFile.close()
 
    try:
        settings = json.loads(settingStr)
    except ValueError:
        logging.exception("Error parsing settings.")
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
 
    settings["repost_protection"] = bool(settings["repost_protection"])
 
    return settings
 
def wordInFile(word, file):
    for line in file:
        if(line.find(word)>=0):
            return True
    return False
	
def monitorActivity(sr):
    data = sr.get_new(limit=1)
    post = data.next()
    myfile = "Tester.txt"
    for post in posts:
        if len(post.comments)==0 and post.url not in myfile:
            #add url to list
            if len(list) > 0:
                if time.time() - post.created > -28740 and post.num_comments==0:
                    sr.send_message("A thread without a comment", "The following thread has had no comments, and it has been a day since it was posted: " + post.url)
                    with open("Tester.txt", "a") as myfile:
                        myfile.write("/n" + post.url)
                        myfile.close()
 
def exitApp():
    sys.exit(1)
 
def runBot():       
    """Start a run of the bot."""
    logging.info("Starting bot.")
    settings = loadSettings()
 
    # Get reddit stuff
    logging.info("Logging into Reddit.")
    reddit = getReddit(settings)
    sr = getSubreddit(settings, reddit)
    wordInFile()
    monitorActivity(sr)
   
    logging.info("Done!")
 
if __name__ == "__main__": 
    if len(sys.argv) > 1:
        print str(sys.argv)
        try:
            runBot()
        except IOError:
            logging.info("Environment Settings file not found.")
        except SystemExit:
            logging.info("Exit called.")
        except:
            logging.exception("Uncaught exception.")              
    else:
        logging.info("Environment not defined.")
    logging.shutdown()
