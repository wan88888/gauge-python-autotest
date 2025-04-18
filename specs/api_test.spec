# API Testing with JSONPlaceholder

This specification demonstrates API testing with JSONPlaceholder.

## Get Posts

* I send a GET request to "/posts"
* The response status code should be "200"
* The response should contain a list of posts

## Get Single Post

* I send a GET request to "/posts/1"
* The response status code should be "200"
* The response should contain a single post with ID "1"

## Create a Post

* I send a POST request to "/posts" with the following data:
    |Key    |Value              |
    |-------|-------------------|
    |title  |Test Post          |
    |body   |This is a test post|
    |userId |1                  |
* The response status code should be "201"
* The response should contain the created post
* The response should contain the field "id"

## Update a Post

* I send a PUT request to "/posts/1" with the following data:
    |Key    |Value                  |
    |-------|----------------------|
    |title  |Updated Test Post     |
    |body   |This is an updated post|
    |userId |1                     |
* The response status code should be "200"
* The response should contain the updated post
* The response should contain the field "title" with value "Updated Test Post"

## Delete a Post

* I send a DELETE request to "/posts/1"
* The response status code should be "200" 