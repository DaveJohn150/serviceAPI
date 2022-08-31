from fastapi import FastAPI, Request, HTTPException, status
from pydantic import BaseModel
import queue
from os import getenv
from os.path import dirname

#define queue
logsQueue = queue.Queue()

#define fast api application
app = FastAPI()

#class for returned city value
class Data(BaseModel):
    Location: str

#class for returned chat bot logs 
class logData(BaseModel):
    Text: str
    Timestamp: str
    UserName: str
    ConversationType: str
    ConversationID: str

#dictionary to store location
locations = {
    0: {
        "Location": "Perth"
    }
}

f = open('key.txt') #works running in docker, doesnt work running locally
key = f.read().strip()
f.close()

def auth(req):
    try:
        apiKey = req.headers["Authorization"]
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No Authorization header"
        ) 
    if apiKey != key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect API key in Authorization header"
        ) 
    else:
        return

#Url and Function for location get request 
@app.get("/get-location")
def home(req: Request):
    auth(req)
    return (locations)

#Url and Function for location post request
@app.post("/new-location")
def create_item(data: Data, req: Request):
    auth(req)
    locations[0] = { "Location" : data.Location}
    return[locations[0]]

#Url and Function for chat log post request
@app.post("/add-chatlog")
def add_chatlog(logdata: logData, req: Request):
    auth(req)
    bot_log_data = {    
        "Text": logData.Text,
    "Timestamp": logData.Timestamp,
    "UserName": logData.UserName,
    "ConversationType": logData.ConversationType,
    "ConversationID": logData.ConversationID
    }
    logsQueue.put(bot_log_data)
    return[list(logsQueue.queue)]

#Url and Function for chat log get request
@app.get("/get-chatlog")
def get_chatlog(req: Request):
    auth(req)
    listObj = []
    while not logsQueue.empty():
        listObj.append(logsQueue.get())    
    return[listObj]

# For debugging only
# import uvicorn
# if __name__ == "__main__":
#     uvicorn.run(app,  port="8000")