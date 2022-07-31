# Solution

The webiste gives you this information: Command executed: ping -c 2 127.0.0.1
Adn the url is http://01.linux.challenges.ctf.thefewchosen.com:49580/index.php?host=127.0.0.1.

This seems like an easy RCE(Remote code execution), we had ?host=127.0.0.1|ls to the url and we could execute an ls command.
Using the "pipe" character we can pip various commands together. With the following command: |find / -name "*.txt" we get all the files that ended with .txt in their name and the flag is one for them.

Using |cat /flag.txt we get the flag.