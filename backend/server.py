from raft.consensus import Node
from raft.consensus import FOLLOWER, LEADER
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sys
import logging

app = Flask(__name__)
CORS(app, resources={r"/req": {"origins": "http://127.0.0.1:*"}, r"/request": {"origins": "http://127.0.0.1:*"}})

@app.route('/authenticate', methods=['GET', 'POST'])
def authenticate():
    return render_template('users.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('test.html')

@app.route("/req", methods=['POST'])
def value_get():
    payload = request.json["payload"]
    reply = {"code": 'fail', 'payload': payload}
    if n.status == LEADER:
        result = n.handle_get(payload)
        if result == -1:
            reply = {"code": "fail", "reason": "Invalid"}
        else:
            reply = {"code": "success", "payload": result}
    elif n.status == FOLLOWER:
        reply["payload"]["message"] = n.leader
    return jsonify(reply)

@app.route("/request", methods=['POST'])
def value_put():
    payload = request.json["payload"]
    reply = {"code": 'fail'}

    if n.status == LEADER:
        # request handle, reply is a dictionary
        result = n.handle_put(payload)
        print("result", result)
        if result == -1:
            reply = {"code": "fail", "reason": "Username already exists!"}
        else:
            reply = {"code": "success"}
    elif n.status == FOLLOWER:
        # redirect request
        payload["message"] = n.leader
        reply["payload"] = payload
    return jsonify(reply)

# we reply to vote request
@app.route("/vote_req", methods=['POST'])
def vote_req():
    term = request.json["term"]
    commitIdx = request.json["commitIdx"]
    staged = request.json["staged"]
    choice, term = n.decide_vote(term, commitIdx, staged)
    message = {"choice": choice, "term": term}
    return jsonify(message) 

@app.route("/heartbeat", methods=['POST'])
def heartbeat():
    term, commitIdx = n.heartbeat_follower(request.json)
    # return anyway, if nothing received by leader, we are dead
    message = {"term": term, "commitIdx": commitIdx}
    return jsonify(message)

# disable flask logging
log = logging.getLogger('werkzeug')
log.disabled = True

if __name__ == "__main__":
    # python server.py index ip_list
    if len(sys.argv) == 3:
        index = int(sys.argv[1])
        ip_list_file = sys.argv[2]
        ip_list = []
        with open(ip_list_file) as f:
            for ip in f:
                ip_list.append(ip.strip())
        my_ip = ip_list.pop(index)
        
        http, host, port = my_ip.split(':')
        
        n = Node(ip_list, my_ip)
        app.run(port=int(port), debug=False)
    else:
        print("usage: python server.py <index> <ip_list_file>")