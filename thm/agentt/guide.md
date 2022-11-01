# Recon

## Nmap

```
PORT   STATE SERVICE
80/tcp open  http

80/tcp open  http    PHP cli server 5.5 or later (PHP 8.1.0-dev)
|_http-title:  Admin Dashboard
```

## Gobuster



## Nikto

+ Server: No banner retrieved
+ Retrieved x-powered-by header: PHP/8.1.0-dev
+ The anti-clickjacking X-Frame-Options header is not present.
+ The X-XSS-Protection header is not defined. This header can hint to the user agent to protect against some forms of XSS
+ The X-Content-Type-Options header is not set. This could allow the user agent to render the content of the site in a different fashion to the MIME type
+ No CGI Directories found (use '-C all' to force check all possible dirs)
+ OSVDB-44056: /sips/sipssys/users/a/admin/user: SIPS v0.2.2 allows user account info (including password) to be retrieved remotely.
+ OSVDB-3092: /demo/: This might be interesting...
+ OSVDB-18114: /reports/rwservlet?server=repserv+report=/tmp/hacker.rdf+destype=cache+desformat=PDF:  Oracle Reports rwservlet report Variable Arbitrary Report Executable Execution



# Web


- We find the user Douglas McGee as the admin.
- https://www.exploit-db.com/exploits/22381 - ?
- https://vulners.com/securityvulns/SECURITYVULNS:DOC:22105 - ?
- As we can see from nikto with have a non-standard responser header called: X-Powered-By: PHP/8.1.0-dev
- Search for the PHP/8.1.0-dev on google we get a RCE(Remote COde Execution) in this specific version of php where there is a backdoor that can be used
by passing commands through a request header called "User-Agentt". https://www.exploit-db.com/exploits/49933
- We get a shell as root by running the exploit in the exploit db page.
- find / -name flag* -type f 2>/dev/null
- cat /flag.txt
