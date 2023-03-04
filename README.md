SnowSled
================================

> The aim of the tool is to execute DDL/DML on Snowflake using Python.

Installation
------------

*   Install Python ([Python 3.6.5](https://www.python.org/downloads/release/python-365/))
*   Install Required Dependencies  
    (logging,sqlparse,pandas,requests,snowflake-python-connector)

Steps to use the utility
------------------------

1.  Extract zip file. (PythonSnowflakeExecutorV1.0.0.zip)
2.  Place files to be executed into input folder (Preferred format: .sql)
3.  Store password on local machine and add it’s complete location in `password_location` option in **configExecution.properties**
4.  Enter your credentials and login parameters in **configConnection.properties**
5.  Before execution make sure **configExecution.properties** fields are set to either to TRUE or FALSE (Refer Config Fields)
6.  Add filenames to be executed in text file. eg: **executionFileNames.txt**  
    If the filenames are in different path enable `full_path_provided` option
7.  If `variable_substitution` is TRUE, Update **Mapping.csv** file with values
8.  Open Command prompt and navigate to extracted folder location
9.  To execute the utility once all steps are complete.  
    Type the below command on command prompt.

    python snowflakeExecutor.py -f executionFileNames.txt -c connectionName
    

10.  You can also set `default_connection` & `default_file_list_name` in **configExecution.properties** and run the utility using the below command

    python snowflakeExecutor.py
    

11.  Once the execution is complete find result & logs code in **output** folder
