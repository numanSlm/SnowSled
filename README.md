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

1.  Place files to be executed into input folder (Preferred format: .sql)
2.  Store password on local machine and add it’s complete location in `password_location` option in **configExecution.properties**
3.  Enter your credentials and login parameters in **configConnection.properties**
4.  Before execution make sure **configExecution.properties** fields are set to either to TRUE or FALSE (Refer Config Fields)
5.  Add filenames to be executed in text file. eg: **executionFileNames.txt**  
    If the filenames are in different path enable `full_path_provided` option
6.  If `variable_substitution` is TRUE, Update **Mapping.csv** file with values
7.  Open Command prompt and navigate to extracted folder location
8.  To execute the utility once all steps are complete.  
    Type the below command on command prompt.
```
    python snowflakeExecutor.py -f executionFileNames.txt -c connectionName
```    

9.  You can also set `default_connection` & `default_file_list_name` in **configExecution.properties** and run the utility using the below command 
```
    python snowflakeExecutor.py
``` 

10.  Once the execution is complete find result & logs code in **output** folder
