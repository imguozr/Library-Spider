import redis

redis_cli = redis.Redis(host='localhost', port=6379, password='foobared')

for book_id in range(180580, 10000000):
    url = 'http://202.119.228.6:8080/opac/item.php?marc_no=' + '%010d' % book_id
    # print(book_id)
    redis_cli.lpush('book:start_urls', url)
