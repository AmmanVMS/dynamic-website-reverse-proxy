Feature: View the main page
    In order to see which configuration is already there, I would like to see
    the front page filled with some redirects.

    Scenario: the title
        Given we are on the index page
         Then we see the title "Dynamic Website Configuration" 
         Then we see a heading "Dynamic Website Configuration"

    Scenario: a test.example.org entry
        Given we are on the index page
         Then we see a website for test.example.org
          And the website's domain is "test.example.org"
          And the website's source is "http://172.16.0.1"
          And the website's owner is "🔒system"
