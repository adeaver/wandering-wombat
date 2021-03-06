# -*- coding: utf-8 -*-

from pymongo import MongoClient
from haversine import haversine
import re


class Wombats_Db():

    def __init__(self):
        self.CLIENT = MongoClient()
        self.DB = self.CLIENT.wombats.points
        self.COORDINATES = {"New York City":(40.7217, 74.0059), "Chicago":(41.8369, 87.6847), "Charleston":(32.7833,79.9333),
        "Las Vegas":(36.1215, 115.1739), "Seattle":(47.6097, 122.3331), "San Francisco":(37.7833, 122.4167), "Washington D.C.":(38.9047, 77.0164),
        "New Orleans":(29.9500, 90.0667), "St. Louis":(38.6272, 90.1978), "Phoenix":(33.4500, 112.0667), "Los Angeles":(34.0500, 118.2500),
        "Philadelphia":(39.9500, 75.1667), "Denver":(39.7392, 104.9903), "Salt Lake City":(40.7500, 111.8833), "Yosemite":(37.8499, 119.5677),
        "Orlando":(28.4158, 81.2989)}

    def is_empty(self):
        cursor = self.DB.find()
        return cursor.count() == 0

    def get_from_category(self, categories):
        query = self.DB.find({"categories":{"$in":categories}})
        return query

    def get_from_city(self, city_name):
        query = self.DB.find({"city":city_name})
        return query

    def unique(self, old_list):
        token = ""
        new_list = []

        for item in old_list:
            if(item != token):
                new_list.append(self.clean(item))
                token = item

        return new_list

    def sort_results_by_review_count(self, data):
        if(len(data) == 1):
            return data
        else:
            data1 = self.sort_results_by_review_count(data[:len(data)/2])
            data2 = self.sort_results_by_review_count(data[len(data)/2:])

            return self.merge("review_count", data1, data2)

    def merge(self, key, data1, data2):
        data = []
        i = 0
        j = 0

        for index in range(0, len(data1)+len(data2)):
            if(i >= len(data1)):
                data += data2[j:]
                break
            
            if(j >= len(data2)):
                data += data1[i:]
                break

            if(data1[i][key]>data2[j][key]):
                data.append(data1[i])
                i += 1
            else:
                data.append(data2[j])
                j += 1

        return data

    def clean(self, inp):
        output = re.sub("\'", "", inp)
        output = re.sub(":", "-", output)
        output = re.sub("/", "-", output)
        output = re.sub("#", "", output)

        return output

    def merge_sort_distances(self, data):
        if(len(data) == 1):
            return data
        else:
            data1 = self.merge_sort_distances(data[:len(data)/2])
            data2 = self.merge_sort_distances(data[len(data)/2:])

            return self.merge(1, data1, data2)

    def get_best_route(self, cities):
        fastest_route = []
        fastest_distance = 0

        for index in range(0, len(cities)):
            without_first_city = [cities[x] for x in range(len(cities)) if x != index]
            route_info = [[cities[index], 0]] + self.order_cities_by_distance(cities[index], without_first_city)

            distance = sum([item[1] for item in route_info])
            route = [item[0] for item in route_info]

            if(len(fastest_route) == 0 or fastest_distance > distance):
                fastest_route = route
                fastest_distance = distance

        return fastest_route

    def order_cities_by_distance(self, last_city, cities):
        coords = self.COORDINATES[last_city]
        coords_test = self.COORDINATES[cities[0]]

        closest_distance = haversine(coords, coords_test, miles=True)
        closest_index = 0 

        if(len(cities) == 1):
            return [[cities[0], closest_distance]]

        for index in range(1, len(cities)):
            coords_test = self.COORDINATES[cities[index]]
            distance = haversine(coords, coords_test, miles=True)

            if(closest_distance>distance):
                closest_distance = distance
                closest_index = index

        next_city = cities.pop(closest_index)

        return [[next_city, closest_distance]] + self.order_cities_by_distance(next_city, cities)