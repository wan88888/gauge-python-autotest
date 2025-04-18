# Web Testing with The Internet

This specification demonstrates web testing with The Internet login page.

## Successful Login

* I open the login page
* I enter username "tomsmith"
* I enter password "SuperSecretPassword!"
* I click the login button
* I should be successfully logged in
* The secure area page should be displayed

## Failed Login with Invalid Username

* I open the login page
* I enter username "invalid"
* I enter password "SuperSecretPassword!"
* I click the login button
* I should see an error message
* The error message should contain "Your username is invalid!"

## Failed Login with Invalid Password

* I open the login page
* I enter username "tomsmith"
* I enter password "invalid"
* I click the login button
* I should see an error message
* The error message should contain "Your password is invalid!"

## Logout from Secure Area

* I open the login page
* I enter username "tomsmith"
* I enter password "SuperSecretPassword!"
* I click the login button
* I should be successfully logged in
* I click the logout button
* I should be logged out
* The login page should be displayed 