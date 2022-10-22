# Writeup

If we try to create a user with the name "admin" we get the result: "this user already exists"
Lets create a user "test", we get session  eyJ1c2VybmFtZSI6InRlc3QifQ%3D%3D
Lets create a user "abc", we get session   eyJ1c2VybmFtZSI6ImFiYyJ9
Lets create a user "adm1n", we get session 

admin2 = eyJ1c2VybmFtZSI6ImFkbWluMiJ9


We notice similarity in the session IDS. THe objective here is to login or get a session as username admin.
The users closer to this are admim, adm1n and admin1. So we retrieve the session ID:

admin1 = eyJ1c2VybmFtZSI6ImFkbWluMSJ9
admim =  eyJ1c2VybmFtZSI6ImFkbWltIn0%3D
adm1n =  eyJ1c2VybmFtZSI6ImFkbTFuIn0%3D

To build the admin cookie we retireve parts of the cookies up there

THe init from admin1: eyJ1c2VybmFtZSI6ImFkbWl
The final from admim and adm1n: In0%3D

eyJ1c2VybmFtZSI6ImFkbWl<?>In0%3D

As we can see both in the first and last usernames that end with "n" the final character is a "u" so the admin cookie is:

admin =  eyJ1c2VybmFtZSI6ImFkbWluIn0%3D

