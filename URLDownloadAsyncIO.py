###########################################################################################
# Bruce Rhoades - Concurrency Code Sample - I/O Bound Sample - AsyncIO 
# approach analyzing perfomance for downloading a collection of urls
#
# The upside here is that it is the fastest approach among multithreading and sychronous
#
# Downside here is that it is a bit more complicated and involves extra code for much 
# better performance - but worth it, as it also scales well - no overhead of thred
# management
# 
# Another downside is that special async versions of libraries need to be used. Using their 
# regular versions is slower as they do not notify the event loop 
# ###########################################################################################

import aiohttp
import asyncio
import time


###########################################################################################
# Function to download a web page asynchronously
###########################################################################################
async def downloadSite(session, url):
    async with session.get(url) as response:
        print("Read {0} from {1}".format(response.content_length, url))


###########################################################################################
# Function to download a series of web pages asynchronously
###########################################################################################
async def downloadAllSites(sites):
    # share the session across all tasks as they are running in the same thread
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in sites:
            # create a list of tasks, one for each site 
            # tasks take far fewer resources and less time to create than threads
            # creating and running more of them works well so they scale better than threads
            task = asyncio.ensure_future(downloadSite(session, url))
            tasks.append(task)
        # keep session context alive until all of the tasks have completed; schedule the tasks
        # concurrently - pause here and come back here when gather is ready
        await asyncio.gather(*tasks, return_exceptions=True)



###########################################################################################
# Function to download a series of web pages asynchronously using asyncio
###########################################################################################
def testConcurrency3IOBoundAsyncIO():
    sites = [
        "https://www.jython.org",
        "http://olympus.realpython.org/dice",
    ] * 80
    startTime = time.time()

    # start up the event loop and tell it the tasks to run
    asyncio.run(downloadAllSites(sites))
    time.sleep(3)
    duration = time.time() - startTime
    print(f"\nPERFORMANCE: Downloaded {len(sites)} sites in {duration} seconds")

