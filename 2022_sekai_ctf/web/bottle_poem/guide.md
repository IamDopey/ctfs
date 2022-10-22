## Bottle Poem


## Description 

Come and read poems in the bottle.

No bruteforcing is required to solve this challenge. Please do not use scanner tools. 
Rate limiting is applied. Flag is executable on server.

Author: bwjy


## Solution

It seems like it is passing the file name in the variable id which it means that it is a LFI(Local File Inclusion).
The file name is case sensitive and we can parse multiple commands with &&.

We can go to http://bottle-poem.ctf.sekai.team/show?id=/proc/self/cwd/app.py.
The directory /proc/self/cwd means the directory where the process is running the current working directory.
And like app.py is common name to use for the application sourcecode, browsing there we can see the source code.

Looking at the sourcecode we can see that we have another  endpoint "sign" and which sets a cookie.
We can see that we have a config.secret that is importing sekai and we can maybe try to find that file.

http://bottle-poem.ctf.sekai.team/show?id=/proc/self/cwd/config/secret.py

Content: sekai = "Se3333KKKKKKAAAAIIIIILLLLovVVVVV3333YYYYoooouuu"

Looking at the documentation we have two important functions, cookie_decode and cookie_encode.
I create a script to decode the cookie and encode it replacing "guest" for "admin".
When I update the cookie, I receive:  Hello, you are admin, but it’s useless. 

Since we can't do much maybe we can leverage this to create a RCE.
THis issue: https://github.com/bottlepy/bottle/issues/900 explains how an attacker can execute commands at 
the target machine by leveraging the problem in the bottle python library.

What I did was built a script to explore this vulnerability and execute commands, executing a reverse shell.
