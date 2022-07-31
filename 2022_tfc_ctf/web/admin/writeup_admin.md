# Solution

Looking at the files we notice that the user is classified as admin if he got the parameter "isAdmin" with the value of true.
What I did was, capture the request with burpsuite and in the json object that is sent with the username I sent another element, isAdmin, with the value true.
Like this

```
{
	"username": "hello",
	"isAdmin": True
}
```
And we got the flag since we create an admin and the if:
```
    if (user.isAdmin) {
      user.flag = process.env.FLAG!;
    }
```
became true.