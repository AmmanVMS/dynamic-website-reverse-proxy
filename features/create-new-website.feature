Feature: Create websites with redirects.
    Users should be able to create websites and edit them.

    Scenario Outline: We can create a website entry.
        Given we are <start>
         Then we type "<domain>" into the input for the domain
          And we type "<input source>" into the input for the source
          And we click "Save Website"
         Then we see a website for <website domain>
          And the website's domain is "<website domain>"
          And the website's source is "<website source>"
          And the website's owner is "<owner>"

Examples: Anonymous creates a website
    | start             | domain    | input source | website domain      | website source     | owner     |
    | on the index page | my-page   | 172.16.0.22  | my-page.example.org | http://172.16.0.22 | anonymoys |

Examples: User creates a subdomain website
    | start              | domain    | input source              | website domain        | website source           | owner |
    | logged in as user  | user-page | https://172.16.0.23:4443  | user-page.example.org | https://172.16.0.23:4443 | user  |
    | logged in as admin | a         | 172.16.0.23:8000          | a.example.org         | http://172.16.0.23:8000  | admin |

Examples: A user creates a website with a full domain
    | start              | domain    | input source | website domain | website source      | owner |
    | logged in as user2 | a.b.c     | 172.16.3.3   | a.b.c          | http://172.16.0.3   | user2 |
    | logged in as admin | a.test    | 172.16.0.100 | a.test         | http://172.16.0.100 | admin |
