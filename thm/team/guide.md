# Recon

## Nmap 


```
PORT   STATE SERVICE
21/tcp open  ftp
22/tcp open  ssh
80/tcp open  http

21/tcp open  ftp     vsftpd 3.0.3
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 79:5f:11:6a:85:c2:08:24:30:6c:d4:88:74:1b:79:4d (RSA)
|   256 af:7e:3f:7e:b4:86:58:83:f1:f6:a2:54:a6:9b:ba:ad (ECDSA)
|_  256 26:25:b0:7b:dc:3f:b2:94:37:12:5d:cd:06:98:c7:9f (ED25519)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-title: Team
|_http-server-header: Apache/2.4.29 (Ubuntu)

```

## Gobuster

```
gobuster dir -u http://team.thm -w ~/tools/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt
gobuster vhost -u http://team.thm -w ~/tools/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt
```

### team.thm

```
/images               (Status: 301) [Size: 305] [--> http://team.thm/images/]
/scripts              (Status: 301) [Size: 306] [--> http://team.thm/scripts/]
/assets               (Status: 301) [Size: 305] [--> http://team.thm/assets/] 
```

### dev.team.thm

```
http://dev.team.thm/script.php?page=teamshare.php
```


## Nikto

```
nikto -h http://dev.team.thm 
nikto -h http://team.thm 
```

We did not found anything with nikto in both subdomains/domains.


# Web

- We found "Apache2 Ubuntu Default Page: It works! If you see this add 'team.thm' to your hosts!" in the title
- We add the team.thm in our hosts and perform a vhost and directory bruteforce
- We found dev.team.thm with the gobuster
- team.thm seems like it does not have anything, it seems like it is only a frontend page with a template
- dev.team.thm in the other hand has file inclusion vulnerability
- http://dev.team.thm/script.php?page=/etc/passwd lets us see the contents of any file in the machine
- We have the following users:
```
dale:x:1000:1000:anon,,,:/home/dale:/bin/bash gyles:x:1001:1001::/home/gyles:/bin/bash ftpuser:x:1002:1002::/home/ftpuser:/bin/sh
```
- I tried to see if I can perform a log poisoning but we didnt have permissions to read those files.

- we have an ftpuser that may be used in the ftp service(we can try to bruteforce him)
- I tried use the ftpuser without password but it gives login failed
- I tried to bruteforce the ftpuser using rockyou but does not work

- Since i cant get nothing from the vulnerability i found i need to start searching for something in te endpoints of team.thm domain.
- I started enumerating the endpoints we got in team.thm
```
gobuster dir -u http://team.thm/scripts -w ~/tools/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt  --extensions .txt,.py,.php,.sh
gobuster dir -u http://team.thm/assets -w ~/tools/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt
gobuster dir -u http://team.thm/images -w ~/tools/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt
```

```
/css                  (Status: 301) [Size: 309] [--> http://team.thm/assets/css/]
/js                   (Status: 301) [Size: 308] [--> http://team.thm/assets/js/] 
/fonts                (Status: 301) [Size: 311] [--> http://team.thm/assets/fonts/]
/thumbs               (Status: 301) [Size: 312] [--> http://team.thm/images/thumbs/]
/script.txt           (Status: 200) [Size: 597] //We found a weird file in /scripts/
```

- With the file scripts.txt that we found it gives us some information about how the ftp is configured but it leads nowhere since we cant change the file to execute. 
- But we have an information that seems weird:
``` 
 Note to self had to change the extension of the old "script" in this folder, as it has creds in
```
- Searching in google for old extension we found that is normal that the systems create a .old for older files after the default file extension
- In this case it seems like we may have a scripts.old
- We download a file that its the same for scripts.txt but with the username and password.
- username and password for the ftp: ftpuser : T3@m$h@r3
- we have a /workshare directory and inside we have another file called New_site.txt
```
Also as per the team policy please make a copy of your "id_rsa" and place this in the relevent config file.
```
- Using ffuf we get to the configuration that gyles was talking
- fuf -w ~/tools/seclists/Fuzzing/LFI/LFI-gracefulsecurity-linux.txt -u http://dev.team.thm/script.php?page=FUZZ 1>fuzzing.txt
- filtering for ssh we found an sshd_config file that has the dale openssh private key
- We can that we can inject shell code in the script that we can interact with: /home/gyles/admin_checks
- We notice that we can inject code in two inputs, name and error, but only error is directly executed.
- So we can do /bin/bash and then create a interactive shell: python3 -c "import pty; pty.spawn('/bin/bash')"
- We get a shell as gyles
- Run linpeas:
 - /usr/local/bin/main_backup.sh                                                                                                                                                     
 - /opt/admin_stuff
- Looking at the admin_stuff we have a script that executes main_backup.sh every minute as root
- Looking at the permissions for the main_backups.sh we notice that members from the admin group can edit this file, and gyles is one of them
- So we add a python reverse shell and start netcat. After sometime we got a reverse shell as root, GG!
