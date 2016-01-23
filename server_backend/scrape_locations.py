from pattern.web import download

def get_attractions_from_page(url):
    html = download(url)
    properties = html.split("property_title\">")
    
    # for index in range(1, len(properties)):
    #     print get_attraction(properties[index])
    attraction = get_attraction(properties[1])
    #print get_attraction_details(attraction["url"])

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
    details = html.split("div class=\"detail\">")[1].split("</div>")[0]

    # split up the details into categories
    list_details = []

    jank_details = details.split(", ")

    # I'm not really sure what I'm doing here but it works
    for jank in jank_details:
        title = jank.split("<")[1]
        clean_title = title.split(">")[1]

        list_details.append(clean_title)

    return list_details

get_attractions_from_page("http://www.tripadvisor.com/Attractions-g60763-Activities-New_York_City_New_York.html")
# f = open("ny.txt", "w")
# f.write(properties[len(properties)-1])
# f.close()