"""

"""

import csv
import os
import configparser
import snowflake.connector
import sqlparse
from datetime import datetime
import requests
import json
import pandas
import logging



def getConnProp():
    global configConn
    configConn = configparser.RawConfigParser()
    configConn.read('./properties/configConnection.properties')
    return

def getPassProp():
    global configPass
    getExeProp()
    try:
        password_location = configExecute.get('conditions', 'password_location')
        print("Password location = ",password_location)
        configPass = configparser.RawConfigParser()
        configPass.read(password_location)
    except:
        password_location = "Not found"
        print("Could not find password in location mentioned.")
        exit()
    return

# Add Email ID and Password below


def makeSSOConnection(connectionName):
    getConnProp()
    getPassProp()
    # Fetch  all values for sso snowflake connection
    username = configConn.get(connectionName, 'username')
    password = configPass.get(connectionName,'password')
    warehouse = configConn.get(connectionName, 'warehouse')
    database = configConn.get(connectionName, 'database')
    schema = configConn.get(connectionName, 'schema')
    role = configConn.get(connectionName, 'role')
    account = configConn.get(connectionName, 'account')
    authenticator = configConn.get(connectionName, 'authenticator')
    client_id = configConn.get(connectionName, 'client_id')
    client_secret = configConn.get(connectionName, 'client_secret')
    grant_type = configConn.get(connectionName, 'grant_type')
    scope = configConn.get(connectionName, 'scope')
    url = configConn.get(connectionName, 'url')

    # Parameters to pass to get access token
    data2 = {
        'client_id': client_id,
        'client_secret': client_secret,
        'username': username,
        'password': password,
        'grant_type': grant_type,
        'scope': scope
    }

    # Get access-token from AWS privatelink (DO NOT CHANGE)
    headers = {
        'Content-type': 'application/x-www-form-urlencoded;charset=UTF-8'
    }
    
    response = requests.post(url, headers=headers, data=data2)

    response_json = json.loads(response.text)
    try:
        access_token = response_json['access_token']
        print("Access token generated")
    except:
        print("Access token not received")
        exit()

    # Change user,warehouse,role,database,schema as required below
    cursor_target = snowflake.connector.connect(
        user=username,
        account=account,
        authenticator=authenticator,
        warehouse=warehouse,
        role=role,
        database=database,
        schema=schema,
        token=access_token
    )
    print("Logging in for User: ",username)
    return cursor_target


def makeSnowflakeConnection(connectionName):
    getConnProp()
    getPassProp()

    warehouse = configConn.get(connectionName, 'warehouse')
    username = configConn.get(connectionName, 'username')
    password = configConn.get(connectionName,'password')
    database = configConn.get(connectionName, 'database')
    account = configConn.get(connectionName, 'account')
    schema = configConn.get(connectionName, 'schema')
    role = configConn.get(connectionName, 'role')
    
    cursor_target = snowflake.connector.connect(
        user=username,
        password=password,
        account=account,
        warehouse=warehouse,
        database=database,
        schema=schema,
        role=role
    )
    print("Logging in for User: ",username)
    return cursor_target


def getExeProp():
    global configExecute
    configExecute = configparser.RawConfigParser()
    configExecute.read('./properties/configExecution.properties')
    return
