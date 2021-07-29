from auth_data import *
import psycopg2

conn = psycopg2.connect(dbname='shop_table', user='postgres',
                        password=mypassword, host='localhost')

cursor = conn.cursor()


def add_to_shop(id_of_item, type_of_item, name_of_item, number_of_item):
    global cursor, conn
    SQL_query = "insert into shop_items (id, type, name, count) values (%d, '%s', '%s', %d);" % (
        id_of_item, type_of_item, name_of_item, number_of_item)
    # print(SQL_query)
    cursor.execute(SQL_query)
    conn.commit()


def find_number_of(item):
    SQL_query = 'select count from shop_items ' + 'where name = ' + "'" + item + "'" + ' order by count;'
    cursor.execute(SQL_query)
    return sum(int(x) for row in cursor.fetchall() for x in row)


def get_price_for(item):
    SQL_query = 'select price from shop_items ' + 'where name = ' + "'" + item + "'" + ' order by count;'
    cursor.execute(SQL_query)
    return sum(int(x) for row in cursor.fetchall() for x in row)


def get_what_we_have():
    SQL_query = 'select name, count from shop_items where count > 0  order by count;'
    cursor.execute(SQL_query)
    result = list(" ".join(map(str, row)) for row in cursor.fetchall())
    # print(result)
    return result


def get_items_list(type):
    SQL_query = 'select name from shop_items ' + 'where type = ' + "'" + type + "'" + ' order by count;'
    cursor.execute(SQL_query)
    return list((map(str, row) for row in cursor.fetchall()))


def get_items(type):
    SQL_query = 'select name, price, count from shop_items ' + 'where type = ' + "'" + type + "'" + ' order by count;'
    cursor.execute(SQL_query)
    return "\n".join(' '.join(map(str, row)) for row in cursor.fetchall())

# get_what_we_have()
