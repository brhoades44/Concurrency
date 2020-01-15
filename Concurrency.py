###########################################################################################
# Bruce Rhoades - Concurrency Code Samples - Synchronous (single threaded) Multi-Threaded, 
# AsyncIO and Multi-Process Approaches Examined
###########################################################################################

###########################################################################################
# The first step of this process is deciding if you should use a concurrency module. 
# Concurrency always comes with extra complexity and can often result in bugs that are 
# difficult to diagnose.
#
# It is recommended to hold out on adding concurrency until you have a known performance 
# issue and then determine which type of concurrency you need. Premature optimization is 
# the root of all evil (or at least most of it) in programming.”
###########################################################################################


###########################################################################################
# Once you’ve decided that you should optimize your program, figuring out if your program 
# is CPU-bound or I/O-bound is a great next step. 
#
# CPU-bound problems only really gain from using multiprocessing. Threading and asyncio 
# does not help this type of problem at all as the overhead involved in implementing
# these solutions just adds to the performance bottleneck. Multiprocessing allows to 
# make use of the processing power of modern computers by utiliting multiple CPUs.
#
# For I/O-bound problems, the general rule of thumb is to use asyncio when you can.
# Asyncio can provide the best speed for this type of program, but sometimes critical 
# libraries will be required that have not been ported to take advantage of asyncio. 
# In these instances, threading can be a better choice. The CPU idle time during I/O 
# can be used to process other threads/tasks therefore increasing performance
# 
# Multiprocessing does not help for these types of issues as the overhead of managing 
# the multiple processes adds to the idle time related to the I/O. 
###########################################################################################

###########################################################################################
# Concurrency makes a big difference for two types of problems: Those that are CPU-bound
# and those that are I/O bound. I/O bound issues slow programs down because it must wait
# for I/O from an external resource. I.e., when programs work with things slower than the 
# CPU (i.e., file system and network connections). 
# CPU-bound problems are those that spend most of their time doing CPU operations and not
# dealing with these external resources
###########################################################################################


###########################################################################################
# With multiprocessing, Python creates new processes. A process here can be thought of as 
# almost a completely different program, though technically they’re usually defined as a 
# collection of resources where the resources include memory, file handles and things like 
# that. One way to think about it is that each process runs in its own Python interpreter.
###########################################################################################

###########################################################################################
# 3 Concurrency types: 
#
# 1.) Pre-emptive multitasking (threading) - The operating system decides when to switch 
#     tasks external to Python. Number of Processors: 1
#
# 2.) Cooperative multitasking (asyncio) - The tasks decide when to give up control. 
#     Numer of Processors: 1
#
# 3.) Multiprocessing (multiprocessing) - The processes all run at the same time on 
#     different processors. Numer of Processors: Many
###########################################################################################

import multiprocessing
import requests
import time

import URLDownloadAsyncIO
import URLDownloadMultiThreaded
import URLDownloadSynchronous

session = None
def setGlobalSession():
    global session
    if not session:
        session = requests.Session()

def downloadSite(url):
    with session.get(url) as response:
        name = multiprocessing.current_process().name
        print(f"{name}:Read {len(response.content)} from {url}")

###########################################################################################
# Function to download a series of web pages using multiprocessing
###########################################################################################
def downloadAllSites(sites):
    # Create a number of separate Python interpreter processes and have each one 
    # run downloadSiteMultiProcessing on some of the items in sites
    # Pool matches the # of CPUs on the computer with the # of processes it creates
    # #of processes in an optional parameter
    # having too many processes can slow things down as setting them up and breaking them
    # down is an expensive operation
    # create a session for each process not each time 
    with multiprocessing.Pool(initializer=setGlobalSession) as pool:
        pool.map(downloadSite, sites)


###########################################################################################
# Function to download a series of web pages asynchronously using Multiprocessing
# It does this by creating a new instance of the Python interpreter to run on each CPU and 
# then farming out part of your program to run on it.
#
# Upside to this approach is that it is relatively easy to set up and requires little 
# extra code and takes full advantage of a computer's CPU power
#
# Downside is some extra code, the global Session object, plus it is slower than 
# the threading and asyncio approaches. MultiProcessing is not really tailored for 
# these I/O bound problems. 
############################################################################################
def testConcurrency4IOBoundMultiProcessing():
    if __name__ == "__main__":
        sites = [
            "https://www.jython.org",
            "http://olympus.realpython.org/dice",
        ] * 80
        startTime = time.time()
        downloadAllSites(sites)
        duration = time.time() - startTime
        print(f"\nPERFORMANCE: Downloaded {len(sites)} in {duration} seconds")


###########################################################################################
# Function to return sum of squares
###########################################################################################
def sumOfSquares(number):
    return sum(i * i for i in range(number))

###########################################################################################
# Function to accept a list of numbers and then compute the sum of square for each item 
# in the list
###########################################################################################
def findSums(numbers):
    for number in numbers:
        sumOfSquares(number)

###########################################################################################
# Same logic but with the addition of using multiprocessing
###########################################################################################
def findSumsMultiProcessing(numbers):
    with multiprocessing.Pool() as pool:
        pool.map(sumOfSquares, numbers)

###########################################################################################
# Function to test a lenthy CPU intensive operation to determine performance 
#
# Param: multiProcessing - when False, operation done synchronously on one processor
#                          when True, operation done via multiProcessing
#
# Upside of multiprocessing is that it is faster and easier to set up in this case
# Communication between processes also adds complexity that a sychronous, non-current
# program would not need to deal with 
###########################################################################################
def testConcurrency5CPUBoundSynchronous(multiProcessing=False):
    if __name__ == "__main__":
        numbers = [3_000_000 + x for x in range(20)]

        startTime = time.time()
        if(multiProcessing == True):
            findSumsMultiProcessing(numbers)
        else:
            findSums(numbers)

        duration = time.time() - startTime
        print(f"\nPERFORMANCE: Duration {duration} seconds")

###########################################################################################
# Function to test a lenthy CPU intensive operation done via MultiProcessing to determine 
# performance 
#
# Implementing a CPU Bound problem like this via Threads and AsyncIO will SLOW DOWN the 
# operation because both threads and tasks run on the same CPU in the same process, as 
# well as the work of the non-concurrent threads performing the CPU intensive operation.
# All this overhead in addition to the lenthy operation causes it to be slower than the 
# synchronous, single threaded solution!
###########################################################################################
def testConcurrency6CPUBoundSMultiProcessing():
    testConcurrency5CPUBoundSynchronous(True)


###########################################################################################
# Function to query a process selection from the user until a valid response is given
###########################################################################################
def getProcessSelection():
    processSelection = ''
    while (processSelection != 'q'):
        print("""\n        1.) I/O Bound Problem: Download Multiple URLs - Synchronous Approach
        2.) I/O Bound Problem: Download Multiple URLs - Multithreaded Approach
        3.) I/O Bound Problem: Download Multiple URLs - AsyncIO Approach
        4.) I/O Bound Problem: Download Multiple URLs - Multiprocess Approach
        5.) CPU Bound Problem: CPU Intensive Operation- Synchronous Approach
        6.) CPU Bound Problem: CPU Intensive Operation- Multiprocess Approach""")
        processSelection = input("\nPlease make a selection from the above choices. Please Enter a Value Between 1 and 6 (or q to quit): ")
        if(processSelection not in ['1', '2', '3', '4', '5', '6']):
            if(processSelection != 'q'):
                print("\nINVALID SELECTION!\n")
            continue
        else:
            break

    return processSelection

def intro():
    print("""    This application is intended to diagnose a variety of approaches to solving 2 types of problems that can potentially
    be solved efficiently through the implementation of a type of concurrency solution. These types of problems are those that are
    I/O Bound and those that are CPU Bound. 4 Approaches are suggested for a particular I/O bound problem involving downloading of
    URLs: Synchronous (Single Threaded), MultiThreaded, AsyncIO and MultiProcess. 2 Approaches are suggested for a particular CPU
    Bound problem involving lengthy operations of summing squares: Synchronous (Single Threaded) and MultiProcess. MultiThreaded
    and AsyncIO are discouraged for these types of problems as their performance is worse than Synchronous (Single Threaded) since 
    there is extra CPU overhead to managing threads and tasks in addition to the intense CPU operations involved in the problem. \n
    Note that MultiProcess approach is also discouraged for I/O Bound problems as the overhead of managing processes adds to 
    the overhead of the I/O Operation rendering it less performant than AsyncIO and Multithreaded Solutions. 

    Enter q at any time to quit. Cheers!\n""")

###########################################################################################
# Main
###########################################################################################
if(__name__ == "__main__"):
    intro()
    processSelection = ''
    while(processSelection != 'q'):
        processSelection = getProcessSelection()
        if(processSelection != 'q'):
            if(processSelection == '1'):
                URLDownloadSynchronous.testConcurrency1IOBoundSynchronous()
            elif(processSelection == '2'):
                URLDownloadMultiThreaded.testConcurrency2IOBoundThreaded()
            elif(processSelection == '3'):
                URLDownloadAsyncIO.testConcurrency3IOBoundAsyncIO()
            elif(processSelection == '4'):
                testConcurrency4IOBoundMultiProcessing()
            elif(processSelection == '5'):
                print("Performing lengthy CPU operation...")
                testConcurrency5CPUBoundSynchronous()
            else:
                print("Performing lengthy CPU operation...")
                testConcurrency6CPUBoundSMultiProcessing()
