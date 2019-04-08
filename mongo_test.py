import pymongo

client = pymongo.MongoClient('mongodb://db.guozr.im:27017')
db = client['library']
collection = db['books']


def get_ids():
    id_lists = []
    for item in collection.find():
        id = item['id']
        id_lists.append(id)
        print(id)
    return id_lists

# id_lists = get_ids()
# with open('id.txt', 'w') as f:
#     f.write('[')
#     for id in id_lists:
#         f.write('\''+id+'\', ')
#     f.write(']')
