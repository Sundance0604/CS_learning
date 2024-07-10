# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class Dbfcrs2Pipeline:
    fp = None

    def open_spider(self, spider):
        if spider.name == 'actor':
            self.fp = open('./actor.text', 'w', encoding='utf-8')
        elif spider.name == 'review':
            self.fp = open('./review.text', 'w', encoding='utf-8')
        else:
            pass

    def process_item(self, item, spider):
        if spider.name == 'actor':
            actor = item['actor']
            role = item['role']
            gender = item['gender']
            birthday = item['birthday']
            self.fp.write(actor + ' ' + role + '\n\t'+gender+'\n\t'+birthday+'\n')
        elif spider.name == 'review':
            idname = item['idname']
            title = item['title']
            shortcontent = item['shortcontent']
            self.fp.write(idname + '\n\t' + title + '\n\t' + shortcontent + '\n\n')
        else:
            pass
        return item

    def close_spider(self, spider):
        if self.fp:
            self.fp.close()
