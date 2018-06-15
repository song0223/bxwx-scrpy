# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from .sql import Sql
from bxwxcj.items import BxwxcjItem
from bxwxcj.items import BxwxzjItem

class BxwxcjPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, BxwxcjItem): ##item中存在DingdianItem
            bxwx_id = item['bxwx_id']
            ret = Sql.select_xs_id(bxwx_id)
            if ret[0] == 1:
                print(item['title'] + '已经存在！')
                pass
            else:
                title = item['title']
                author = item['author']
                is_ending = item['is_ending']
                type = item['type']
                bxwx_id = item['bxwx_id']
                introduction = item['introduction']
                bxwx_url = item['bxwx_url']
                Sql.insert_xs(title, author, 0, is_ending, type, bxwx_id, introduction, bxwx_url)
                print('开始录入小说--标题：' + title)

        if isinstance(item, BxwxzjItem):
            book_id = item['book_id']
            bxwx_id = item['bxwx_zj_id']
            bxwx_url = item['bxwx_zj_url']
            title = item['title']
            content = item['content']
            sort = item['sort']
            Sql.insert_zj_content(book_id, bxwx_id, bxwx_url, title, content, sort)
            print('开始录入章节！：' + title)