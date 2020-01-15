###########################################################################################
# Bruce Rhoades - Concurrency Code Sample - I/O Bound Sample - Sychronous, Single 
# Threaded approach analyzing perfomance for downloading a collection of urls
#
# The upside to this approach is that it is easy, straightforward and therefore the 
# easiest to maintain (i.e., easiest for other people who work on your code long after you
# are gone to understand :) )
#
# The downside is that it is slow compared to solutions using concurrency
###########################################################################################

import requests
import time

###########################################################################################
# Function to download a web page
###########################################################################################
def downloadSite(url, session):
    # using get from Sessions instead of from requests directly to speed things up
    with session.get(url) as response:
        print(f"Read {len(response.content)} from {url}")


###########################################################################################
# Function to download a series of web pages
###########################################################################################
def downloadAllSites(sites):
    with requests.Session() as session:
        for url in sites:
            downloadSite(url, session)


###########################################################################################
# Function to download web pages in a single threaded, synchronous fashion
#
###########################################################################################
def testConcurrency1IOBoundSynchronous():
    sites = [
        "https://www.jython.org",
        "http://olympus.realpython.org/dice",
    ] * 80

    startTime = time.time()
    downloadAllSites(sites)
    duration = time.time() - startTime
    print(f"\nPERFORMANCE: Downloaded {len(sites)} in {duration} seconds")