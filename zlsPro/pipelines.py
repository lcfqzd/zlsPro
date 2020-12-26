# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from openpyxl import Workbook

# 创建工作薄Workbook
book = Workbook()

# 创建工作表Sheet
sheet = book.create_sheet('4567电影网_喜剧电影', 0)

# 向工作表中添加数据
sheet.append(['电影名', '链接', '简述'])


class ZlsproPipeline:

    def open_spider(self,spider):
        pass

    def process_item(self, item, spider):
        # conn = spider.conn  # 调用声明在Spider类中redis的链接对象
        print(item)
        # conn.lpush('movieData',str(item))

        row = [item['title'], item['detail_url'], item['desc']]
        sheet.append(row)

        # 输出保存
        book.save('4567电影网_喜剧电影.xls')

        return item

    def close_spider(self,spider):
        pass


