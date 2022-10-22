# Intro

We are presented with a website that seems to have a vulnerability in the deserialization, hint in the title "insecure deserialization".
The page shows rick with the following text "Don't play around with this serum morty!! <__main__.anti_pickle_serum object at 0x7f10a7239850>"
In the cookies tab we have a cookie with the name plan_b and the value:
KGRwMApTJ3NlcnVtJwpwMQpjY29weV9yZWcKX3JlY29uc3RydWN0b3IKcDIKKGNfX21haW5fXwphbnRpX3BpY2tsZV9zZXJ1bQpwMwpjX19idWlsdGluX18Kb2JqZWN0CnA0Ck50cDUKUnA2CnMu
Using cyber chef the following is base64 string and the plaintext is:
```
(dp0
S'serum'
p1
ccopy_reg
_reconstructor
p2
(c__main__
anti_pickle_serum
p3
c__builtin__
object
p4
Ntp5
Rp6
s.

```
```
whatweb http://161.35.46.205:31892/

http://161.35.46.205:31892/ [302 Found] Cookies[plan_b], Country[UNITED STATES][US], HTTPServer[Werkzeug/1.0.1 Python/2.7.17], IP[161.35.46.205], Python[2.7.17], RedirectLocation[http://161.35.46.205:31892/], Title[Redirecting...], Werkzeug[1.0.1]
```

# Vulnerbility

Look at the script in this directory.

# References

- https://davidhamann.de/2020/04/05/exploiting-python-pickle/
- https://docs.python.org/3/library/subprocess.html#subprocess.check_output
- https://www.simplilearn.com/tutorials/python-tutorial/subprocess-in-python
