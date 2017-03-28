from polls.storageData import storageData

import requests
import bs4
from selenium import webdriver
import time

class crawlData:
    def __init__(self,url):
        self.url = url
    @classmethod
    def getInfoUrl(cls,url):
        listNav = []
        urlLink = requests.get(url)
        soup = bs4.BeautifulSoup(urlLink.content)
        nav = soup.nav
        for item in nav.find_all('a'):
            listNav.append(item.get('href'))
        return listNav

class crawlSpecificCss(crawlData):
    def __init__(self):
        pass
    @classmethod
    def getInfoUrl(cls,url):
        listNav = []
        urlLink = requests.get(url)
        soup = bs4.BeautifulSoup(urlLink.content)
        for item in soup.find_all('h3'):
            listNav.append(item.text)
        return listNav
    @classmethod
    def getLinkWithSelenium(cls,url,cssSelector,className):
        listComment = []
        br = webdriver.Firefox(executable_path=r'C:\Users\DELL\Downloads\geckodriver-v0.15.0-win64 (1)\geckodriver.exe')
        br.get(url)
        cssClick = br.find_element_by_css_selector(css_selector=cssSelector)
        soup = bs4.BeautifulSoup(cssClick.get_attribute('innerHTML'))
        for item in soup.find_all('div',{'class': className}):
            try:

                catgorizeComment = item.find_all('p',{'class':'_2xg6Ul'})[0].text
                comment = item.find_all('div',{'class':'qwjRop'})[0].text
                #print(item.find_all('p',{'class':'_2xg6Ul'})[0].text)
                #print(item.find_all('div',{'class':'qwjRop'})[0].text)
                listComment.append(
                    storageData.jsonData(
                        catgorizeComment = catgorizeComment,
                        comment = comment
                    )
                )
            except:
                pass
        return listComment

class crawlSpecific(crawlData):
    def __init__(self):
        pass
    @classmethod
    def getInfoUrl(cls,url,typeCss,classNameKey,classNameValue):
        listNav = []
        urlLink = requests.get(url)
        soup = bs4.BeautifulSoup(urlLink.content)
        for item in soup.find_all(typeCss,{classNameKey:classNameValue}):
            listNav.append(
                {
                    'name':item.contents[0].text,
                    'address':item.find_all('p')[0].text
                }
            )

        return listNav