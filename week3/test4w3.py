from pymongo import MongoClient

client = MongoClient('localhost',27017)
db = client.dbsparta

param = {'title' : '매트릭스'}
movie = db.movies.find_one(param)

star = movie['star']

param2 = {'star' : star}
data = {'star' : 0}
db.movies.update_many(param2,{'$set': data})