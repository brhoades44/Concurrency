###########################################################################################
# Bruce Rhoades - Concurrency Code Sample - I/O Bound Sample - Multiple 
# Threaded approach analyzing perfomance for downloading a collection of urls
#
# # The upside here is that it is faster than the synchronous, single-threaded version
#
# Downside here is that it is a bit more complicated as it involves more code and 
# consideration needs to be given wrt the data that is shared between threads and ensure
# it is thread safe (i.e., multiple threads accessing the data such that it maintains state
# amongst thread usage). Improper use of thread safety on data can result in issues such 
# as race conditions that yield random, intermitten bugs that are difficult to diagnose
# ###########################################################################################

import concurrent.futures
import requests
import threading
import time

# used as access point for threads' session for thread safety
threadLocal = threading.local()
###########################################################################################
# Helper function to create a single session for the thread the first time called
# Retrieve the session for the thread on subsequent calls
###########################################################################################
def getSession():
    if not hasattr(threadLocal, "session"):
        threadLocal.session = requests.Session()
    return threadLocal.session 


###########################################################################################
# Function to download a web page using multithreading
###########################################################################################
def downloadSite(url):
    # get the session for the thread
    session = getSession()
    # using get from Sessions instead of from requests directly to speed things up
    with session.get(url) as response:
        print(f"Read {len(response.content)} from {url}")


###########################################################################################
# Function to download a series of web pages using multithreading
###########################################################################################
def downloadAllSites(sites):
    # Create a pool of concurrent threads and use an Executor to control 
    # how and when each of the threads in the pool will run to download
    # each of the sites in the list
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(downloadSite, sites)


###########################################################################################
# Function to download a series of web pages using multithreading
###########################################################################################
def testConcurrency2IOBoundThreaded():
    sites = [
        "https://www.jython.org",
        "http://olympus.realpython.org/dice",
    ] * 80

    startTime = time.time()
    downloadAllSites(sites)
    duration = time.time() - startTime
    print(f"\nPERFORMANCE: Downloaded {len(sites)} in {duration} seconds")
