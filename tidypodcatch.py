#!/usr/bin/env python3
"""
tidypodcatch
    A simple Python3 script for archiving podcasts from an rss feed
    https://github.com/pwhitbread/tidypodcatch
"""

import feedparser
import re
import os
import requests
import xml.etree.ElementTree as etree
import sys

# Function to check if the required directory exists, creates otherwises
def ckmkdir(reqpath):
  if not os.path.exists(reqpath):
    os.makedirs(reqpath)
    return 1
  return 0

def main():
    
    # Defaults. Future plan to make customisable on a per feed basis
    fieldsep = " - "
    intdigits = 4
    links_count = 2

    if len(sys.argv) != 2:
        printf("usage: tidypodcatch.py <xml file>")
        sys.exit()
    xmlfile = sys.argv[1]

    # Import XML
    try:
        tree = etree.parse(xmlfile)
        root = tree.getroot()
    except:
        print("Malformed xml file")
        sys.exit()

    i = 0
    for podcastnode in tree.iter("Podcast"):

        i = i + 1
        filefmt = []

        try:
            RSSurl =  podcastnode.find('RSS').text
        except:
            print("Malformed or missing RSS element, block ", i)
            sys.exit()

        try:
            target_path = podcastnode.find('Path').text
        except:
            print("Malformed or missing Path element, block ", i)
            sys.exit()

        atoms = 0
        try:
            fileformatnode = podcastnode.find('FilenameFormat')
            for filenameatom in fileformatnode.iter("atom"):
                atoms = atoms + 1
                filefmt.append(filenameatom.text)
        except:
            print("Malformed or missing Fileformat element, block ", i)
            sys.exit()

        if atoms == 0:
            # No metadata atoms defined, skip feed 
            print("Mising Fileformat atom element(s), block ", i)
            sys.exit()            

        # create target path if it does not exist
        ckmkdir(target_path)

        # Obtain RSS
        NewsFeed = feedparser.parse(RSSurl)
    
        for episode in NewsFeed.entries:
            fn = ""
            for i in range(0,links_count):
                if episode.links[i].href.endswith(".mp3"):
                    episode_url = episode.links[i].href
                    codec = ".mp3"
                elif episode.links[i].href.endswith(".mp3"):
                    episode_url = episode.links[i].href
                    codec = ".m4a"


            for fnatom in filefmt:
                if fn != "":
                    fn = fn + fieldsep
                if (fnatom.lower() == "date"):
                    fn = fn + '{:02}'.format(episode.published_parsed[0]) + "-" + '{:02}'.format(episode.published_parsed[1]) + "-" + '{:02}'.format(episode.published_parsed[2])
                elif episode[fnatom].isdigit():    
                    fn = fn + '{num:0{width}}'.format(num=int(episode[fnatom]), width=int(intdigits))
                else:
                    fn = fn + episode[fnatom]

            fn = fn + codec
            valid_fn = re.sub('[^\w_.)( -]', '', fn)

            print(episode["title"])
            print(fn)
        
            if not os.path.isfile(target_path + "/" + valid_fn):
                print ("download: " + valid_fn)
                r = requests.get(episode_url, allow_redirects=True)
                open(target_path + "/" + valid_fn, 'wb').write(r.content)

                meta_txt = "----------\n"
                for metadata in episode.keys():
                    meta_txt = meta_txt + '{}: {}\n'.format(metadata,episode[metadata])
                open(target_path + "/" + "meta.txt", 'a').write(meta_txt)   


if __name__ == "__main__":
    main()
