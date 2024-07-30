import bs4 as bs
import urllib
import urllib.request
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

web=input("Enter url of the website:")
url = urllib.request.urlopen(web)
html = url.read()
soup = bs.BeautifulSoup(html, 'lxml')

#ON-PAGE CHECKLIST

# 1. Check page title
title= soup.title.text
def check_page_title(title):
    if len(title) > 70:
        return "Page title is too long"
    elif len(title) < 10:
        return "Page title is too short"
    else:
        return "Page title is optimized"

# 2. Check meta description
description = soup.find('meta', attrs={'name': 'description'})
def check_meta_description(description):
    if len(description) > 160:
        return "Meta description is too long"
    elif len(description) < 50:
        return "Meta description is too short"
    else:
        return "Meta description is optimized"

# 3. Check URL structure
url = web
def check_url_structure(url):
    if url.count('//') > 3:
        return "URL structure is not optimal"
    else:
        return "URL structure is optimized"
        
# 4. Check page Heading
headings = soup.find_all(['h1', 'h2', 'h3'])
def check_heading_tags(headings):
    if len(headings) == 0:
        return "No heading tags found."
    for heading in headings:
        if not heading.text.strip():
            return "Heading tag without text content found."
    return "Heading is optimized."  

# 5. Check alt tag 
images = soup.find_all('img')
def check_alt_attribute(images):
    if len(images) == 0:
        return "No image tags found."   
    for image in images:
        if not image.has_attr('alt') or not image['alt'].strip():
            return "Image tag without alt attribute or empty alt attribute found."
    return "Alt attribute in image is optimized."
print(check_page_title(title))
print(check_meta_description(description))
print(check_url_structure(url))
print(check_heading_tags(headings))
print(check_alt_attribute(images))

#TECHNICAL CHECKLIST

response = requests.get(url)
robots_url = url + "/robots.txt"
response1 = requests.get(robots_url)
soup = BeautifulSoup(response.content, 'html.parser')
headers = {
            'User-Agent': 'Mozilla/5.0 \
            (Windows NT 10.0; Win64; x64)\
            AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/58.0.3029.110 Safari/537.3'
        }
response2 = requests.get(url, headers=headers)
# 1. Check crawlable
def check_crawlability(url):
    if response.status_code == 200:
        print("Website is crawlable")
    else:
        print("Website is not crawlable")

# 2. Check xml sitemap	
def check_xml_sitemap(url):
    if response.status_code == 200:
        content_type = response.headers.get('Content-Type')
        if 'xml' in content_type:
            xml_data = response.text
            root = ET.fromstring(xml_data)
            if root.tag == 'urlset':
                print("XML sitemap is present and valid")
            else:
                print("XML sitemap is present but not valid")
        else:
            print("URL does not point to an XML sitemap")
    else:
        print("Failed to retrieve the URL:", response.status_code)

# 3. Check https			
def check_https(url):
    if response.status_code == 200 and response.url.startswith("https://"):
        print("URL is using HTTPS")
    else:
        print("URL is not using HTTPS")

# 4. check errors
def check_404_errors(url):
    if response.status_code == 404:
        print("URL has 404 errors")
    else:
        print("URL does not have 404 errors")
 
# 5. Check mobile-friendly 
def check_mobile_friendly(url):
    if 'mobile' in response2.headers.get('X-Wap-Profile', '').lower() or \
            'mobile' in response2.headers.get('Profile', '').lower() or \
            '<meta name="viewport" content="width=device-width' in response2.text.lower():
        print("URL has a mobile-friendly design")
    else:
        print("URL does not have a mobile-friendly design")
check_crawlability(url)
check_xml_sitemap(url)
check_https(url)
check_404_errors(url)
check_mobile_friendly(url)


# OFF-PAGE

# Check backlinks
def check_backlinks(url):
    count = 0
    if response.status_code == 200:
    
        soup = BeautifulSoup(response.text, 'html.parser')

    
        backlinks = soup.find_all('a', href=True)

   
        for link in backlinks:
            #print(link['href'])
            count = count + 1
        #print(count)
        if count > 5:
            print("Backlink is optimized.")
        else:
            print("Backlink is not optimized.")
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
    
check_backlinks(url)