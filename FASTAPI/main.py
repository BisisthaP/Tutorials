from fastapi import FastAPI

api = FastAPI()

#stimulation of a database 
all_todo = [{'todo_id': 1, 'task': 'Do laundry'}, {'todo_id': 2, 'task': 'Read a book'}]

@api.get("/")

def index():
    return {"message": "Hello, World!"}

@api.get('calculation')
def calculation():
    pass 
    return ""
#above is sync 

# @api.get('/getdata')
# async def get_data_from_db():
#     await requests #only used for asyn 
#     pass 
#     return ""

#use path parameters to retrieve a specific todo item
# '/' = default path/route 
#{abc} = where abc is a path parameter (anything in {} is a path parameter)
@api.get('/todos/{todo_id}')  #endpoint to get a specific todo item
def get_todo(todo_id: int):
    #because we are loading from a list - use sync 
    #but if we were loading from a database - use async
    for todo in all_todo:
        if todo['todo_id'] == todo_id:
            return {'result': todo}

@api.get('/todos')  #endpoint is the todo without any path parameter
def get_todo(first_n: int = None):  #query parameter 
    if first_n:
        return {'result': all_todo[:first_n]}  #return the first n todo items
    else:
        return all_todo
#difference between path and query parameters - 
# path parameters are part of the path - /todos/{todo_id} (must be defined within the path)
# query parameters are optional and are defined after the ? in the URL - /todos?first_n=3 - will return the first 3 todo items

#error 
#http://127.0.0.1:9999/todos?first_n=2
#type error - slice indices must be integers or None or have an __index__ method
#so the value for first_n is treated as a string, not integer 
#solution - add first_n :int = None in the function definition

#can access the specific todo item by going to the URL - http://127.0.0.1:9999/todos/1
#where 1 is the todo_id

from fastapi import FastAPI

app = FastAPI()

# The router maps a GET request at the path "/users/123" to the function below
@app.get("/users/{user_id}")
async def read_user(user_id: int):
    # The path parameter {user_id} is automatically passed to the function
    return {"user_id": user_id, "detail": "User data"}

from fastapi.responses import JSONResponse

@app.get("/data")
def get_data():
    # FastAPI/Starlette converts this Python dict into a JSON response
    return {"message": "Hello from the server"}

@app.get("/custom_response")
def custom_response():
    # You can also manually return a specific Starlette response
    return JSONResponse(
        content={"status": "ok"},
        status_code=202,
        headers={"X-Custom-Header": "FastAPI-Powered"}
    )

from fastapi.middleware.cors import CORSMiddleware
# The CORSMiddleware is a Starlette component used directly in FastAPI

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],
)

# Every request will pass through this middleware before hitting the router.
# The middleware adds the necessary CORS headers to allow cross-domain requests.

from fastapi import WebSocket

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # 1. Accept the connection (Establishes the channel)
    await websocket.accept() 
    try:
        while True:
            # 2. Receive data from the client
            data = await websocket.receive_text()
            
            # 3. Send data back to the client
            await websocket.send_text(f"Message received: {data}")
    except Exception:
        # 4. Handle connection close
        print(f"Client disconnected")
    finally:
        await websocket.close()