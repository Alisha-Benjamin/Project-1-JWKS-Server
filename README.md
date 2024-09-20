Alisha Benjamin - anb0369 - alishabenjamin@my.unt.edu <br/>
CSCE 3550 - Foundations of Cyber Security <br/>
Project 1 - Basic JWKS Server <br/>
Language: python <br/>

//At the end of the project, you should have a functional JWKS server with a RESTful API that can serve public keys with expiry and unique kid to verify JWTs.
//The server should authenticate fake user requests, issue JWTs upon successful authentication, and handle the “expired” query parameter to issue JWTs signed with an expired key.

Run this program using : <br/>
python app.py <br/>

Test Client <br/>
Ensure you run the test client on a separate IDE or Terminal instance:<br/>
curl -X POST http://localhost:8080/auth <br/>
curl -X POST http://localhost:8080/auth?expired=true <br/>
