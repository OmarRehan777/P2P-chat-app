from pymongo import MongoClient
# gadGAD
# 3000 
# 3001
# 172.16.0.2
# Includes database operations
class DB:


    # db initializations
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['p2p-chat']


    # checks if an account with the username exists
    def is_account_exist(self, username):
        if self.db.accounts.find_one({'username': username}):
            return True
        else:
            return False
    

    # registers a user
    def register(self, username, password):
        account = {
            "username": username,
            "password": password
        }
        self.db.accounts.insert_one(account)


    # retrieves the password for a given username
    def get_password(self, username):
        return self.db.accounts.find_one({"username": username})["password"]


    # checks if an account with the username online
    def is_account_online(self, username):
        if self.db.online_peers.find_one({"username": username}):
            return True
        else:
            return False

    
    # logs in the user
    def user_login(self, username, ip, port):
        online_peer = {
            "username": username,
            "ip": ip,
            "port": port
        }
        self.db.online_peers.insert_one(online_peer)
    

    # logs out the user 
    def user_logout(self, username):
        acc=self.db["online_peers"].find_one({"username": username})
        self.db["online_peers"].delete_one(acc)
    

    # retrieves the ip address and the port number of the username
    def get_peer_ip_port(self, username):
        res = self.db.online_peers.find_one({"username": username})
        return (res["ip"], res["port"])
    
    def room_create(self, roomid,username):
        room = {
            "roomid": roomid,
            "clients": [username]
        }
        self.db.rooms.insert_one(room)

    def is_room_exist(self, roomid):
        if self.db.rooms.find_one({"roomid": roomid}):
            return True
        else:
            return False

    def add_client(self, roomid, username):
        self.db.rooms.update_one({"roomid":roomid},{"$push": {"clients":username}})
        
    def isUserAlreadyInRoom(self, roomid, username):
        document = {
            "roomid": roomid,
            "clients": username            
        }

        return self.db.rooms.find_one(document)
    
    
    
    