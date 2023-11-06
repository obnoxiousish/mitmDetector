# mitmDetector
a poc mitm detection

# Info

```
The browser wont let you swap out window.location without redirecting
And since it's using a hash, a simple domain replace wont bypass this

However, someone could change the const currentURL to = their phishing domain
In a real implementation you'll want to use random variable names, and grab / attempt to hide where your using window.location.host 
Or as well use it many different places, and in many different files.

Someone could replace all "= windows.location.host" with "= '{theirPhishingDomain}'" so you will want to write some JS that'll break if this is done.

Ultimately if someone understands this is what is being done and how + where it can be bypassed

Also in production this would have to be salted with the users email and be submitted with the login/signup or etc request instead of seperately.
Otherwise it'll be bypassed easily.
```