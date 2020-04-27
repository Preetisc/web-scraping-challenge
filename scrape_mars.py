from bs4 import BeautifulSoup as bs
import pandas as pd
from splinter import Browser
import requests
import re
from time import sleep

def scrape():
    executable_path = {'executable_path': 'C:/Users/ssjaiswal/Documents/web_drivers/chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    scrape={}

    ################# NASA Mars News ################################

    mars_website_url="https://mars.nasa.gov/news/"
    browser.visit(mars_website_url)
    sleep(10)
    html = browser.html
    soup = bs(html,'html.parser')
    news_title =soup.find('div',class_='list_text').find('div',class_="content_title").text
    #print(news_title)
    news_p =soup.find('div',class_='list_text').find('div',class_='article_teaser_body').text
    #print(news_p)
    scrape["news_title"]=news_title
    scrape["news_p"]=news_p



    ################# NASA Mars News ################################
    ################## JPL Mars Space Images - Featured Image ###########
    jpl_url="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    #jpl_url="https://www.jpl.nasa.gov/"
    browser.visit(jpl_url)
    sleep(5)
    #html_jpl = browser.html
    #soup_jpl = bs(html_jpl,'html.parser')
    #print(soup_jpl)
    browser.click_link_by_partial_text('FULL IMAGE')
    sleep(5)
    browser.click_link_by_partial_text("more info")   
    sleep(5)
    featured_image_url=browser.find_by_xpath("//img[@class='main_image']")._element.get_attribute("src")
    scrape["featured_image_url"]=featured_image_url
    ################## JPL Mars Space Images - Featured Image ###########
    ######################## Mars Weather ##################################

    twe_url="https://twitter.com/marswxreport?lang=en"
    browser.visit(twe_url)
    sleep(10)
    twe_html = browser.html
    soup = bs(twe_html,'html.parser')
    #print(soup)
    all_span=soup.find_all('span',class_='css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0')
    #print(all_span)
    for span in all_span:
        string1=span.text
        if (string1.startswith('InSight sol')):
            scrape["mars_weather"]=string1
            break
            

    #print(mars_weather)
    ######################## Mars Weather ##################################
    ############################# Mars Facts ################################

    mars_facts_url="https://space-facts.com/mars/"
    mars_facts=pd.read_html(mars_facts_url)
    sleep(10)
    mars_facts
    type(mars_facts)
    mars_facts
    df=mars_facts[0]
    df.columns = ['fact','value']
    #df=df.set_index(['fact'])
    df.head()
    #df.count()
    mars_table=df.to_html(index=False)
    scrape["mars_fact_table"]=mars_table



    ############################# Mars Facts ################################
    ######################## Mars Hemispheres ####################################

    mars_hem_url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(mars_hem_url)
    sleep(10)
    #mars_hem_html = browser.html
    #soup_hem =bs(mars_hem_html,'html.parser')

    #div_all =soup_hem.find_all('div',class_='description')
    #print(div_all)

    #hemisphere_image_urls=[]
    i=0
    for i in range(4):
        hem_dic={}
        links=browser.find_by_tag('h3')
        hem_dic["title"]=links[i].text
        links[i].click()
        sleep(3)
        html = browser.html
        soup_hem =bs(html,'html.parser')
        url_hem= soup_hem.find('img',class_='wide-image')['src']

        hem_dic["img_url"]="https://astrogeology.usgs.gov"+ url_hem
        #print(f" hem_dic ${hem_dic}")
        #hemisphere_image_urls.append(hem_dic)
        scrape["hem"+str(i)]=hem_dic
        

    ######################## Mars Hemispheres ####################################
    #print("**************************")
    #print(scrape)
    browser.quit()
    return scrape



