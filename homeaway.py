# -*- coding: utf-8 -*-

import MySQLdb
import time
from enum import Enum
import subprocess


class State(Enum):
    Home = 0
    Away = 1


if __name__ == "__main__":

    # Get LAN State to check existence of IPhone
    arp_result = subprocess.getoutput('sudo arp-scan -I eth0 -l')
    # Show arp-scan result
    print(arp_result)
    # Check if IPhone MAX adress is in LAN
    MacMatch = arp_result.find('xx:xx:xx:xx:xx:xx')
    if MacMatch == -1:
        CurrentState = State.Away
    else:
        CurrentState = State.Home

    # Connect to MySQL server
    connector = MySQLdb.connect(host="localhost", db="homeaway", user="user_homeaway", passwd="pass_homeaway",
                                charset="utf8")
    cursor = connector.cursor()

    sql = u"insert into homeaway_table(`id`,`date`,`state`) values(0,now(),'%s')" % CurrentState.name
    cursor.execute(sql)
    connector.commit()

    cursor.close()
    connector.close()

    # Show Current State
    print(CurrentState.name)
