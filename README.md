### Webhooks Event Handler (Server)
A basic flask server to handle git webhook push event.  
The server does the following upon receiving a push notification:  
- pulls recent changes to working repository (local)
- runs a couple of tests (python tests in our case)
- sends a summary of the tests as email to contributors.

# Note  
For this current version, email is only sent upon failure of the tests


# Future (Intended) features
Find a way to show a check pass on github if tests are passing.
Prob, use a link that point to an endpoint of the server. If there
is no failing tests, it will return a green svg icon as a response 
indicating a pass and returns a red svg icon otherwise.