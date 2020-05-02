# Microservices-Flask-Redis-Python

## These are the library, and tools that will need to be install in order to run the project 
```sh
Install Flask
$ pip3 install --user Flask-API python-dotenv
```
```sh
Install Request
$ pip3 install --user requests
```
```sh
Install Gunicorn3 & foreman 
$ sudo apt install --yes gunicorn3
$ sudo apt install --yes ruby-foreman

```
```sh
Install FeedGenerator
$ sudo apt update
$ sudo apt install --yes python3-lxml
$ pip3 install --user feedgen
```

### For Voting microservices part
```sh
Installing Redis
	$ sudo apt update
	$ sudo apt install --yes redis python3-hiredis

You can verify that Redis is up and running with:
	$ redis-cli ping
Server will respone: PONG

Installing the high-speed Python library for Redis
	$ sudo apt install --yes python3-hiredis

Install the Flask-And-Redis extension
	$ pip3 install --user Flask-and-Redis   

```

### To run project after install above:
```sh
In commandline, run: 

flask init
foreman start
```

## Current issue </br>
```sh
For this project, each microservices will be given a default port to ensure that all microservices will work properly all
	•Posting microservices: localhost:5000/post/posts/all 	
	•Voting microservices: localhost:5100/api/v1/resources/votes/all 
	•BFF microservices: localhost:5200/recent

```
# Rss feeds provided by the BFFF Microservices </br>
### The 25 most recent posts to any community  </br>
```sh
http://localhost:5200/recent
```
### The 25 most recent posts to a particular community  </br>
```sh
http://localhost:5200/<string>/<int> 
http://localhost:5200/school/25 

```
### Top 25 posts to any community, sorted by score </br>
```sh
http://localhost:5200/score 
```
### The top 25 posts to a particular community, sorted by score</br>
```sh
http://localhost:5200/score/<string>
http://localhost:5200/score/school

```
### The hot 25 posts to any community, ranked using Reddit hot ranking algorithm</br>
```sh
http://localhost:5200/hot 
```

### Voting microservices part:
```sh
•	View all votes by postID: http://127.0.0.1:5000/votebypostid/<postID>
•	View all post: http://127.0.0.1:5000/
•	View 1 votes by vote id: http://127.0.0.1:5000/vote/<voteID>
•	Upvote a post: http://127.0.0.1:5000/post/<postID>/upvote
Have to input in json format. 
Example: {“postID”: 0}
•	Downvote a post: http://127.0.0.1:5000/post/<postID>/downvote
Have to input in json format. 
Example: {“postID”: 0}
•	List the n top-scoring posts to any community: http://127.0.0.1:5000/toppostscore/2
•	Given a list of post identifiers, return the list sorted by score: http://127.0.0.1:5000/listsortedbyscore
Have to input a list: Example: [0, 2]

```