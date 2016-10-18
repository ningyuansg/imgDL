import requests
import bs4
import os

# gets URL from input
def getURL():
    url = input("Enter URL here >>>")
    return url

# gets soup object from url
def getSoup(url):
    html = requests.get(url)
    print("Retrieving .html..."),
    soup = bs4.BeautifulSoup(html.text, 'html.parser')
    print("Parsing soup object..."),
    return soup

# universal retrieval
def allGet(url, soup):
    print("Switching to universal mode..."),
    imgtags = soup.select('img')
    print("Building image URLs...")
    imgsrc = []
    for tag in imgtags:
        if '.svg' not in tag.get('src'):
            if 'http' in tag.get('src'):
                src = tag.get('src')
            else:
                src = 'http:' + tag.get('src')
            imgsrc.append(src)
    return imgsrc

# retrieves imgsrc list of img URLS for 4chan
def chanGet(url, soup):
    print("Switching to 4chan mode..."),
    fileText = soup.select('div .fileText a')
    print("Building image URLs..."),
    imgsrc = []
    for tag in fileText:
        src = 'http:' + tag.get('href')
        imgsrc.append(src)
    return imgsrc

# TODO sanitises file names for OS module

# iterates over list to download images
def download(imgsrc):
    print("Starting downloads...")
    dlcount = 1
    for imgurl in imgsrc:
        print("Downloading", str(dlcount), "of", str(len(imgsrc)))
        imgdata = requests.get(imgurl)
        # TODO catch errors with invalid file names
        filename = imgurl[imgurl.rfind('/') + 1:]
        imgfile = open(filename, 'wb')
        for chunk in imgdata.iter_content(10000):
            imgfile.write(chunk)
        imgfile.close()
        dlcount += 1
    print("All downloads complete!")

# TODO make a downloadAll function for ease of use when importing this module
if __name__ == '__main__':
    url = getURL()
    soup = getSoup(url)
    if '4chan' in url:
        imgsrc = chanGet(url, soup)
    else:
        imgsrc = allGet(url, soup)
    download(imgsrc)
    input("Press enter to exit.")
