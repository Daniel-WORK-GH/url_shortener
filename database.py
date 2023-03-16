#https://www.codecademy.com/article/sql-commands
import sqlite3 as db
from linkdata import Linkdata

TABLE = "Links"
FULL_LINK_COL, SHORT_LINK_COL = "full_link", "shortened"

connection = db.connect("localdatabase.db")
cursor = connection.cursor()

def create_table():
    command = f"""
        CREATE TABLE IF NOT EXISTS {TABLE} (
        {FULL_LINK_COL} TEXT,
        {SHORT_LINK_COL} TEXT
        );"""
    cursor.execute(command)
    
def add_value(link : Linkdata):
    command = f"""
        INSERT INTO {TABLE}
        VALUES {link.to_tuple()};
        """
    cursor.execute(command)
    
def get_value(full_link) -> Linkdata:
    command = f"""
        SELECT * FROM {TABLE} 
        WHERE {FULL_LINK_COL}='{full_link}'; 
        """
    cursor.execute(command)
    value = cursor.fetchone()
    if value: return Linkdata(*value)

def generate_value(full_link):
    linkdata = Linkdata(full_link)
    add_value(linkdata)
    return linkdata

def is_value_exists(shortened):
    if get_original_url(shortened) != None:
        return True
    return False

def get_original_url(shortened) -> Linkdata:
    command = f"""
        SELECT * FROM {TABLE} 
        WHERE {SHORT_LINK_COL}='{shortened}'; 
        """   
    cursor.execute(command)
    value = cursor.fetchone()
    if not value: return
    return Linkdata(*value)

def save_changes():
    connection.commit()

def clear():
    command = f"""DELETE FROM {TABLE};"""
    cursor.execute(command)

create_table()