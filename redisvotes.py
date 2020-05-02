#import the redis-py client package
import redis
import flask_api
from flask import request, Flask
from flask_api import status, exceptions
import pugsql
import datetime
import json

# define connection information for Redis
redis_host = "127.0.0.1"
redis_port = 6379
redis_password = ""

# vote configuration
redis_key = 'votes'
num_votes = 0

app = flask_api.FlaskAPI(__name__)
# # app.config.from_envvar('APP_CONFIG')

db1 = redis.StrictRedis(host=redis_host, port=redis_port, db = 0)
db2 = redis.StrictRedis(host=redis_host, port=redis_port, db = 1)

# Create custom Flask command to init Redis db
@app.cli.command("init")
def init_redis():
    print("Flask init success")

    # Empty the Redis list
    for i in range(0, db2.llen("votes")):
        db2.lpop("votes")
    
    myDB = raw_data()
    print("Successfully create Redis db")

# Home page
@app.route('/', methods=['GET'])
def home():
    return {"Welcome to Flask and Redis using":"Python"}, status.HTTP_200_OK

# view all votes by postID http://127.0.0.1:5000/votebypostid/0
@app.route('/votebypostid/<int:id>', methods=['GET'])
def vote_by_postid(id):
    for i in range(0, db2.llen("votes")):
        data = json.loads(db2.lindex("votes", i))
        if data['postID'] == id:
            return data, status.HTTP_200_OK
    
    return {"Not found the postID": f'{id}'}, status.HTTP_404_NOT_FOUND

# view 1 vote by voteID http://127.0.0.1:5000/vote/0
@app.route('/vote/<int:id>', methods=['GET'])
def vote_by_voteID(id):
    for i in range(0, db2.llen("votes")):
        data = json.loads(db2.lindex("votes", i))
        if data['voteID'] == id:
            return data, status.HTTP_200_OK

    return {"Not found the voteID": f'{id}'}, status.HTTP_404_NOT_FOUND

# upvote a post http://127.0.0.1:5000/post/<postID>/upvote
@app.route('/upvote/<int:id>', methods=['GET', 'POST'])
def up_votes(id):
    if request.method == 'GET':
        for i in range(0, db2.llen("votes")):
            data = json.loads(db2.lindex("votes", i))
            if data['postID'] == id:
                return data, status.HTTP_200_OK
        return {"Not found the postID": f'{id}'}, status.HTTP_404_NOT_FOUND

    elif request.method == 'POST':
        postID = request.data.get('postID')

        for i in range(0, db2.llen("votes")):
            data = json.loads(db2.lindex("votes", i))
            if data['postID'] == postID:
                data['upvote'] = data['upvote'] + 1
                db2.lset("votes", i, json.dumps(data))      # update upvote
                return data, status.HTTP_200_OK
        return {"Not found the postID": f'{postID}'}, status.HTTP_404_NOT_FOUND

# downvote a post http://127.0.0.1:5000/post/<postID>/downvote
@app.route('/downvote/<int:id>', methods=['GET', 'POST'])
def down_votes(id):
    if request.method == 'GET':
        for i in range(0, db2.llen("votes")):
            data = json.loads(db2.lindex("votes", i))
            if data['postID'] == id:
                return data, status.HTTP_200_OK
        return {"Not found the postID": f'{id}'}, status.HTTP_404_NOT_FOUND

    elif request.method == 'POST':
        postID = request.data.get('postID')

        for i in range(0, db2.llen("votes")):
            data = json.loads(db2.lindex("votes", i))
            if data['postID'] == postID:
                data['downvote'] = data['downvote'] + 1
                db2.lset("votes", i, json.dumps(data))      # update upvote
                return data, status.HTTP_200_OK
        return {"Not found the postID": f'{postID}'}, status.HTTP_404_NOT_FOUND

# top n post score http://127.0.0.1:5000/toppostscore/2
@app.route('/toppostscore/<int:topscore>', methods=['GET'])
def top_post_score(topscore):    
    sortedList = []

    if topscore > db2.llen("votes"):
        print("Length of list smaller than total number topscore")
        topscore = db2.llen("votes")

    while len(sortedList) < topscore:
        maxScore = -100
        maxData = {'':''}
        for i in range(0, db2.llen("votes")):            
            data = json.loads(db2.lindex("votes", i))
            flag = True
            for j in range(len(sortedList)):
                print(sortedList[j])
                if(data['postID'] == sortedList[j]['postID']):
                    flag = False
            if(flag):
                score = data['upvote'] - data['downvote']
                if score > maxScore:
                    maxScore = score
                    maxData = data
        # add to sortedList
        sortedList.append(maxData)

    return sortedList, status.HTTP_200_OK

# list sorted by score http://127.0.0.1:5000/listsortedbyscore
# input json example: {"listPostID": [0, 2]}
@app.route('/listsortedbyscore', methods=['GET', 'POST'])
def list_sorted_by_score():
    if request.method == 'GET':
        listVotes = []
        for i in range(0, db2.llen("votes")):
            data = json.loads(db2.lindex("votes", i))
            listVotes.append(data)
        return listVotes, status.HTTP_200_OK
    elif request.method == 'POST':
        datarequested = request.data    # this is a json
        listID = datarequested['listPostID']    # assign to the list
        print('List input: ' + f'{listID}')
        sortedList = []
        if len(listID) > db2.llen("votes"):
            print("Length of list input too large")
            return {'Max length': f'{db2.llen("votes")}'}, status.HTTP_400_BAD_REQUEST

        while len(sortedList) < len(listID):
            maxScore = -100
            maxData = {'':''}
            for i in range(0, db2.llen("votes")):            
                data = json.loads(db2.lindex("votes", i))
                for k in range(len(listID)):
                    if(data['postID'] == listID[k]):
                        flag = True
                        for j in range(len(sortedList)):
                            print(sortedList[j])
                            if(data['postID'] == sortedList[j]['postID']):
                                flag = False
                        if(flag):
                            score = data['upvote'] - data['downvote']
                            if score > maxScore:
                                maxScore = score
                                maxData = data
            # add to sortedList
            sortedList.append(maxData)
    return sortedList, status.HTTP_200_OK

# Create raw data
def raw_data():
    myDB = [
        {
            "voteID": 0, "postID": 0, "community": "home", "upvote": 2,"downvote": 0
        },
        {
            "voteID": 1, "postID": 1, "community": "school", "upvote": 4, "downvote": 0
        },
        {
            "voteID": 2, "postID": 2, "community": "workplace", "upvote": 10, "downvote": 1
        },
        {
            "voteID": 3, "postID": 3, "community": "home", "upvote": 2, "downvote": 0
        },
        {
            "voteID": 4, "postID": 4, "community": "home", "upvote": 2,"downvote": 0
        },
        {
            "voteID": 5, "postID": 5, "community": "school", "upvote": 4, "downvote": 0
        },
        {
            "voteID": 6, "postID": 6, "community": "workplace", "upvote": 10, "downvote": 1
        },
        {
            "voteID": 7, "postID": 7, "community": "home", "upvote": 2, "downvote": 0
        }
    ]

    for i in myDB:
        db2.lpush("votes", json.dumps(i))
    return myDB

if __name__ == '__main__':
    app.run(debug=True)

