"""

"""

from snowflake.connector.secret_detector import SecretDetector
from configFunctionsPython import *
import sys
import os.path
from os import path
import time

# Get execution configurations parameters
sso_login, continue_on_failure, variable_substitution, show_errors_on_console, append_master_csv_log, full_path_provided, split_on_parameter, default_connection, default_file_list_name, splitting_parameter = getExecuteConfig()
inputFileList = ""


fFlagUnset = False
for i in range(0, len(sys.argv)):
    if(sys.argv[i] == "-f"):
        inputFileList = sys.argv[i+1]
        fFlagUnset = True
        break
if(fFlagUnset == False):
    inputFileList = default_file_list_name

cFlagUnset = False
for i in range(0, len(sys.argv)):
    if(sys.argv[i] == "-c"):
        connectionName = sys.argv[i+1]
        cFlagUnset = True
        break

if(cFlagUnset == False):
    connectionName = default_connection

if(len(inputFileList) > 0):
    print("-----------------------------------------------------------------------------")
    print("Reading files from", inputFileList)


# Get execution configurations parameters
# sso_login, continue_on_failure, variable_substitution, show_errors_on_console, append_master_csv_log = checkConfigCondition = getExecuteConfig()

# Check connection type
if(sso_login.strip().upper() == 'TRUE'):
    # Create a connection
    cursor_target = makeSSOConnection(connectionName)
    print("Snowflake SSO Connection Established :", connectionName)
else:
    # Create a connection
    cursor_target = makeSnowflakeConnection(connectionName)
    print("Snowflake Connection Established (Non-SSO) :", connectionName)
