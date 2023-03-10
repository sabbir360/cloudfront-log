import csv
import time

from config import *
from model import CFLogs

start_time = time.time()

LOG_FILE = f"logs/{LOG_FILE}"
GENERATED_FILTER_FILE = f"filter/{GENERATED_FILTER_FILE}"

if EXPORT_DB:
    CFLogs.create_table()

log_file = open(LOG_FILE, 'r')
Lines = log_file.readlines()

# Strips the newline character
"""
2023-01-18	00:59:27	ORD58-P7	18554	66.249.73.97	GET	xxxx.cloudfront.net	/url/endpoint/goes/here	404	-	Mozilla/5.0%20(Linux;%20Android%206.0.1;%20Nexus%205X%20Build/MMB29P)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/109.0.5414.74%20Mobile%20Safari/537.36%20(compatible;%20Googlebot/2.1;%20+http://www.google.com/bot.html)	-	-	Error	UDwWsqcn3fqJwSHuHgdlNSyc9jSs2bxi--ym-pS62mhdpa0-CjYNvw==	www.xxxx.com	https	529	0.129	-	TLSv1.3	TLS_AES_128_GCM_SHA256	Error	HTTP/1.1	-	-	62793	0.125	Error	text/html;%20charset=utf-8	-	-	-
0           1           2           3 size    4 client ip   5   url  6                              7                                     8  9  10                                                                                                                                                                                                                                       11 12  13      14                                                          15 domain           16      17  time 18  19  20     21                        22    23          24  25    26
"""
csv_header = []
csv_contents = []

# header for CSV
for k, _ in {
    "date": 1,
    "time": 2,
    "size": 3,
    "client_ip": 4,
    "host": 5,
    "endpoint": 6,
    "status": 7,
    "user_agent": 8,
    "response_time": 9
}.items():
    csv_header.append(k)

# filter for endpoint
discard_list = [".js", ".css", ".gif", ".json", ".bmp", ".exe", ".git", "/static/", ".ico", ".png", ".php", ".sql", ".zip", ".tar", ".txt"]
discard_count = 0
line_count = 0

file_name_for_generate = GENERATED_FILTER_FILE

with open(f'{file_name_for_generate}.csv', 'w', newline='') as file:

    writer = csv.writer(file)
    writer.writerow(csv_header)

    for line in Lines:
        try:
            line_count += 1
            # date time ignore
            request_items = line.split("\t")
            # print(f"Processing line {row_count}")

            request_row = {
                "date": request_items[0],
                "time": request_items[1],
                "size": request_items[3],
                "client_ip": request_items[4],
                "host": request_items[15],
                "endpoint": request_items[7],
                "status": request_items[8],
                "user_agent": request_items[10],
                "response_time": request_items[18]
            }
            # print(f"{line.strip()}")
            # if any(item == request_row["endpoint"] for item in ["/static/", ".ico", ".png", ".php"]):
            if not any(substring in request_row["endpoint"] for substring in discard_list):
                csv_content = []
                for _, v in request_row.items():
                    csv_content.append(v)
                if EXPORT_CSV:
                    writer.writerow(csv_content)
                if EXPORT_LOG:
                    csv_contents.append(line)
                if EXPORT_DB:
                    CFLogs.insert(log_date=request_row["date"],
                                  log_time=request_row["time"],
                                  size=request_row["size"],
                                  client_ip=request_row["client_ip"],
                                  host=request_row["host"],
                                  uri=request_row["endpoint"],
                                  status=request_row["status"],
                                  user_agent=request_row["user_agent"],
                                  response_time=request_row["response_time"],
                                  ).execute()
            else:
                discard_count += 1
        except IndexError:
            print(f"Ignoring unformatted line --> {line}")
            discard_count += 1

# writing to file
if EXPORT_LOG:
    filtered_log_file = open(f'{file_name_for_generate}.log', 'w')
    filtered_log_file.writelines(csv_contents)
    filtered_log_file.close()

print(f"Total lines {line_count}")
print(f"Total discarded lines {discard_count}")
print(f"Total lines after filtering {line_count-discard_count}")

end_time = time.time()
elapsed_time = end_time - start_time
print("Time elapsed: {:.2f} seconds".format(elapsed_time))
