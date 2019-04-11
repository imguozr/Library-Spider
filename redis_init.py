import redis

redis_cli = redis.Redis(host='localhost', port=6379, password='foobared')

# for book_id in range(520000, 8500000):
#     url = 'http://202.119.228.6:8080/opac/item.php?marc_no=' + '%010d' % book_id
#     print(book_id)
#     redis_cli.rpush('book:start_urls', url)

for book_id in range(8500000, 1000000, -1):
    url = 'http://202.119.228.6:8080/opac/item.php?marc_no=' + '%010d' % book_id
    print(book_id)
    redis_cli.rpop('book:start_urls')
