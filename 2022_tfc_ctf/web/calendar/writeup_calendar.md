# Solution

Giving a quick look at the website and trying to understand how the website works, we notice the wordpress stuff that the site contains.
Running the tool wpscan against the website we got an hit saying that the plugin Modern Events Calendar version is vulnerable.
Searching a little bit for the exploit we found it in the metapsploit database: [Exploit](https://www.exploit-db.com/exploits/50084).
(Note: the exploit is the file 50084.py inside this directory, I change it a little bit to run it against the website).

With that we found the password for the admin user and the flag is TFCTF{PASSWORD_HERE}