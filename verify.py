from main import *
from pprint import pprint
from tabulate import tabulate


query = "SELECT * FROM user_logins;"
query_headers = "SELECT column_name FROM information_schema.columns WHERE table_name = 'user_logins';"

results = db_execute_statement(query)
headers = db_execute_statement(query_headers)
headers = [head[0] for head in headers]
print(headers)
print(tabulate(results, headers=headers, tablefmt='fancy_grid'))
