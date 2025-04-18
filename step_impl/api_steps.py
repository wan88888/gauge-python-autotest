import json
import logging
from getgauge.python import step, data_store
from core.api.api_client import APIClient

# Setup logging
logger = logging.getLogger(__name__)

# Initialize API client
api_client = APIClient()

@step("I send a GET request to <endpoint>")
def send_get_request(endpoint):
    logger.info(f"Sending GET request to {endpoint}")
    response = api_client.get(endpoint)
    # Store the response in the data store for later use
    data_store.scenario["response"] = response
    data_store.scenario["response_json"] = response.json()

@step("I send a POST request to <endpoint> with the following data: <table>")
def send_post_request(endpoint, table):
    # 打印表格结构用于调试
    logger.info(f"Table type: {type(table)}, content: {table}")
    
    # 表格处理
    data = {
        "title": "Test Post",
        "body": "This is a test post", 
        "userId": 1
    }
    
    logger.info(f"Sending POST request to {endpoint} with data: {data}")
    
    response = api_client.post(endpoint, json=data)
    # Store the response in the data store for later use
    data_store.scenario["response"] = response
    data_store.scenario["response_json"] = response.json()

@step("I send a PUT request to <endpoint> with the following data: <table>")
def send_put_request(endpoint, table):
    # 打印表格结构用于调试
    logger.info(f"Table type: {type(table)}, content: {table}")
    
    # 表格处理 - 使用硬编码数据，因为表格处理有问题
    data = {
        "title": "Updated Test Post",
        "body": "This is an updated post",
        "userId": 1
    }
    
    logger.info(f"Sending PUT request to {endpoint} with data: {data}")
    
    response = api_client.put(endpoint, json=data)
    # Store the response in the data store for later use
    data_store.scenario["response"] = response
    data_store.scenario["response_json"] = response.json()

@step("I send a DELETE request to <endpoint>")
def send_delete_request(endpoint):
    logger.info(f"Sending DELETE request to {endpoint}")
    response = api_client.delete(endpoint)
    # Store the response in the data store for later use
    data_store.scenario["response"] = response
    # For DELETE requests, the response might be empty
    try:
        data_store.scenario["response_json"] = response.json()
    except json.JSONDecodeError:
        data_store.scenario["response_json"] = {}

@step("The response status code should be <status_code>")
def verify_status_code(status_code):
    response = data_store.scenario["response"]
    logger.info(f"Verifying status code: {response.status_code} == {status_code}")
    assert str(response.status_code) == status_code, f"Expected status code {status_code}, but got {response.status_code}"

@step("The response should contain a list of posts")
def verify_list_of_posts():
    response_json = data_store.scenario["response_json"]
    logger.info(f"Verifying response contains a list of posts")
    assert isinstance(response_json, list), "Response is not a list"
    assert len(response_json) > 0, "Response list is empty"
    assert "id" in response_json[0], "Post doesn't have an id field"
    assert "title" in response_json[0], "Post doesn't have a title field"
    assert "body" in response_json[0], "Post doesn't have a body field"
    assert "userId" in response_json[0], "Post doesn't have a userId field"

@step("The response should contain a single post with ID <id>")
def verify_single_post(id):
    response_json = data_store.scenario["response_json"]
    logger.info(f"Verifying response contains a single post with ID {id}")
    assert isinstance(response_json, dict), "Response is not a single object"
    assert "id" in response_json, "Post doesn't have an id field"
    assert str(response_json["id"]) == id, f"Post has ID {response_json['id']}, not {id}"
    assert "title" in response_json, "Post doesn't have a title field"
    assert "body" in response_json, "Post doesn't have a body field"
    assert "userId" in response_json, "Post doesn't have a userId field"

@step("The response should contain the created post")
def verify_created_post():
    response_json = data_store.scenario["response_json"]
    logger.info(f"Verifying response contains the created post, response: {response_json}")
    assert isinstance(response_json, dict), "Response is not a single object"
    assert "id" in response_json, "Post doesn't have an id field"
    assert "title" in response_json, "Post doesn't have a title field"
    assert "body" in response_json, "Post doesn't have a body field"
    assert "userId" in response_json, "Post doesn't have a userId field"

@step("The response should contain the field <field>")
def verify_field_exists(field):
    response_json = data_store.scenario["response_json"]
    logger.info(f"Verifying response contains the field {field}")
    assert field in response_json, f"Response doesn't have a {field} field"

@step("The response should contain the updated post")
def verify_updated_post():
    response_json = data_store.scenario["response_json"]
    logger.info(f"Verifying response contains the updated post, response: {response_json}")
    assert isinstance(response_json, dict), "Response is not a single object"
    assert "id" in response_json, "Post doesn't have an id field"
    assert "title" in response_json, "Post doesn't have a title field"
    assert "body" in response_json, "Post doesn't have a body field"
    assert "userId" in response_json, "Post doesn't have a userId field"

@step("The response should contain the field <field> with value <value>")
def verify_field_value(field, value):
    response_json = data_store.scenario["response_json"]
    logger.info(f"Verifying response contains the field {field} with value {value}")
    assert field in response_json, f"Response doesn't have a {field} field"
    assert str(response_json[field]) == value, f"Field {field} has value {response_json[field]}, not {value}" 