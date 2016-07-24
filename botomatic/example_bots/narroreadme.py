import urllib
import urllib2
import json
import re
import sys

from botomatic import TBot

class NarroReadMe(TBot):
    debug_mode = False

    def __init__(self):
        handle = "narroreadme"
        self.query = "read this article"
        super(NarroReadMe, self).__init__(handle)


    def run(self):
        # find other people's reading recommendations on twitter and reply
        count = 0
        for tweet in self.search("read this article"):
            if tweet.lang != 'en': # english only, for now
                continue 

            if tweet.entities["urls"]:
                url = tweet.entities["urls"][0]["expanded_url"]
                if ("fb.me" not in url) & ("twitter.com" not in url):
                    self.reply_with_readme(tweet.id, url, tweet.user.screen_name)
                    count += 1
                else:
                    print "Avoiding facebook/twitter status"
            else:
                print "No urls present in tweet"
        
        print "%i replies" % (count)
        self.wrap_up()

    def reply_with_readme(self, id, url, name):
        narro_url = "https://www.narro.co/add?url=" + url
        reply = "@%s You can listen to that article on @narroapp here: %s" % (name, narro_url)
        print reply
        self.tweets.append(id, reply)

if __name__ == '__main__':
    r = NarroReadMe()
