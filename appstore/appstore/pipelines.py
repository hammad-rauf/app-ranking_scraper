import mysql.connector

class AppstorePipeline(object):
    def __init__(self):

        self.create_connection()
        #self.create_table()
        pass

    def create_connection(self):

        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'H@mmad123',
            database = 'appranking'
        )
        self.curr = self.conn.cursor()
    
    def create_table(self):

        self.curr.execute("drop table if exists appranking_table")
        self.curr.execute("CREATE TABLE appranking_table( date text, subcategory text,category text, type text, ranking int, app_name text, app_link text)")

    def process_item(self, item, spider):

        self.store_db(item)

        return item

    def store_db(self,item):

        self.curr.execute(f"insert into appranking_table values ('{item['date']}','{item['subcategory']}','{item['category']}','{item['type']}',{item['ranking']},'{item['app_name']}','{item['app_link']}')")

        self.conn.commit()