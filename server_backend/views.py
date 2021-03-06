from flask import request, Flask
from wombats_db import Wombats_Db
from scrape_locations import db_setup
import json, re, sys

db_manager = Wombats_Db()
app = Flask(__name__)

@app.route("/api/getLocations", methods=["GET"])
def get_locations():
    try:
        # Preferences, Number of Cities
        category_parameters = [re.sub("And", "&", arg.title()) for arg in request.args.get("q").split(",")]
        number_of_cities = int(request.args.get("count")) if "count" in request.args else -1

        cursor = db_manager.get_from_category(category_parameters)
        data = []
        cities = dict()

        for obj in cursor:
            data.append(obj)

        data_sorted = db_manager.sort_results_by_review_count(data)
        for item in data_sorted:
            city_name = item["city"] if item["city"] != "Grand Canyon" and item["city"] != "Sedona" else "Phoenix"

            point_data = cities.get(city_name, [])

            if(number_of_cities != -1):
                if(len(cities.keys()) == number_of_cities and point_data == []):
                    continue

            point_data.append(item["name"])
            cities[city_name] = point_data

        for key in cities:
            city_list = cities[key]
            city_list.sort()
            cities[key] = db_manager.unique(city_list)

        cities["cities"] = db_manager.get_best_route(db_manager.unique(cities.keys()))

        final = dict()
        final["response"] = "America is great"
        final["data"] = cities

        return str(final)
    except Exception as e:
        final = dict()
        final["response"] = "You've been Trumped"
        final["data"] = dict()
        final["error"] = e

        return str(final)

@app.route('/db/setup', methods=["GET"])
def setup_db():
    if(db_manager.is_empty()):
        db = db_setup()
        db.setup_database()
        return "Successful"
    else:
        return "DB already exists"

if __name__ == "__main__":
    app.run(debug=True)