Feature: View the page
    In order to see which configuration is already there, I would like to see
    the front page filled with some redirects.

    Scenario: test.example.org
        Given we are on the index page
         Then we see a website for test.example.org
#          And it is served by http://172.16.0.1
#          And it is owned by system

