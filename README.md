# ForceBrute - Brute force script for HTTP POST Forms

**ForceBrute** is a script that performs brute force attacks on HTTP POST-based login forms. It allows you to conduct brute force attacks using wordlists for different login and password combinations.

## Functionality

This script allows you to perform brute force attacks in three different ways:

1. **brute force on login** - When a login wordlist is provided.
2. **brute force on password** - When a password wordlist is provided.
3. **brute force on both login and password** - When wordlists for both login and password are provided.

## Requirements

- **requests**: To make HTTP POST requests.
- **numpy**: To split wordlists into smaller chunks.

## How to Use

You can run the script like this:

```bash
python forcebrute.py -u <URL> -lp <login_parameter> -pp <password_parameter> -L <login_list> -P <password_list> -rt <failed_response_text> -t <number_of_threads>```

| Parameter                  | Description                                                                                                      |
|----------------------------|------------------------------------------------------------------------------------------------------------------|
| `-u`/`--url`                | URL of the login form                                                                                             
| `-l`/`--login`              | Specific username for brute force |
| `-L`/`--LOGIN`              | Path to a login wordlist file                                                                     
| `-p`/`--password`           | Specific password for brute force |
| `-P`/`--PASSWORD`           | Path to a password wordlist file                                                                 
| `-rt`/`--response-text`     | Text indicating a failed login response (useful for error checking in the form)                                  
| `-rc`/`--response-code`     | HTTP response code for successful login (e.g., 302 for redirect)                                                  
| `-t`/`--threads`            | Number of threads to use for brute force (maximum 120, default 5)                                                     
| `-lp`/`--login-parameter`   | The login parameter name in the POST form                                                                         
| `-pp`/`--password-parameter`| The password parameter name in the POST form                                                                     
