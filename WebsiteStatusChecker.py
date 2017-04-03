import requests
from sendEmail import send_email
from bs4 import BeautifulSoup 

def readLines():
    """Reads in lines from urls.txt, gives the status and other information on them"""
    with open("urls.txt", "r") as f:
        urls = f.readlines()

    # cleans up the strings
    urls = [url.replace("\n", "") for url in urls]
    urls = [url.replace(" ", "") for url in urls]

    writeLines(urls)

def writeLines(urls):
    # composes the status string, writes to a file
    with open("statuses.txt", "a") as f:
        f.seek(0)
        f.truncate()
        for i in range(len(urls)):
            statusString = str(i) + " || " + urls[i] + "\n"
            statusString += "\tStatus: " + str(checkStatus(urls[i]))
            print(statusString)
            f.write(statusString + "\n\n")

def checkStatus(url):
    """Checks the status of the url--what the status number is, and whether it is an Index Of page
        If there is an error--the website doens't load, for example, return that error
    """
    def checkForIndexPage(r):
        """Checks whether it a given url is actually an Index Of page. Takes in a Request object"""
        soup = BeautifulSoup(r.text, 'lxml')
        head = soup.find('h1')
        if head != None and head.string != None and ("Index of " in head.string):
            return "Shows 'Index Of' page ✘" 
        else:
            return "Displays properly ✓"

    returnString = ""
    try:
        r = requests.get(url)
        returnString +=  str(r.status_code) 
        if r.status_code == 200: # if the page is accessible, then check whether it displays properly
            returnString += "\n\t" + checkForIndexPage(r)
        return returnString
    except Exception as e:
        return(e)




# only runs if the module is called directly, not when it is imported. When it is imported, the user can call functions themselves
if __name__ == "__main__":
    readLines()    