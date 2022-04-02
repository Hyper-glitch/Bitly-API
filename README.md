# Bitly API

## Basic information

***Bitly API*** allows you to interact with **bitly.com** and create new bitlinks or count clicks by the old one.

## Running

You need to create **.env** file and set the <ins>following environmental variables</ins> *(for example see in .env file)*:

| Environmental         | Description                                           |
|-----------------------|-------------------------------------------------------|
| `GENERIC_ACCESS_TOKEN`| personal access token for authorization to Bitly API  |

This script runs a docker container with an application:
```bash
docker build -t bitly_app .
docker run -d --env-file .env bitly_app
```
