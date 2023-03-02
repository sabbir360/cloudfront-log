# CloudFront Log
This project takes input from CloudFront Logs and can filter and discard any unwanted info you want to skip. And generate a filtered **log** file and **csv** file separately.

Currently supported CSV file headers are (but customizable)
|date|time|size|client_ip|host|endpoint|status|user_agent|response_time|
|----|----|----|---------|----|--------|------|----------|-------------|
|date|time|size|client_ip|host|endpoint|status|user_agent|response_time|

## Prerequisites
 - Python 3.9+

 ## How to run this project
 - Rename `config.py.sample` to `config.py`.
 - Put your log file to `logs` directory and update the file name to `LOG_FILE` variable.
 - Do same for your desired final output file using `GENERATED_FILTER_FILE` variable.
 - Run `python main.py`
