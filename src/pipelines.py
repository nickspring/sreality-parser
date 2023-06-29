# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import os

import psycopg2
from psycopg import Error


class SrealityParserPipeline:
    """We will save data to Postgresql using this pipeline"""

    def __init__(self):
        """Connect to db and create cursor on init"""
        try:
            self.connection = psycopg2.connect(
                user=os.getenv("POSTGRES_USER"),
                password=os.getenv("POSTGRES_PASSWORD"),
                host=os.getenv("POSTGRES_HOST"),
                port=os.getenv("POSTGRES_PORT"),
                database=os.getenv("POSTGRES_DATABASE"),
            )

            self.cursor = self.connection.cursor()

            # create table if not exists
            self.cursor.execute(
                """
            CREATE TABLE IF NOT EXISTS ads(
                id SERIAL PRIMARY KEY,
                title VARCHAR(250),
                image VARCHAR(250)
            )
            """
            )

            # erase table - as we would like to have each run new data
            self.cursor.execute("TRUNCATE TABLE ads")
            self.connection.commit()

        except (Exception, Error) as error:
            print("Error while connecting to PostgreSQL", error)

    def process_item(self, item, spider):
        """Save each item to db"""
        query = "INSERT INTO ads (title, image) VALUES (%s, %s)"

        self.cursor.execute(query, (item["title"], item["image"]))
        self.connection.commit()

        return item

    def close_spider(self, spider):
        """Close cursor & connection to database"""

        self.cursor.close()
        self.connection.close()
