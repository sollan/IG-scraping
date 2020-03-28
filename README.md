# IG Scraping

Instagram scraping tool

Configure: path to chromedriver (or other web driver), IG account to scrape, your IG account, and password.

Right now, ReadPage collects the links to all the posts of a given user and saves them in a csv file (links.csv). Because it involves scrolling to bottom (to get all posts), you need to use your own account and password for auto-login. 

ParseLinks reads the links from this csv and parses the post information, and saves the info in another csv file (results.csv). If there are many posts involved, ParseLinks is set to save the working data at an interval so that the progress isn't lost, e.g. due to memory. (should be improved to save file, release memory, and start new file.)

information saved:

posting date, caption, hashtags involved in caption and OP comments, number of likes, and number of comments

The use of this should comply with GDPR :) Ask for consent before you save their data.
