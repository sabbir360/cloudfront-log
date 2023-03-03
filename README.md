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
 - For configuring export please be noted below:
     ```python
        # For generate output
        EXPORT_LOG = False  # For exporting .log file as same as CloudFront # High Memory
        EXPORT_CSV = True  # Export CSV with field specified on script
        # Database config is required
        EXPORT_DB = False    # This will store log to database for field specified on CSV Export.

        # MYSQL (Only supported for now)
        DB_HOST = "127.0.0.1"
        DB_NAME = "cf_logs"
        DB_USER = "root"
        DB_PASS = "admin"
     ```
 - Install required packages using `pip install -r requirements.txt`
 - Run `python main.py`

 ## Tips for MySQL

If you want to export the CSV directly to your mysql DB do the followings (As insert using python can take immersive time)

- Create database and run below schema
```sql
CREATE TABLE `cflogs` (
  `id` INT AUTO_INCREMENT NOT NULL,
  `date` DATE NOT NULL,
  `time` TIME NOT NULL,
  `size` INT NOT NULL,
  `client_ip` VARCHAR(15) NOT NULL,
  `host` VARCHAR(100) NOT NULL,
  `endpoint` VARCHAR(250) NOT NULL,
  `status` INT NOT NULL,
  `user_agent` TEXT NOT NULL,
  `response_time` FLOAT NOT NULL,
  CONSTRAINT `PRIMARY` PRIMARY KEY (`id`)
);
CREATE INDEX `index_date`
ON `cflogs` (
  `date` ASC
);
CREATE INDEX `index_ep`
ON `cflogs` (
  `endpoint` ASC
);
CREATE INDEX `index_host`
ON `cflogs` (
  `host` ASC
);
CREATE INDEX `index_rst`
ON `cflogs` (
  `response_time` ASC
);
CREATE INDEX `index_status`
ON `cflogs` (
  `status` ASC
);
CREATE INDEX `index_time`
ON `cflogs` (
  `time` ASC
);
```

- Then keep your CSV to `/var/lib/mysql-files/` as MySQL by default only allow secured location.
- Logon to MySQL console `mysql -uuser -ppassword db_name`
- Run this
```sql
LOAD DATA INFILE '/var/lib/mysql-files/your_file.csv' INTO TABLE cflogs FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS (date, time, size, client_ip, host, endpoint, status, user_agent, response_time);
```
