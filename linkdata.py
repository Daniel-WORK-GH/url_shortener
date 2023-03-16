import sqlite3 as db
import database as db
from config import WEBSITE_DOMAIN

LOOKUP = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-."
LEN = len(LOOKUP)

class Linkdata:
    def __init__(self, full_link : str, shortened : str = None):
        self.full_link = full_link
        if shortened: self.shortened = shortened
        else: self.shortened = Linkdata.generate_shortlink(full_link)

    def __repr__(self) -> str:
        return f"(Linkdata : \n\tfull_link = {self.full_link}\n\tshortened = {self.shortened})"

    def to_tuple(self):
        return (
            self.full_link,
            self.shortened,
        )
    
    @staticmethod
    def generate_shortlink(full_link : str) -> str:
        original_val = hash(full_link)
        offset = 0
        ret = ""

        # HACK: horrible implementation, can ran for a very
        # large amout of time, should use a diffrent nmethod
        while True:
            val = original_val + offset
            while val != 0:
                data = val % LEN
                val //= LEN
                if val < 0: val += 1
                ret += str(LOOKUP[data])
                
            if not db.is_value_exists(ret):
                offset += 1
                break

        return f"{ret}"