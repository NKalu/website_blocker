from datetime import datetime as dt
from datetime import timedelta as td
import time
import os

class WebsiteBlocker():
    def __init__(self):
        if os.name == 'nt':
            self.host_path = "C:\Windows\System32\drivers\etc\hosts"
        else:
            self.host_path = "/etc/hosts"
        self.redirect_path = "127.0.0.1"
        self.sites_to_be_blocked = []



    def website_list(self):
        sites = input("Please input the site you would like to block separated by commas: \n")

        initial_list = sites.split(",")

        for x in initial_list:
            if x.startswith("www"):
                self.sites_to_be_blocked.append(x)
                self.sites_to_be_blocked.append(x.strip("www."))
            else:
                self.sites_to_be_blocked.append(x)
                self.sites_to_be_blocked.append("www.%s" % x)


    def time_to_be_blocked(self):
        time_units = ["hours", "minutes", "seconds"]
        time_blocked = input("How long would you like to block these websites in "
                             "hours, minutes and seconds(ex. 2 hours 3 minutes and 30 seconds)?: \n")


        if  any(x in time_blocked.lower() for x in time_units):
            time_blocked = [int(x) for x in time_blocked.split() if x.isdigit()]
        else:
            print("Please include hours, minutes and seconds in your answer")
            self.time_to_be_blocked()

        return time_blocked


    def add_to_host(self, file_content, list_of_websites, host_file):
        for website in list_of_websites:
            if website in file_content:
                pass
            else:
                host_file.write(self.redirect_path + ' ' + website + '\n')


    def del_from_host(self, file_content, list_of_websites):
        content = file_content.readlines()
        file_content.seek(0)
        for line in content:
            if not any(website in line for website in list_of_websites):
                file_content.write(line)
        file_content.truncate()

wb = WebsiteBlocker()
wb.website_list()
list_of_websites = wb.sites_to_be_blocked
time_blocked = wb.time_to_be_blocked()


start_time = dt.now()
end_time = start_time + td(hours=time_blocked[0], minutes=time_blocked[1], seconds=time_blocked[2])

while start_time < end_time:
    print("Blocking sites...")

    with open(wb.host_path, 'r+') as host:
        content = host.read()
        wb.add_to_host(content, list_of_websites, host)
    start_time = dt.now()
    time.sleep(5)

with open(wb.host_path, 'r+') as host:
    wb.del_from_host(host, list_of_websites)