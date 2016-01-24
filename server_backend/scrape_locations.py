from pattern.web import download
from pymongo import MongoClient
import re, time

class db_setup():

    def __init__(self):
        self.city_info = [
        "Charleston*****http://www.tripadvisor.com/Attractions-g54171-Activities-Charleston_South_Carolina.html",
        "Las Vegas*****http://www.tripadvisor.com/Attractions-g45963-Activities-Las_Vegas_Nevada.html",
        "Seattle*****http://www.tripadvisor.com/Attractions-g60878-Activities-Seattle_Washington.html",
        "San Francisco*****http://www.tripadvisor.com/Attractions-g60713-Activities-San_Francisco_California.html",
        "Washington D.C.*****http://www.tripadvisor.com/Attractions-g28970-Activities-Washington_DC_District_of_Columbia.html",
        "New Orleans*****http://www.tripadvisor.com/Attractions-g60864-Activities-New_Orleans_Louisiana.html",
        "St. Louis*****http://www.tripadvisor.com/Attractions-g44881-Activities-Saint_Louis_Missouri.html",
        "Sedona*****http://www.tripadvisor.com/Attractions-g31352-Activities-Sedona_Arizona.html",
        "Los Angeles*****http://www.tripadvisor.com/Attractions-g32655-Activities-Los_Angeles_California.html",
        "Philadelphia*****http://www.tripadvisor.com/Attractions-g60795-Activities-Philadelphia_Pennsylvania.html",
        "Phoenix*****http://www.tripadvisor.com/Attractions-g31310-Activities-Phoenix_Arizona.html",
        "Denver*****http://www.tripadvisor.com/Attractions-g33388-Activities-Denver_Colorado.html",
        "Salt Lake City*****http://www.tripadvisor.com/Attractions-g60922-Activities-Salt_Lake_City_Utah.html",
        "Grand Canyon*****http://www.tripadvisor.com/Attractions-g143028-Activities-Grand_Canyon_National_Park_Arizona.html",
        "Yosemite*****http://www.tripadvisor.com/Attractions-g61000-Activities-Yosemite_National_Park_California.html",
        "Orlando*****http://www.tripadvisor.com/Attractions-g34515-Activities-Orlando_Florida.html",
        "New York City*****http://www.tripadvisor.com/Attractions-g60763-Activities-New_York_City_New_York.html",
        "Chicago*****http://www.tripadvisor.com/Attractions-g35805-Activities-Chicago_Illinois.html"]

    def get_review_count(self, reviews):
        review_count = reviews.lower().split(" review")[0]
        review_count_clean = re.sub("[^0-9]", "", review_count)
        return int(review_count_clean)

    def clean_href(self, tag):
        return tag.split("href=")[1].split("\"")[1]

    def get_num(self, page):
        return int(page.split("oa")[1].split("-")[0])

    def get_base_url(self, page):
        parts = page.split("oa")
        first_part = "http://www.tripadvisor.com" + parts[0] + "oa"
        second_part = "-" + parts[1].split("-")[1]

        return [first_part, second_part]

    def get_all_pages(self, url):
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
        
        min_page = self.get_num(self.clean_href(pages[1]))
        max_page = self.get_num(self.clean_href(pages[len(pages)-2]))
        url_parts = self.get_base_url(self.clean_href(pages[1]))

        urls = []

        for number in range(min_page, 90+30, 30):
            urls.append(url_parts[0] + str(number) + url_parts[1])

        return urls


    def get_attractions_from_page(self, url, city, client):

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
            attraction = self.get_attraction(properties[index])
            attraction['categories'] = self.get_attraction_details(attraction["url"], attraction["name"])

            if(len(attraction['categories']) > 0):
                client.insert({"city":city, "name":attraction["name"], "_id":attraction["url"], "review_count":attraction["review_count"], "categories":attraction["categories"]})
            else:
                print "Error on: " + attraction["name"]

    def get_attraction(self, prop):
        # define attraction container
        attraction = dict()

        # get first tag
        first_tag = prop.split("<")[1]

        # get the attraction_name
        attraction_name = first_tag.split(">")[1]

        try:
            review_count = self.get_review_count(prop.split("#REVIEWS\">")[1])
        except:
            review_count = 0

        # get attraction url
        attraction_url = first_tag.split("href=")[1].split("\"")[1]

        # put the data into attraction
        attraction["name"] = attraction_name
        attraction["url"] = "http://www.tripadvisor.com" + attraction_url
        attraction["review_count"] = review_count

        return attraction

    def get_attraction_details(self, attraction_url, attraction_name):
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

    def setup_database(self):

        client = MongoClient()
        points = client.wombats.points

        for index in range(0, len(self.city_info)):
            info = self.city_info[index].split("*****")

            print "Working on... " + info[0] + " (" + str(index+1) + " of " + str(len(self.city_info)) + ")"

            pages = self.get_all_pages(info[1])

            for page in pages:
                self.get_attractions_from_page(page, info[0], points)

            print "Completed " + str(index+1) + " of " + str(len(self.city_info))

        # Remove problematic entry
        points.remove({"_id":"http://www.tripadvisor.com/Attraction_Review-g44551-d8528148-Reviews-Kirkwood_Farmers_Market-Kirkwood_Saint_Louis_Missouri.html"})