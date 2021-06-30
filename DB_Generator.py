import requests
import os
import utils1.logging_api as logger # requires utils/loggin_api.py
import datatime
import pymssql
import json
import random


def UpdateUsers():
    url="https://randomuser.me/api/"
    resp=requests.get(url)
    customers=json.load(resp.content)
    print(customers)
    full_name=customers['results'][0]['name']['first']
    print(full_name)
    id=random.randint(1,100)
    password=random.randint(1,100000)
    print(password)

with pymssql._mssql.connect(server=conf['server'], user='', password='',database=conf['database']) as conn:
    query = 'INSERT INTO users ( full_name, password, password ,id) ' + \
            f"VALUES ('{new_users['full_name']}', '{new_users['password']}', '{new_users['real_id']}'););"
    conn.execute_query(query)


def UpdateFlights():
 for _ in range(25):
    timestamp=datetime()
    remaining_seats=random.randint(0,50)
    orgin_country_id=random.randint(1,3)
    dest_country_id=random.randint(1,3)

with pymssql._mssql.connect(server=conf['server'], user='', password='',
                                    database=conf['database']) as conn:
    query = 'INSERT INTO flights ( timestamp, remaining_seats, orgin_country_id ,dest_country_id) ' + \
            f"VALUES ('{new_flights['timestamp']}', {new_flights['remaining_seats']}, '{new_flights['orgin_country_id']}', {new_flights['dest_country_id']});"
    conn.execute_query(query)


def UpdateTickets():
 for _ in range(30):
    flight_id=random.randint(0,50)
    user_id=random.randint(1,50)

    with pymssql._mssql.connect(server=conf['server'], user='', password='', database=conf['database']) as conn:
        query = 'INSERT INTO tickets (user_id,flight_id) ' + \
            f"VALUES ('{new_tickets['user_id']}', {new_tickets['flight_id']},);"
        conn.execute_query(query)