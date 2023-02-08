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

# Initiate cursor
cs = cursor_target.cursor()

# Initiate Logger
for logger_name in ['snowflake.connector', 'botocore', 'boto3']:
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    # Change Logger File if needed
    ch = logging.FileHandler('./Output/LoggerDEBUG.log')
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(SecretDetector(
        '%(asctime)s - %(threadName)s %(filename)s:%(lineno)d - %(funcName)s() - %(levelname)s - %(message)s'))
    logger.addHandler(ch)

# Check Output Logging File Name
mode = 'w'
if(append_master_csv_log.strip().upper() == 'TRUE'):
    OutputLog = "MASTER_LOG.csv"
    mode = 'a'
else:
    value = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    OutputLog = str(value)+"_log.csv"
    mode = 'w'

# Read all execution file names
with open('./'+inputFileList, mode='r', encoding='utf-8-sig') as infile:
    reader = infile.read()
infile.close()

# List of all Files
executionFileNames = reader.split('\n')
executedTotal = 0
executionFailure = 0

dontAddHeader = False
try:
    with open('./output/'+OutputLog, mode='r', encoding='utf-8') as fd2:
        readFile = fd2.read()
        if(len(readFile.strip()) > 0):
            dontAddHeader = True
except:
    dontAddHeader = False
    

# Write into Output file
with open('./output/'+OutputLog, mode=mode, encoding='utf-8', newline='') as fd:
    writer = csv.writer(fd, delimiter=',')
    if(dontAddHeader == False):
        writer.writerow(["File,Name", "ObjectName", "Execution",
                         "Timestamp", "ErrorLog", "Failed_SFQID", "ExecutionTime(mins)"])

    # Iteragte through each file
    for fileName in executionFileNames:
        skipFile = False
        errorsInFile = 0
        if(fileName.startswith('#')):
            print("Skipped ", fileName)
            skipFile = True
        else:
            # add things here
            if(full_path_provided.strip().upper() == 'FALSE'):
                input_path = "./input/"+fileName
            else:
                input_path = fileName

            if(path.exists(input_path)):
                with open(input_path, mode='r', encoding='utf-8') as readfile:
                    # Read Data inside file
                    fileContent = readfile.read()

                # Split on each semicolon
                if(split_on_parameter.upper().strip() == "TRUE"):
                    sqlQueries = fileContent.split(splitting_parameter)
                else:
                    sqlQueries = []
                    sqlQueries.append(fileContent)
                print("-------------------------------------------")
                print("Executing ", fileName)

                # Used to check if error is generated
                error_flag = False
