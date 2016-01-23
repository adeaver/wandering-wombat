from pymongo import MongoClient

class Wombats_Db():

    def __init__(self):
        self.CLIENT = MongoClient()
        self.DB = self.CLIENT.wombats.points

    def get_from_category(self, categories):
        query = self.DB.find({"categories":{"$in":categories}})
        return query

    def get_from_city(self, city_name):
        query = self.DB.find({"city":city_name})
        return query

    def sort_results_by_review_count(self, data):
        if(len(data) == 1):
            return data
        else:
            data1 = self.sort_results_by_review_count(data[:len(data)/2])
            data2 = self.sort_results_by_review_count(data[len(data)/2:])

            return self.merge(data1, data2)

    def merge(self, data1, data2):
        data = []
        i = 0
        j = 0

        for index in range(0, len(data1)+len(data2)):
            if(i >= len(data1)):
                data += data2
                break
            
            if(j >= len(data2)):
                data += data1
                break

            if(data1[i]["review_count"]>data2[j]["review_count"]):
                data.append(data1[i])
                i += 1
            else:
                data.append(data2[j])
                j += 1

        return data
