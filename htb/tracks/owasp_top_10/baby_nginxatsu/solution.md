
Using whatweb tool we identify that it is a nginx website, so we can maybe mount the generate nginx configuration in the website itself.

WhatWeb:

http://134.122.104.208:32557/ [302 Found] Cookies[XSRF-TOKEN,laravel_session], Country[UNITED STATES][US], HTML5, HTTPServer[nginx], HttpOnly[laravel_session], IP[134.122.104.208], Laravel, Meta-Refresh-Redirect[http://134.122.104.208:32557/auth/login], PHP[7.4.12], RedirectLocation[http://134.122.104.208:32557/auth/login], Title[Redirecting to http://134.122.104.208:32557/auth/login], X-Powered-By[PHP/7.4.12], nginx
http://134.122.104.208:32557/auth/login [200 OK] Cookies[XSRF-TOKEN,laravel_session], Country[UNITED STATES][US], HTTPServer[nginx], HttpOnly[laravel_session], IP[134.122.104.208], Laravel, Meta-Author[makelarisjr, makelaris], PHP[7.4.12], PasswordField[password], Title[nginxatsu], X-Powered-By[PHP/7.4.12], nginx


First we create an account: admin@test.com/123

After generating a nginx config file we open http://134.122.104.208:32557/config/51

In the config we have a interesiting comment:
# We sure hope so that we don't spill any secrets
# within the open directory on /storage


In /storage we have all the configs files generated.
At http://134.122.104.208:32557/storage/ we found a strange file:

- http://134.122.104.208:32557/storage/v1_db_backup_1604123342.tar.gz
- It contains some emails:

emails:
nginxatsu-me0wth@makelarid.es
nginxatsu-giv@makelarid.es
nginxatsu-adm-01@makelarid.es
Giovann1nginxatsu-giv@makelarid.es

Lets open with sqlitebrowser.
We have three users, their api tokens and their passwords ciphered.

Using https://www.dcode.fr/hash-function we find out that the passwords hash function are md5.
Then using the website https://md5hashing.net/hash/md5 we get one of the hash's adminadmin1 for the user nginxatsu-adm-01@makelarid.es

Using those credentials we get the flag
