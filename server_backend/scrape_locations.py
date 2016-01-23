from pattern.web import download

def get_attractions_from_page(url):
    attractions = []
    html = download(url)
    properties = html.split("property_title\">")

 
    for index in range(1, len(properties)):
        attraction = get_attraction(properties[index])
        attraction['categories'] = get_attraction_details(attraction["url"])

        if(len(attraction['categories']) > 0):
            attractions.append(attraction)

    return attractions

def get_attraction(prop):
    # define attraction container
    attraction = dict()

    # get first tag
    first_tag = prop.split("<")[1]

    # get the attraction_name
    attraction_name = first_tag.split(">")[1]

    # get attraction url
    attraction_url = first_tag.split("href=")[1].split("\"")[1]

    # put the data into attraction
    attraction["name"] = attraction_name
    attraction["url"] = "http://www.tripadvisor.com" + attraction_url

    return attraction

def get_attraction_details(attraction_url):
    html = download(attraction_url)

    # get the descriptions of the location in the ugliest line of code I've ever written
    try:
        details = html.split("div class=\"detail\">")[1].split("</div>")[0]
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

def get_all_pages(url):
    html = download(url)

    # get the page numbers element
    pageNumbers = html.split("class=\"pageNumbers\">")[1]
    pageNumbers = pageNumbers.split("</div>")[0]

    # get a list of all the pages
    pages = pageNumbers.split("<")[2:]
    
    min_page = get_num(clean_href(pages[1]))
    max_page = get_num(clean_href(pages[len(pages)-2]))
    url_parts = get_base_url(clean_href(pages[1]))

    urls = []

    for number in range(min_page, max_page+30, 30):
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


pages = get_all_pages("http://www.tripadvisor.com/Attractions-g60763-Activities-New_York_City_New_York.html")
for page in pages:
    print get_attractions_from_page(page)
# print get_attractions_from_page("http://www.tripadvisor.com/Attractions-g60763-Activities-New_York_City_New_York.html")
# f = open("ny.txt", "w")
# f.write(properties[len(properties)-1])
# f.close()