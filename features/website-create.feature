Feature: Create websites with redirects.
    Users should be able to create websites and edit them.

    Scenario Outline: We can create a website entry.
        Given we are <start>
         Then we type "<domain>" into the input for the domain
          And we type "<input source>" into the input for the source
         When we click "Save Website"
         Then we see a website for <website domain>
          And the website's domain is "<website domain>"
          And the website's source is "<website source>"
          And the website's owner is "<owner>"

Examples: Anonymous creates a website
    | start             | domain    | input source | website domain      | website source     | owner      |
    | on the index page | my-page   | 172.16.0.22  | my-page.example.com | http://172.16.0.22 | 🔓anonymous |

Examples: User creates a subdomain website
    | start              | domain    | input source              | website domain        | website source           | owner |
    | logged in as user  | user-page | https://172.16.0.23:4443  | user-page.example.com | https://172.16.0.23:4443 | user  |
    | logged in as admin | a         | 172.16.0.23:8000          | a.example.com         | http://172.16.0.23:8000  | admin |

Examples: A user creates a website with a fqdn
    | start              | domain        | input source | website domain | website source      | owner |
    | logged in as user2 | x.example.com | 172.16.3.3   | x.example.com  | http://172.16.3.3   | user2 |
    | logged in as admin | a.test        | 172.16.0.100 | a.test         | http://172.16.0.100 | admin |
