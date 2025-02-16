# APZ-hm1

---

### Description

Based on the description of the task to be performed, three microservices were implemented:

- **facade service**:
    - sends a `POST` request to the logging service to save messages with unique ids;
    - sends a `GET` request to the logging service to get all saved messages and a static text from the messages service; 

- **logging service**:
    - receives a `POST` request from the facade service to store messages;
    - stores received messages in a local hash table, where the key is a unique identifier (UUID) and the value is the message itself;
    - outputs each received message to the console;
    - handles `GET` requests by returning all stored messages (without UUIDs) as a concatenated string.

- **messages-service**:
    - handles `GET` requests by returning a static message, such as `"not implemented yet"`.
    - returns HTTP status code 405 Method Not Allowed for any POST request, as it does not support message storage.


---


### Get started

Need to run three dockers for three servers:

```shell
docker build -f .\Dockerfile.facade -t app1 .
```

```shell 
docker run -d -p 5001:5001 app1
```

Need to repeat this two more times for the other two services:

1. **facade service**: port `5001` (app1)
2. **logging service**: port `5002` (app2)
3. **messages service**: port `5003` (app3)

---

### Making requests:

`POST` request:

```shell
Invoke-WebRequest -Uri "http://127.0.0.1:5001/send_to_logging_service" -Method Post -Headers @{ "Content-Type" = "application/json" } -Body '{"msg": "Testing"}'
```

<br>

`GET` request:

```shell
Invoke-WebRequest -Uri "http://127.0.0.1:5001/get_resulted_messages" -Method Get -Headers @{ "Content-Type" = "application/json" }
```



