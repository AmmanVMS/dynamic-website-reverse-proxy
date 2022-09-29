Feature: Edit already existing websites.
    Users should be able to edit websites they created and not those of other people.

    Scenario Outline: A user can not edit the website of another user.
        Given <other user>'s website <domain> is served by http://172.16.0.99
          And we are <start>
         Then we type "<domain>" into the input for the domain
          And we type "http://172.16.0.100" into the input for the source
         When we click "Save Website"
         Then we see a website for <domain>
          And the website's domain is "<domain>"
          And the website's source is "http://172.16.0.99"
          And the website's owner is "<other user>"
          And we see a website notice "<message>"

Examples: Anonymous edits the website
    | start             | domain            | other user | message                                             |
    | on the index page | edit1.example.com | admin      | anonymous cannot edit subdomain owned by admin      |
    | on the index page | edit2.example.com | user       | anonymous cannot edit subdomain owned by other user |

Examples: A user edits the website
    | start             | domain            | other user | message                                        |
    | logged in as user | edit3.example.com | admin      | user cannot edit subdomain owned by admin      |
    | logged in as user | edit4.example.com | user2      | user cannot edit subdomain owned by other user |

    Scenario Outline: The website created by system cannot be edited by anyone.
        Given we are <start>
         Then we type "test.example.org" into the input for the domain
          And we type "http://172.16.0.100" into the input for the source
         When we click "Save Website"
         Then we see a website for test.example.org
          And the website's domain is "test.example.org"
          And the website's source is "http://172.16.0.1"
          And the website's owner is "🔒system"
          And we see a website notice "<message>"

Examples: Different users.
    | start              | message                                    |
    | on the index page  | anonymous cannot edit fqdn owned by system |
    | logged in as user  | user cannot edit fqdn owned by system      |
    | logged in as admin | admin cannot edit fqdn owned by system     |
    