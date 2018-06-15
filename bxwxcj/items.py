# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BxwxcjItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ##小说录入字段
    # define the fields for your item here like:
    title = scrapy.Field()  # 小说名字
    author = scrapy.Field()  # 作者
    image = scrapy.Field()  # 小说封面
    is_ending = scrapy.Field()  # 小说状态是否完结
    type = scrapy.Field()  # 文章类别
    bxwx_id = scrapy.Field()  # 小说编号
    bxwx_url = scrapy.Field()  # 小说链接
    introduction = scrapy.Field()  # 小说简介

##小说章节录入字段
class BxwxzjItem(scrapy.Item):
    book_id = scrapy.Field()  # 小说id
    bxwx_zj_id = scrapy.Field()  # 章节id
    bxwx_zj_url = scrapy.Field()  # 章节url
    title = scrapy.Field()  # 章节标题
    content = scrapy.Field()  # 章节内容
    sort = scrapy.Field()  # 排序
