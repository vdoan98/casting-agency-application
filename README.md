# Casting Agency Web Application

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

The application will:

1) Allow company employees to create accounts 
2) Allow company employees to perform actions based on role authorization

## Models:

Movies with attributes title and release date
Actors with attributes name, age and gender

## Endpoints:
- GET /actors and /movies
- DELETE /actors/ and /movies/
- POST /actors and /movies and
- PATCH /actors/ and /movies/

## Roles:
1. Casting Assistant
    - Can view actors and movies
2. Casting Director
    - All permissions a Casting Assistant has and…
    - Add or delete an actor from the database
    - Modify actors or movies
3. Executive Producer
    - All permissions a Casting Director has and…
    - Add or delete a movie from the database

## Tests:
- One test for success behavior of each endpoint
- One test for error behavior of each endpoint
- At least two tests of RBAC for each role

