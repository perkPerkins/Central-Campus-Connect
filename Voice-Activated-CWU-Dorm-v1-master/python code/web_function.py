# Made by Patrick & Emily 
# on 1/25/2020
# Updated last: 1/26/2020
import urllib.parse
import requests
import urllib
import sys
import logging
import pymysql
from bs4 import BeautifulSoup
    
# scrape Google
class Google:
    def __init__(self, slot_list):
        mySlot = ' '.join(slot_list)
        self.slot_string = urllib.parse.quote_plus(mySlot)
        self.url = 'https://google.com/search?q={0}'.format(self.slot_string)

    def scrape (self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        #print(soup)
        big_box_results = soup.find_all('div', class_='BNeawe s3v9rd AP7Wnd')#'HwtpBd gsrt PZPZlf')
        # for b in big_box_results:
        #     print(b)
        # print(big_box_results[0].contents[0].contents)
        return str(big_box_results[0].contents[0].contents)
        # So whenever there is no time box on google, create an if statement that will look
        # at the cwu calender instead OR look at the database for the results.
        # this can be done by checking if the 'big_box_results[0].contents[0].contents' has </div.
        # if it does then that means there is no box from google and we need to check somewhere else (db or calender)
        #if big_box_results[0].contents[0].contents.contains('div'): ----- finish this later

#REMEMBER! I TURN OFF DB WHEN NOT IN USE
# Add another method here that will search the database instead if there
# is no information on Google or the Calender
class Db_session:
    
    
    def __init__(self):

        self.primary_keys = {"Buildings":"building_name", "Clubs":"club_name", "Staff":"staff_name", "Events":"event_name", "Offices":"office_name", "Students":"id"}
        
        #Temporary db config info location
        self.rds_host  = "db-centralconnect.cqvokg1if3d4.us-east-2.rds.amazonaws.com"
        self.name = "CWUAdmin"
        self.password = "CWUdbMaster!"
        self.db_name = "cwudb"
    
    def connect_to_db(self, rds_host, username, password, db_name):
        
        try:
            self.conn = pymysql.connect(rds_host, user=username, passwd=password, db=db_name, connect_timeout=5)
            print("I actually connected")
            return True
        except pymysql.MySQLError as e:
            print("CWU Official Error:")
            print(e)
            return False
    
    # tableName: name of table
    # primaryKey: value of the primary key of a row
    # returns a list of values simbolizing the desired row from the table
    def get_row_from_table(self, tableName, primaryKey):
        with self.conn.cursor() as cur:
            command = "select * from " + tableName + " where " + tableName + "." + self.primary_keys[tableName] + " = '" + str(primaryKey) + "'"
            cur.execute(command)
            for row in cur:
                return row
    
    # Return x amount of results from t table
    
    
    # Here will be the logic for accessing the table containing canvas authentication
    
    # Here will be the logic for accessing the table containing authentication for PII (possible the same as previous comment)
        
    def add_building(self, building_name, building_loc, open_time, close_time, purpose):
        with self.conn.cursor() as cur:
            command = "insert into Buildings(building_name, building_loc, open_time, close_time, purpose) values (\'" + building_name +"\', \'" + building_loc +"\', \'" + open_time +"\', \'" + close_time +"\', \'" + purpose +"\')"
            cur.execute(command)
            self.conn.commit()
            self.test_func()
            
    def test_func(self):
        with self.conn.cursor() as cur:
            cur.execute("select * from Buildings")
            for row in cur:
                print(row)
            
        #self.conn.commit()

def start_web(list_of_slots):
    list_of_slots.append('cwu')
    convert_lst = ""
    googlez = Google(list_of_slots) # search Google
    googlez = googlez.scrape()
    return googlez
