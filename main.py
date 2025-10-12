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

