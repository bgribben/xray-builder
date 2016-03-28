from bs4 import BeautifulSoup
import sqlite3
import os

os.remove('./test.db')

tables = [  "CREATE TABLE excerpt(id INTEGER, start INTEGER, length INTEGER, image TEXT, related_entities TEXT, goto INTEGER, PRIMARY KEY(id))",
            "CREATE TABLE entity(id INTEGER, label TEXT, loc_label INTEGER, type INTEGER, count INTEGER, has_info_card TINYINT, PRIMARY KEY(id))",
            "CREATE TABLE type(id INTEGER, label INTEGER, singular_label INTEGER, icon INTEGER, top_mentioned_entities TEXT, PRIMARY KEY(id))",
            "CREATE TABLE entity_description(text TEXT, source_wildcard TEXT, source INTEGER, entity INTEGER, PRIMARY KEY(entity))",
            "CREATE TABLE occurrence(entity INTEGER, start INTEGER, length INTEGER)",
            "CREATE TABLE string(id INTEGER, language TEXT, text TEXT)",
            "CREATE TABLE source(id INTEGER, label INTEGER, url INTEGER, license_label INTEGER, license_url INTEGER, PRIMARY KEY(id))",
            "CREATE TABLE entity_excerpt(entity INTEGER, excerpt INTEGER)",
            "CREATE TABLE book_metadata(srl INTEGER, erl INTEGER, has_images TINYINT, has_excerpts TINYINT, show_spoilers_default TINYINT, num_people INTEGER, num_terms INTEGER, num_images INTEGER, preview_images TEXT)",
            "CREATE INDEX idx_occurrence_start ON occurrence(start ASC)",
            "CREATE INDEX idx_entity_type ON entity(type ASC)",
            "CREATE INDEX idx_entity_excerpt ON entity_excerpt(entity ASC)"]

soup = BeautifulSoup(open("test.html"), "html.parser")

conn = sqlite3.connect("test.db")
c = conn.cursor()
entityId = 1

for table in tables:
    c.execute(table)

for x in soup.select("#WikiModule_Characters ul.li_6 li"):
    c.execute("INSERT INTO entity (label, type, has_info_card) VALUES ('{0}', 1, 1)".format(x.text.partition(":")[0].replace("'", "\\'")))
    c.execute("INSERT INTO entity_description (text, entity) VALUES ('{0}', {1})".format(x.text.partition(":")[2].replace(u"\u2018", "'").replace(u"\u2019", "'").replace("'", "''"), entityId))
    entityId+=1

for x in soup.select("#WikiModule_Settings ul.li_6 li"):
	c.execute("INSERT INTO entity (label, type, has_info_card) VALUES ('{0}', 2, 1)".format(x.text.partition(":")[0].replace("'", "\\'")))
	c.execute("INSERT INTO entity_description (text, entity) VALUES ('{0}', {1})".format(x.text.partition(":")[2].replace(u"\u2018", "'").replace(u"\u2019", "'").replace("'", "''"), entityId))
	entityId+=1

conn.commit()
conn.close()

