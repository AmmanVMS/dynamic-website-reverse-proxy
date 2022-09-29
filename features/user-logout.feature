Feature: Log out when you are logged in.
    In order for users to have the normal login/logout flow, it is nice to log them out again.

    Scenario Outline: When users log in, they can log out again.
        Given we are logged in as <username>
         Then we see a button "Log Out"
         When we click "Log Out"
         Then we see a login notice "You are not logged in."
          And we see a text input for the username
          And we see a password input for the password
          And we see a button "Log In"

Examples: User logins to use and test.
    | username |
    | admin    |
    | user     |
    | user2    |

    Scenario Outline: When users log in, they do not see the log-in button.
        Given we are logged in as <username>
         Then we do not see a button "Log In"
          And we do not see a text input for the username
          And we do not see a password input for the password

Examples: User logins to use and test.
    | username |
    | admin    |
    | user     |
    | user2    |
