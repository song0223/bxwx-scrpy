import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from bxwxcj.items import BxwxcjItem
from bxwxcj.items import BxwxzjItem
from bxwxcj.sql import Sql

class Myspider(scrapy.Spider):
    name = 'bxwxcj'
    bash_url = 'https://www.bxwx9.org/btopallvisit/0/1'
    bashurl = '.html'

    xs_type = {
        '玄幻魔法': 1,
        '武侠修真': 2,
        '现代都市': 3,
        '言情小说': 4,
        '历史军事': 5,
        '游戏竞技': 6,
        '科幻灵异': 7,
        '耽美小说': 8,
        '同人小说': 9,
        '其他类型': 10,
    }

    xs_end = {
        '连载中': 1,
        '已完成': 2,
    }

    def start_requests(self):
        yield Request(self.bash_url + self.bashurl, self.parse, dont_filter=True)

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        #max_num = soup.select_one('#pagelink .last').text# 获取排行榜最大页码
        max_num = 2
        for i in range(1, int(max_num) + 1):
            url =  str(self.bash_url)[:-1]
            base_url = url + str(i) + self.bashurl# 得到所有链接
            yield Request(base_url, self.get_xs_name)

    def get_xs_name(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        links = soup.select('#centerm table tr .odd a')# 当前页面所有小说
        for link in links:
            xs_name = link.text
            xs_url = link['href']
            yield Request(xs_url, callback = self.get_xs_info, meta = {'xs_name': xs_name, 'xs_url' : xs_url})

    def get_xs_info(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        items = BxwxcjItem()
        items['title'] = response.meta['xs_name']# 标题
        items['bxwx_url'] = response.meta['xs_url']# 链接地址

        xs_info = soup.find('td', width="82%").find_all('td')

        items['author'] = xs_info[3].text# 作者

        ending_text = xs_info[11].text
        items['is_ending'] = self.xs_end[ending_text]# 完结状态

        type_text = xs_info[1].text
        items['type'] = self.xs_type[type_text]# 小说类型

        url_arr = response.url[:-4].split('/')
        items['bxwx_id'] = url_arr[4] + '_' + url_arr[5]# 小说编号

        xs_introduction = soup.find('div', align="left").text
        xs_introduction = xs_introduction.replace('wWw.bxwx9.org', '')
        xs_introduction = xs_introduction.replace('bxwx9.org', '')
        items['introduction'] = xs_introduction.replace('\xa0', '')# 小说简介

        url = response.url.replace('binfo', 'b')
        url = url[:-4] + '/index.html'# 章节列表url
        yield items
        yield Request(url, callback = self.get_chapter_url, meta={'bxwx_id' : items['bxwx_id']})

    def get_chapter_url(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        chapter_urls = soup.select('#TabCss dl dd a')
        num = 0
        for chapter_url in chapter_urls:
            url = chapter_url['href']
            chapter_name = chapter_url.text
            url = response.url.replace('index.html', url)
            num = num + 1
            chapter_id = chapter_url['href'].rstrip('.html')# 章节编号
            rets = Sql.select_zj_id(chapter_id)
            if rets[0] == 1:
                print('章节已经存在了')
                pass
            else:
                yield Request(url = url, callback = self.get_chapter_content, meta = {'chapter_name' : chapter_name, 'chapter_id' : chapter_id, 'num' : num, 'bxwx_id' : response.meta['bxwx_id']})

    def get_chapter_content(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        items = BxwxzjItem()
        items['title'] = response.meta['chapter_name']# 章节标题
        items['bxwx_zj_url'] = response.url# 章节urla
        items['bxwx_zj_id'] = response.meta['chapter_id']# 章节编号
        items['content'] = soup.select_one('#content').prettify()
        items['sort'] = response.meta['num']# 排序
        items['book_id'] = response.meta['bxwx_id']# 小说编号
        return items