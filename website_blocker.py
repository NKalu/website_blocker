from datetime import datetime as dt
from datetime import timedelta as td
import time
import os

host_paths = ["C:\Windows\System32\drivers\etc\hosts","/etc/hosts"]
redirect_path = "127.0.0.1"

def website_list():
    list_of_sites = []
    sites = input("Please input the site you would like to block separated by commas: \n")

    initial_list = sites.split(",")

    for x in initial_list:
        if x.startswith("www"):
            list_of_sites.append(x)
            list_of_sites.append(x.strip("www."))
        else:
            list_of_sites.append(x)
            list_of_sites.append("www.%s" % x)

    return list_of_sites


def time_to_be_blocked():
    time_units = ["hours", "minutes", "seconds"]
    time_blocked = input("How long would you like to block these websites in "
                         "hours, minutes and seconds(ex. 2 hours 3 minutes and 30 seconds)?: \n")


    if  any(x in time_blocked.lower() for x in time_units):
        time_blocked = [int(x) for x in time_blocked.split() if x.isdigit()]
    else:
        print("Please include hours, minutes and seconds in your answer")
        time_to_be_blocked()

    return time_blocked


def add_to_host(file_content, list_of_websites, host_file):
    for website in list_of_websites:
        if website in file_content:
            pass
        else:
            host_file.write(redirect_path + ' ' + website + '\n')


def del_from_host(file_content, list_of_websites):
    file_content.seek(0)
    for line in file_content:
        if not any(website in line for website in list_of_websites):
            file_content.write(line)
    file_content.truncate()


list_of_websites = website_list()

time_blocked = time_to_be_blocked()

start_time = dt.now()
end_time = start_time + td(hours=time_blocked[0], minutes=time_blocked[1], seconds=time_blocked[2])

while start_time < end_time:
    time.sleep(5)
    print("Blocking sites...")
    if os.name == 'nt':
        with open(host_paths[0], 'r+') as host:
            content = host.read()
            add_to_host(content, list_of_websites, host)
    else:
        with open(host_paths[1], 'r+') as host:
            content = host.read()
            add_to_host(content, list_of_websites, host)
    start_time = dt.now()


if os.name == 'nt':
    with open(host_paths[0], 'r+') as host:
        content = host.readlines()
        del_from_host(host, list_of_websites)
else:
    with open(host_paths[1], 'r+') as host:
        content = host.readlines()
        del_from_host(host, list_of_websites)