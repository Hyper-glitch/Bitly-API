# Bitly API

## Basic information

***Bitly API*** allows you to interact with **bitly.com** and create new bitlinks or count clicks by the old one.

## Starting

You need to create **.env** file and set the <ins>following environmental variables</ins> *(for example see in .env file)*:

| Environmental         | Description                                           |
|-----------------------|-------------------------------------------------------|
| `GENERIC_ACCESS_TOKEN`| personal access token for authorization to Bitly API  |

This script builds and then runs a docker container with an application:
```bash
docker build -t bitly_app .
docker run -d --env-file .env bitly_app
```
## *Classical starting*

1. clone the repository:
```bash
git clone https://github.com/Hyper-glitch/bitly_api.git
```
2. Create **.env** file and set the <ins>environmental variables</ins> as described above.
3. Install dependencies:
```bash
pip install -r requirements.txt
```
