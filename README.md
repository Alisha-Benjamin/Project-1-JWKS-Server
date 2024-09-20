Alisha Benjamin - anb0369 - alishabenjamin@my.unt.edu
CSCE 3550 - Foundations of Cyber Security
Project 1 - Basic JWKS Server
Language: python

//At the end of the project, you should have a functional JWKS server with a RESTful API that can serve public keys with expiry and unique kid to verify JWTs.
//The server should authenticate fake user requests, issue JWTs upon successful authentication, and handle the “expired” query parameter to issue JWTs signed with an expired key.

Run this program using :
python app.py

Test Client
Ensure you run the test client on a separate IDE or Terminal instance:
curl -X POST http://localhost:8080/auth
curl -X POST http://localhost:8080/auth?expired=true
