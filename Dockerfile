FROM python:3.6
ENV PATH /usr/local/bin:$PATH
ADD . /code
WORKDIR /code
RUN pip3 install -r requirements.txt -i https://pypi.douban.com/simple
CMD scrapy runspider book