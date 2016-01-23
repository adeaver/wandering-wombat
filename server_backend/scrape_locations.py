from pattern.web import download

def get_attractions_from_page(url):
    html = download(url)
    properties = html.split("property_title\">")
    
    for index in range(1, len(properties)):
        print get_attraction(properties[index])

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
    attraction[attraction_name] = attraction_url

    return attraction

get_attractions_from_page("http://www.tripadvisor.com/Attractions-g60763-Activities-New_York_City_New_York.html")
# f = open("ny.txt", "w")
# f.write(properties[len(properties)-1])
# f.close()