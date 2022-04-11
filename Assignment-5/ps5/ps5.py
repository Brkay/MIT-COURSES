# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name: Berkay Yaldız
# Collaborators:
# Time:

from os import link, remove

from pandas import describe_option
import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime, tzinfo
import pytz


# -----------------------------------------------------------------------

# ======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
# ======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

# ======================
# Data structure design
# ======================

# Problem 1

# TODO: NewsStory


class NewsStory(object):
    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate

    def get_guid(self):
        return self.guid

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_link(self):
        return self.link

    def get_pubdate(self):
        return self.pubdate


# ======================
# Triggers
# ======================


class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
# TODO: PhraseTrigger


class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        self.phrase = phrase

    # def evaluate(self, trigger):
      #  return self.is_phrase_in(trigger)

    def is_phrase_in(self, argument):
        replaced_letters = string.punctuation
        temp_string = self.phrase.lower()
        for letter in replaced_letters:
            temp_string = temp_string.replace(letter, ' ')

        list_phrase = list(temp_string.split())
        list_argument = list(argument.split())
        if list_argument[0] in list_phrase:
            first_index = list_phrase.index(list_argument[0])
            i = 0
            for index in range(first_index, len(list_argument)+first_index):
                if len(list_phrase)-1 < index:
                    return False
                else:
                    if list_phrase[index] != list_argument[i]:
                        return False
                    i += 1
            return True
        else:
            return False


# Problem 3
# TODO: TitleTrigger
class TitleTrigger(PhraseTrigger):
    def __init__(self, trigger):
        self.trigger = trigger

    def evaluate(self, News_object):
        self.phrase = News_object.get_title()
        return self.is_phrase_in(self.trigger.lower())


# Problem 4
# TODO: DescriptionTrigger
class DescriptionTrigger(PhraseTrigger):
    def __init__(self, trigger):
        self.trigger = trigger

    def evaluate(self, News_object):
        self.phrase = News_object.get_description()
        return self.is_phrase_in(self.trigger.lower())


# TIME TRIGGERS

# Problem 5
# TODO: TimeTrigger
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.
class TimeTrigger(Trigger):
    def __init__(self, date):
        self.time = datetime.strptime(date, "%d %b %Y %H:%M:%S")


# Problem 6
# TODO: BeforeTrigger and AfterTrigger
class BeforeTrigger(TimeTrigger):
    def __init__(self, date):
        TimeTrigger.__init__(self, date)

    def evaluate(self, News_object):
        if News_object.get_pubdate().tzinfo == None:
            return News_object.get_pubdate() < self.time
        else:
            self.time = self.time.replace(tzinfo=pytz.timezone(
                News_object.get_pubdate().tzinfo._tzname))
            return News_object.get_pubdate() < self.time


class AfterTrigger(TimeTrigger):
    def __init__(self, date):
        TimeTrigger.__init__(self, date)

    def evaluate(self, News_object):
        if News_object.get_pubdate().tzinfo == None:
            return News_object.get_pubdate() > self.time
        else:
            self.time = self.time.replace(tzinfo=pytz.timezone(
                News_object.get_pubdate().tzinfo._tzname))
            return News_object.get_pubdate() > self.time


# COMPOSITE TRIGGERS

# Problem 7
# TODO: NotTrigger
class NotTrigger(TitleTrigger):
    def __init__(self, Trigger_object):
        self.Trigger_object = Trigger_object

    def evaluate(self, News_object):
        return not self.Trigger_object.evaluate(News_object)


# Problem 8
# TODO: AndTrigger
class AndTrigger(TitleTrigger):
    def __init__(self, Trigger_object1, Trigger_object2):
        self.Trigger_object1 = Trigger_object1
        self.Trigger_object2 = Trigger_object2

    def evaluate(self, News_object):
        boolean1 = self.Trigger_object1.evaluate(News_object)
        boolean2 = self.Trigger_object2.evaluate(News_object)
        return boolean1 and boolean2
# Problem 9
# TODO: OrTrigger


class OrTrigger(TitleTrigger):
    def __init__(self, Trigger_object1, Trigger_object2):
        self.Trigger_object1 = Trigger_object1
        self.Trigger_object2 = Trigger_object2

    def evaluate(self, News_object):
        boolean1 = self.Trigger_object1.evaluate(News_object)
        boolean2 = self.Trigger_object2.evaluate(News_object)
        return boolean1 or boolean2

# ======================
# Filtering
# ======================

# Problem 10


def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    returned_stories = []
    for news in stories:
        for triggers in triggerlist:
            if triggers.evaluate(news):
                returned_stories.append(news)

    return returned_stories


# ======================
# User-Specified Triggers
# ======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers
    trigger_names = {}
    returned_list = []
    for list_element in lines:
        temp = list_element.split(',')
        if temp[0] == "ADD":
            for keys in trigger_names:
                returned_list.append(trigger_names[keys])
        else:
            if temp[1] == "TITLE":
                trigger_names[temp[0]] = TitleTrigger(temp[2])
            elif temp[1] == "DESCRIPTION":
                trigger_names[temp[0]] = DescriptionTrigger(temp[2])
            elif temp[1] == "AFTER":
                trigger_names[temp[0]] = AfterTrigger(temp[2])
            elif temp[1] == "BEFORE":
                trigger_names[temp[0]] = BeforeTrigger(temp[2])
            elif temp[1] == "NOT":
                trigger_names[temp[0]] = NotTrigger(trigger_names[temp[2]])
            elif temp[1] == "AND":
                trigger_names[temp[0]] = AndTrigger(
                    trigger_names[temp[2]], trigger_names[temp[3]])
            else:
                trigger_names[temp[0]] = TitleTrigger(
                    trigger_names[temp[2]], trigger_names[temp[3]])
    return returned_list


SLEEPTIME = 120  # seconds -- how often we poll


def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("Ukraine")
        t2 = DescriptionTrigger("Russia")
        t3 = DescriptionTrigger("War")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line
        triggerlist = read_trigger_config('triggers.txt')

        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT, fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica", 14),
                    yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []

        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(
                    END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(
                    END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            # stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)

            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()
