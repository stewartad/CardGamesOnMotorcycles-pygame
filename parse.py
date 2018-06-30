# Handles db access

import sqlite3

con = sqlite3.connect('cards.db')
s = con.cursor()


def get_card_query(card_id):
    query = s.execute("SELECT * FROM {table} WHERE {idf}={my_id}".
                      format(table="cards", idf='ID', my_id=card_id))
    return list(s.fetchone())