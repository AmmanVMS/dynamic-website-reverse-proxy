Feature: Log in on the main page
    In order for users to create websites, we want them to log in.

    Scenario: There are inputs to log in.
        Given we are on the index page
         Then we see a text input for the username
          And we see a password input for the password

    Scenario: The Administrator can log in.
        Given we are on the index page
         Then we type "admin" into the input for the username
          And we type "12345" into the input for the password
         When we click "Log In"
         Then we see a login notice "You are logged in as admin."
        
    Scenario: Anyone can log in if they do not have a website.
        Given we are on the index page
         Then we type "firsttimer" into the input for the username
          And we type "password" into the input for the password
          When we click "Log In"
         Then we see a login notice "You are logged in as firsttimer."
        
    Scenario: You can not log in with a wrong password.
        Given we are on the index page
         Then we type "admin" into the input for the username
          And we type "wrong password" into the input for the password
          When we click "Log In"
         Then we see a login notice "Invalid password. You are not logged in."

    Scenario: Check the user log in is possible.
        Given we are logged in as user
         Then we see a login notice "You are logged in as user."
        
    Scenario: Check the admin log in is possible.
        Given we are logged in as admin
         Then we see a login notice "You are logged in as admin."

    Scenario: You are not logged in by default.
        Given we are on the index page
         Then we see a login notice "You are not logged in."
