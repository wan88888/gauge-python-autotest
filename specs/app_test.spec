# Mobile App Testing with SauceLabs Sample App

This specification demonstrates mobile app testing with SauceLabs Sample App.

## Successful Login on Android

Tags: android

* I launch the Android app
* I enter mobile username "standard_user"
* I enter mobile password "secret_sauce"
* I click the mobile login button
* I should be successfully logged into the mobile app
* The mobile home page should be displayed

## Failed Login on Android with Invalid Username

Tags: android

* I launch the Android app
* I enter mobile username "invalid_user"
* I enter mobile password "secret_sauce"
* I click the mobile login button
* I should see a mobile error message
* The mobile error message should contain "Username and password do not match any user"

## Failed Login on Android with Invalid Password

Tags: android

* I launch the Android app
* I enter mobile username "standard_user"
* I enter mobile password "invalid_password"
* I click the mobile login button
* I should see a mobile error message
* The mobile error message should contain "Username and password do not match any user"

## Successful Login on iOS

Tags: ios

* I launch the iOS app
* I enter mobile username "standard_user"
* I enter mobile password "secret_sauce"
* I click the mobile login button
* I should be successfully logged into the mobile app
* The mobile home page should be displayed

## Failed Login on iOS with Invalid Username

Tags: ios

* I launch the iOS app
* I enter mobile username "invalid_user"
* I enter mobile password "secret_sauce"
* I click the mobile login button
* I should see a mobile error message
* The mobile error message should contain "Username and password do not match any user"

## Failed Login on iOS with Invalid Password

Tags: ios

* I launch the iOS app
* I enter mobile username "standard_user"
* I enter mobile password "invalid_password"
* I click the mobile login button
* I should see a mobile error message
* The mobile error message should contain "Username and password do not match any user" 