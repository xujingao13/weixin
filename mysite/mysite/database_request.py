__author__ = 'caozj'

import sqlite3 as sqli


class database():
    def __init__(self):
        '''self.config = dict()
        config_file = open("mysite/database.config")
        config_content = config_file.read()
        config_list = config_content.split("\n")
        for config_item in config_list:
            config_item = config_item.split('=')
            self.config[config_item[0]] = config_item[1]'''
        self.db = sqli.connect("mysite/" + "ring_data.db")
        self.cur = self.db.cursor()
        print 789

    def __del__(self):
        self.cur.close()
        self.db.close()

    def init_db(self):
        with open('mysite/ring_data.sql', mode='r') as f:
            self.cur.executescript(f.read())
        self.db.commit()

    '''select example: "select (attribute1, attribute2,...) from table_name where attribute1 = ? and attribute2 = ? and...", [data1, data2,...]'''
    def select_data(self, command, option=list()):
        len_of_option = len(option)
        print option
        print command
        if len_of_option > 0:
            self.cur.execute(command, option)
        else:
            self.cur.execute(command)
        return self.cur.fetchall()

    '''insert example: "insert into table_name (attribute1, attribute2, ...) values (?,?,...)", [data1, data2,...]'''
    def insert_data(self, command, data_list):
        try:
            for val in data_list:
                self.cur.execute(command, val)
            self.db.commit()
            return True
        except Exception as reason:
            print(reason)
            return False

    '''delete example: delete from table_name where attribution = ?'''
    def delete_data(self, command, option=list()):
        try:
            len_of_option = len(option)
            if len_of_option > 0:
                self.cur.execute(command, option)
            else:
                self.cur.execute(command)
            self.db.commit()
            return True
        except Exception as reason:
            print(reason)
            return False

    '''update example: "update table_name set attribute=? where condition = ?", [attribute_value, condition_value]'''
    def update_data(self, command, option=list()):
        try:
            len_of_option = len(option)
            if len_of_option > 0:
                self.cur.execute(command, option)
            else:
                self.cur.execute(command)
            self.db.commit()
            return True
        except Exception as reason:
            print(reason)
            return False

def get_data(type_of_data, id):
    database_temp = database()
    if type_of_data == "step":
        return database_temp.select_data("select pace_number, datatime from user_data where userid = ?", [id])
    elif type_of_data == "distance":
        return database_temp.select_data("select distance, datatime from user_data where userid = ?", [id])
    elif type_of_data == "calorie":
        return database_temp.select_data("select calorie, datatime from user_data where userid = ?", [id])


def insert_data(type_of_data, data):
    database_temp = database()
    if type_of_data == "step":
        database_temp.insert_data("insert into user_data (userid, pace_number) values (?, ?)", data)
    elif type_of_data == "distance":
        database_temp.insert_data("insert into user_data (userid, distance) values (?, ?)", data)
    elif type_of_data == "calorie":
        database_temp.insert_data("insert into user_data (userid, calorie) values (?, ?)", data)


