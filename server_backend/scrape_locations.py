from pattern.web import download
from pymongo import MongoClient
import re, time

def get_attractions_from_page(url, city, client):

    while True:
        try:
            html = download(url)
        except:
            print "Error Getting Attractions from page"
            time.sleep(.5)
            continue
        break

    properties = html.split("property_title\">")

    for index in range(1, len(properties)):
        attraction = get_attraction(properties[index])
        attraction['categories'] = get_attraction_details(attraction["url"], attraction["name"])

        if(len(attraction['categories']) > 0):
            client.insert({"city":city, "name":attraction["name"], "_id":attraction["url"], "review_count":attraction["review_count"], "categories":attraction["categories"]})
        else:
            print "Error on: " + attraction["name"]

def get_attraction(prop):
    # define attraction container
    attraction = dict()

    # get first tag
    first_tag = prop.split("<")[1]

    # get the attraction_name
    attraction_name = first_tag.split(">")[1]

    try:
        review_count = get_review_count(prop.split("#REVIEWS\">")[1])
    except:
        review_count = 0

    # get attraction url
    attraction_url = first_tag.split("href=")[1].split("\"")[1]

    # put the data into attraction
    attraction["name"] = attraction_name
    attraction["url"] = "http://www.tripadvisor.com" + attraction_url
    attraction["review_count"] = review_count

    return attraction

def get_attraction_details(attraction_url, attraction_name):
    while True:
        try:
            html = download(attraction_url)
        except:
            print "Error getting attraction details"
            time.sleep(.5)
            continue
        break

    # get the descriptions of the location in the ugliest line of code I've ever written
    try:
        detailsplit = html.split("div class=\"detail\">")
        split_loc = 1 if "Neighborhood:" not in detailsplit[1] or len(detailsplit)==2 else 2
        details = detailsplit[split_loc].split("</div>")[0]
    except IndexError:
        return []

    # split up the details into categories
    list_details = []

    jank_details = details.split(", ")

    # I'm not really sure what I'm doing here but it works
    for jank in jank_details:
        split = jank.split("<")

        if(len(split) > 1):
            title = split[1]

            title_split = title.split(">")

            if(len(title_split) > 1):
                clean_title = title_split[1]

                list_details.append(clean_title)

    return list_details

def get_review_count(reviews):
    review_count = reviews.lower().split(" review")[0]
    review_count_clean = re.sub("[^0-9]", "", review_count)
    return int(review_count_clean)

def get_all_pages(url):
    while True:
        try:
            html = download(url)
        except:
            time.sleep(.5)
            print "Error getting all the pages"
            continue
        break

    # get the page numbers element
    pageNumbers = html.split("class=\"pageNumbers\">")[1]
    pageNumbers = pageNumbers.split("</div>")[0]

    # get a list of all the pages
    pages = pageNumbers.split("<")[2:]
    
    min_page = get_num(clean_href(pages[1]))
    max_page = get_num(clean_href(pages[len(pages)-2]))
    url_parts = get_base_url(clean_href(pages[1]))

    urls = []

    for number in range(min_page, 90+30, 30):
        urls.append(url_parts[0] + str(number) + url_parts[1])

    return urls

def clean_href(tag):
    return tag.split("href=")[1].split("\"")[1]

def get_num(page):
    return int(page.split("oa")[1].split("-")[0])

def get_base_url(page):
    parts = page.split("oa")
    first_part = "http://www.tripadvisor.com" + parts[0] + "oa"
    second_part = "-" + parts[1].split("-")[1]

    return [first_part, second_part]


f = open("city_urls.txt", "r")
cities = f.readlines()

client = MongoClient()
points = client.wombats.points

for index in range(0, len(cities)):
    info = cities[index].split("*****")

    print "Working on... " + info[0] + " (" + str(index+1) + " of " + str(len(cities)) + ")"

    pages = get_all_pages(info[1])

    for page in pages:
        get_attractions_from_page(page, info[0], points)

    print "Completed " + str(index+1) + " of " + str(len(cities))

