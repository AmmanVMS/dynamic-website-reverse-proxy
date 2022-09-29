Feature: Edit already existing websites that you are not allowed to edit.
    Users should be able to edit their websites and those of anonymous.
    The Admin is allowed to edit the websites of all the users.

    Scenario Outline: A user edits the website again.
        Given we are <logged in>
         Then we type "<domain>" into the input for the domain
          And we type "http://172.16.0.99" into the input for the source
         When we click "Save Website"
         Then we type "<domain>" into the input for the domain
          And we type "http://172.16.0.100" into the input for the source
         When we click "Save Website"
         Then we see a website for <domain>
          And the website's domain is "<domain>"
          And the website's source is "http://172.16.0.100"
          And the website's owner is "<user>"
          And we see a website notice "Website <domain> saved."

Examples: Different users.
    | logged in          | domain             | user       |
    | on the index page  | works1.example.com | 🔓anonymous |
    | logged in as user2 | works2.example.com | user2      |
    | logged in as admin | works3.example.com | admin      |

    Scenario: A user edits the website of an anonymous user.
        Given we are on the index page
         Then we type "works4.example.com" into the input for the domain
          And we type "http://172.16.0.99" into the input for the source
         When we click "Save Website"
         When we log in as user2
         Then we type "works4.example.com" into the input for the domain
          And we type "http://172.16.0.100" into the input for the source
         When we click "Save Website"
         Then we see a website for works4.example.com
          And the website's domain is "works4.example.com"
          And the website's source is "http://172.16.0.100"
          And the website's owner is "user2"
          And we see a website notice "Website works4.example.com saved."

    Scenario: Administrators can edit websites of other users.
        Given user's website works5.example.com is served by http://172.16.0.99
         When we log in as admin
         Then we type "works5.example.com" into the input for the domain
          And we type "http://172.16.0.100" into the input for the source
         When we click "Save Website"
         Then we see a website for works5.example.com
          And the website's domain is "works5.example.com"
          And the website's source is "http://172.16.0.100"
          And the website's owner is "admin"
          And we see a website notice "Website works5.example.com saved."
