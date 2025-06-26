import re
import os
import sqlite3

script_dir = os.path.abspath(os.path.dirname(__file__))
database_file = os.path.join(script_dir, "app.db")

connection = sqlite3.connect(database_file)
cursor = connection.cursor()

cursor.execute('SELECT street_type_name, street_type_id  FROM street_type')
str_types = cursor.fetchall()
street_types = {x[0]:x[1] for x in str_types}
str_type_filter = r'({}|улица)'.format('|'.join(street_types.keys()))
print(str_type_filter)


txt = 'Улица 10-летия Октября'


print(re.search(str_type_filter,txt.lower()).group(0))
# connection.close()

from transliterate import translit
print(translit('Улица 10-летия Октября', reversed=True))