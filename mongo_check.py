import pymongo

client = pymongo.MongoClient('mongodb://db.guozr.im:27017')
db = client['library']
collection = db['books']


def get_ids():
    id_lists = []
    list = []
    for item in collection.find():
        id = item['id']
        id_lists.append(id)
        print(id)
    for i in range(1, 850000):
        stri = str('%010d' % i)
        if stri not in id_lists:
            print(stri)
            list.append(stri)
    return list

id_lists = get_ids()
with open('id.txt', 'w') as f:
    f.write('[')
    for id in id_lists:
        f.write('\''+id+'\', ')
    f.write(']')
