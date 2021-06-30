import os
import utils1.logging_api as logger # requires utils/loggin_api.py
import datetime
import traceback
import pymssql
import json
from flask import Flask
from flask import render_template, request, redirect, url_for
from logstash_async.handler import AsynchronousLogstashHandler
from logstash_async.formatter import FlaskLogstashFormatter

LOGSTASH_HOST = "192.168.200.19"
LOGSTASH_DB_PATH = "/home/vagrant/app-data/flask_logstash.db"
LOGSTASH_TRANSPORT = "logstash_async.transport.BeatsTransport"
LOGSTASH_PORT = 5044

logstash_handler = AsynchronousLogstashHandler(
    LOGSTASH_HOST,
    LOGSTASH_PORT,
    database_path=LOGSTASH_DB_PATH,
    transport=LOGSTASH_TRANSPORT,
)

logstash_handler.formatter = FlaskLogstashFormatter(metadata={"beat": "myapp"})

app = Flask(__name__)

logger.addHandler(logstash_handler)

def init_logger():
    with open("/Users/itamarg/Desktop/ELAL/conf.txt") as json_file:
        conf = json.load(json_file)

        logger.init(f'{conf["log_file_location"]}'+
                    f'{datetime.datetime.now().year}_'+
                    f'{datetime.datetime.now().month}_' +
                    f'{datetime.datetime.now().day}_' +
                    f'{datetime.datetime.now().hour}_' +
                    f'{datetime.datetime.now().minute}_' +
                    f'{datetime.datetime.now().second}' + '.log'
                    , conf["log_level"])
def test_db_connection():
    try:
        logger.write_lo_log(f'Testing connection to [{conf["server"]}] [{conf["database"]}]', 'INFO')
        conn = pymssql._mssql.connect(server='0.0.0.0:1433', user='', password='MySecret1976',database='ELAL')
    except Exception as e:
        tr = traceback.format_exc()
        logger.write_lo_log(f'Failed to connecto to db [{conf["server"]}] [{conf["database"]}]', 'ERROR')
        logger.write_lo_log(f'Failed to connecto to db {e}', 'ERROR')
        logger.write_lo_log(f'Failed to connecto to db {tr}', 'ERROR')
        print('Faild to connect to db ... exit')
        exit(-1)

@app.route('/flights', methods = ['GET'])
def get_all_flights():
    try:
        print(conf['server'])
        print(conf['database'])
        with pymssql._mssql.connect(server='0.0.0.0:1433', user='', password='MySecret1976',database='ELAL') as conn:
            conn.execute_query('SELECT * FROM Flights')
            result = []
            for row in conn:
                print(f'{row["flights_id"]} {row["timestamp"]} {row["remaining_seats"]} {row["orgin_country_id"]} {row["dest_country_id"]}')

                result.append({'flights_id': row["flights_id"]})

            print('=================== was pymssql._mssql connector')
            print(result)

            return json.dumps(result)
    except Exception as e:
        tr = traceback.format_exc()
        logger.write_lo_log(f'Failed to run [SELECT * FROM Flights] to db {tr}', 'ERROR')
        return json.dumps({'Error' : e})


@app.route('/flights', methods = ['POST'])
def post_new_flights():
    logger.write_lo_log('/flights POST', 'INFO')
    query = ''
    try:
        with pymssql._mssql.connect(server='0.0.0.0:1433', user='', password='MySecret1976',database='ELAL') as conn:
            new_flights = request.get_json()
            print(new_flights)
            logger.write_lo_log(f'/flights POST new flights {new_flights}', 'INFO')
            query = 'INSERT INTO flights ( timestamp, remaining_seats, orgin_country_id ,dest_country_id) '+\
                               f"VALUES ('{new_flights['timestamp']}', {new_flights['remaining_seats']}, '{new_flights['orgin_country_id']}', {new_flights['dest_country_id']});"
            logger.write_lo_log(f'/flights POST new flight query {query}', 'DEBUG')
            conn.execute_query(query)
            return json.dumps({'result' : 'succeed'})

    except Exception as e:
        tr = traceback.format_exc()
        logger.write_lo_log(f'Failed to run [{query}] to db {tr}', 'ERROR')
        return json.dumps({'Error' : e})

@app.route('/flights/<int:flights_id>', methods = ['PUT'])
def update_by_id(flights_id):
    query = ''
    try:
        with pymssql._mssql.connect(server='0.0.0.0:1433', user='', password='MySecret1976',database='ELAL') as conn:
            update_flights = request.get_json()
            logger.write_lo_log(f'/flights PUT new flights {update_flights}', 'INFO')
            query = f'UPDATE flights WHERE ID={flights_id} '+\
                               f"SET timestamp='{update_flights['timestamp']}', remaining_seats={update_flights['remaining_seats']}, " \
                               f"'orgin_country_id='{update_flights['orgin_country_id']}', dest_country_id={update_flights['dest_country_id']});"
            conn.execute_query(query)
            return '{"result" : "success"}'
    except Exception as e:
        tr = traceback.format_exc()
        logger.write_lo_log(f'Failed to run [{query}] to db {tr}', 'ERROR')
        return json.dumps({'Error' : e})

@app.route('/flights/<int:flights_id>', methods = ['DELETE'])
def del_by_id(flights_id):
    query = ''
    try:
        with pymssql._mssql.connect(server='0.0.0.0:1433', user='', password='MySecret1976',database='ELAL']) as conn:
            query = f'DELETE FROM flights WHERE ID={flights_id}'
            conn.execute_query(query)
            return '{"result" : "success"}'
    except Exception as e:
        tr = traceback.format_exc()
        logger.write_lo_log(f'Failed to run [{query}] to db {tr}', 'ERROR')
        return json.dumps({'Error' : e})


@app.route('/countries', methods = ['GET'])
def get_all_countries():
    try:
        print(conf['server'])
        print(conf['database'])
        with pymssql._mssql.connect(server='0.0.0.0:1433', user='', password='MySecret1976',database='ELAL') as conn:
            conn.execute_query('SELECT * FROM countries')
            result = []
            for row in conn:
                print(f'{row["code_AL"]} {row["name"]}' )

                result.append({'code_AL': row["name"]})

            print('=================== was pymssql._mssql connector')
            print(result)

            return json.dumps(result)
    except Exception as e:
        tr = traceback.format_exc()
        logger.write_lo_log(f'Failed to run [SELECT * FROM countries] to db {tr}', 'ERROR')
        return json.dumps({'Error' : e})

app.route('/countries', methods = ['POST'])
def post_new_countries():
    logger.write_lo_log('/countries POST', 'INFO')
    query = ''
    try:
        with pymssql._mssql.connect(server='0.0.0.0:1433', user='', password='MySecret1976',database='ELAL']) as conn:
            new_countries = request.get_json()
            print(new_countries)
            logger.write_lo_log(f'/countries POST new countries {new_countries}', 'INFO')
            query = 'INSERT INTO countries (code_AL, name) '+\
                               f"VALUES ('{new_countries['code_AL']}', {new_countries['name']});"
            logger.write_lo_log(f'/countries POST new countries query {query}', 'DEBUG')
            conn.execute_query(query)
            return json.dumps({'result' : 'succeed'})

    except Exception as e:
        tr = traceback.format_exc()
        logger.write_lo_log(f'Failed to run [{query}] to db {tr}', 'ERROR')
        return json.dumps({'Error' : e})


@app.route('/countries/<int:code_AL>', methods = ['PUT'])
def update_by_id(code_AL):
    query = ''
    try:
        with pymssql._mssql.connect(server='0.0.0.0:1433', user='', password='MySecret1976',database='ELAL') as conn:
            update_flights = request.get_json()
            logger.write_lo_log(f'/countries PUT new countries {update_countries}', 'INFO')
            query = f'UPDATE countries WHERE ID={code_AL} '+\
                               f"SET name='{update_countries['name']}');"
            conn.execute_query(query)
            return '{"result" : "success"}'
    except Exception as e:
        tr = traceback.format_exc()
        logger.write_lo_log(f'Failed to run [{query}] to db {tr}', 'ERROR')
        return json.dumps({'Error' : e})



@app.route('/countries/<int:code_AL>', methods = ['DELETE'])
def del_by_id(code_AL):
    query = ''
    try:
        with pymssql._mssql.connect(server='0.0.0.0:1433', user='', password='MySecret1976',database='ELAL']) as conn:
            query = f'DELETE FROM countries WHERE ID={code_AL}'
            conn.execute_query(query)
            return '{"result" : "success"}'
    except Exception as e:
        tr = traceback.format_exc()
        logger.write_lo_log(f'Failed to run [{query}] to db {tr}', 'ERROR')
        return json.dumps({'Error' : e})

@app.route('/Tickets', methods = ['GET'])
def get_all_Tickets():
    try:
        print(conf['server'])
        print(conf['database'])
        with pymssql._mssql.connect(server=conf['server'], user='', password='MySecret1976',
                                    database=conf['database') as conn:
            conn.execute_query('SELECT * FROM Tickets')
            result = []
            for row in conn:
                print(f'{row["ticket_id"]} {row["user_id"]} {row["flight_id"]}' )

                result.append({'ticket_id': row["ticket_id"]})

            print('=================== was pymssql._mssql connector')
            print(result)

            return json.dumps(result)
    except Exception as e:
        tr = traceback.format_exc()
        logger.write_lo_log(f'Failed to run [SELECT * FROM Tickets] to db {tr}', 'ERROR')
        return json.dumps({'Error' : e})


app.route('/Tickets', methods = ['POST'])
def post_new_countries():
    logger.write_lo_log('/Tickets POST', 'INFO')
    query = ''
    try:
        with pymssql._mssql.connect(server=conf['server'], user='', password='MySecret1976',
                                    database=conf['database']) as conn:
            new_Tickets = request.get_json()
            print(new_Tickets)
            logger.write_lo_log(f'/Tickets POST new Tickets {new_Tickets}', 'INFO')
            query = 'INSERT INTO Tickets (user_id ,flight_id) '+\
                               f"VALUES ('{new_Tickets['user_id']}', {new_countries['flight_id']});"
            logger.write_lo_log(f'/Tickets POST new Tickets query {query}', 'DEBUG')
            conn.execute_query(query)
            return json.dumps({'result' : 'succeed'})

    except Exception as e:
        tr = traceback.format_exc()
        logger.write_lo_log(f'Failed to run [{query}] to db {tr}', 'ERROR')
        return json.dumps({'Error' : e})


@app.route('/Tickets/<int:ticket_id>', methods = ['PUT'])
def update_by_id(ticket_id):
    query = ''
    try:
        with pymssql._mssql.connect(server='0.0.0.0:1433', user='', password='MySecret1976',database='ELAL']) as conn:
            update_flights = request.get_json()
            logger.write_lo_log(f'/Tickets PUT new Tickets {update_Tickets}', 'INFO')
            query = f'UPDATE Tickets WHERE ID={ticket_id} '+\
                               f"SET ticket_id='{update_Tickets['ticket_id']}', user_id={update_Tickets['user_id']}, " \
                               f"'flight_id='{update_Tickets['flight_id']}');"
            conn.execute_query(query)
            return '{"result" : "success"}'
    except Exception as e:
        tr = traceback.format_exc()
        logger.write_lo_log(f'Failed to run [{query}] to db {tr}', 'ERROR')
        return json.dumps({'Error' : e})


@app.route('/Tickets/<int:ticket_id>', methods = ['DELETE'])
def del_by_id(ticket_id):
    query = ''
    try:
        with pymssql._mssql.connect(server='0.0.0.0:1433', user='', password='MySecret1976',database='ELAL') as conn:
            query = f'DELETE FROM Tickets WHERE ID={ticket_id}'
            conn.execute_query(query)
            return '{"result" : "success"}'
    except Exception as e:
        tr = traceback.format_exc()
        logger.write_lo_log(f'Failed to run [{query}] to db {tr}', 'ERROR')
        return json.dumps({'Error' : e})




@app.route('/users', methods = ['GET'])
def get_all_users():
    try:
        print(conf['server'])
        print(conf['database'])
        with pymssql._mssql.connect(server='0.0.0.0:1433', user='', password='MySecret1976',database='ELAL') as conn:
            conn.execute_query('SELECT * FROM users')
            result = []
            for row in conn:
                print(f'{row["id_AI"]} {row["full_name"]} {row["password"]} {row["real_id"]}')

                result.append({'id_AI': row["id_AI"]})

            print('=================== was pymssql._mssql connector')
            print(result)

            return json.dumps(result)
    except Exception as e:
        tr = traceback.format_exc()
        logger.write_lo_log(f'Failed to run [SELECT * FROM users] to db {tr}', 'ERROR')
        return json.dumps({'Error' : e})


@app.route('/users', methods = ['POST'])
def post_new_users():
    logger.write_lo_log('/users POST', 'INFO')
    query = ''
    try:
        with pymssql._mssql.connect(server='0.0.0.0:1433', user='', password='MySecret1976',database='ELAL') as conn:
            new_users = request.get_json()
            print(new_users)
            logger.write_lo_log(f'/users POST new users {new_users}', 'INFO')
            query = 'INSERT INTO users ( id_AI, full_name, password ,real_id) '+\
                               f"VALUES ('{new_users['id_AI']}', {new_users['full_name']}, '{new_users['password']}', {new_users['real_id']});"
            logger.write_lo_log(f'/users POST new users query {query}', 'DEBUG')
            conn.execute_query(query)
            return json.dumps({'result' : 'succeed'})

    except Exception as e:
        tr = traceback.format_exc()
        logger.write_lo_log(f'Failed to run [{query}] to db {tr}', 'ERROR')
        return json.dumps({'Error' : e})



@app.route('/users/<int:id_AI>', methods = ['PUT'])
def update_by_id(id_AI):
    query = ''
    try:
        with pymssql._mssql.connect(server='0.0.0.0:1433', user='', password='MySecret1976',database='ELAL') as conn:
            update_users = request.get_json()
            logger.write_lo_log(f'/users PUT new users {update_users}', 'INFO')
            query = f'UPDATE users WHERE ID={update_users} '+\
                               f"SET id_AI='{update_users['id_AI']}', full_name={update_users['full_name']}, " \
                               f"'password='{update_users['password']}', real_id={update_users['real_id']});"
            conn.execute_query(query)
            return '{"result" : "success"}'
    except Exception as e:
        tr = traceback.format_exc()
        logger.write_lo_log(f'Failed to run [{query}] to db {tr}', 'ERROR')
        return json.dumps({'Error' : e})


@app.route('/users/<int:id_AI>', methods = ['DELETE'])
def del_by_id(id_AI):
    query = ''
    try:
        with pymssql._mssql.connect(server='0.0.0.0:1433', user='', password='MySecret1976',database='ELAL') as conn:
            query = f'DELETE FROM users WHERE ID={id_AI}'
            conn.execute_query(query)
            return '{"result" : "success"}'
    except Exception as e:
        tr = traceback.format_exc()
        logger.write_lo_log(f'Failed to run [{query}] to db {tr}', 'ERROR')
        return json.dumps({'Error' : e})



def main():
    init_logger()
    logger.write_lo_log('**************** System started ...', 'INFO')

    #test_db_connection()

with open('C:/Users/itamar.gabay/user.conf.txt') as json_file:
    conf = json.load(json_file)
main()
app.run(debug=True)