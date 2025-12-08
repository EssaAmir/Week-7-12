# Week 7: Secure Authentication System

**Student Name:** Essa Amir
**Student ID:** M01096017
**Course:** CST1510 - CW2 - Multi-Domain Intelligence Platform

## Project Description
A command-line authentication system implementing secure password hashing using bcrypt. This system allows users to register accounts and log in with proper password security practices.

## Features
* Secure password hashing using bcrypt with automatic salt generation
* User registration with duplicate username prevention
* User login with password verification
* Input validation for usernames and passwords
* File-based user data persistence

## Technical Implementation
* **Hashing Algorithm:** bcrypt with automatic salting
* **Data Storage:** Plain text file (users.txt) with comma-separated values
* **Validation:** Username (3-20 alphanumeric characters), Password (min 6 chars)
