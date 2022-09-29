Feature: Users should have it easy to copy the data in.
    Therefore, you should be able to edit the websites.

    Scenario: We edit a website.
        Given user2's website edit-pencil.example.com is served by http://172.16.0.99
         When we click "✎" in edit-pencil.example.com
         Then we see "edit-pencil.example.com" in the text input for the domain
          And we see "http://172.16.0.99" in the text input for the source
