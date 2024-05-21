from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def zain():
    return "fastapi"
@app.get('/hello/{name}')
def say_hello(name:str):
    return f"hello {name}"
@app.get('/users/{name}')
def get_user(name:str, age:int, gender:str, isMarried:bool, desc:str):
    return f"this is the user with name {name}, age {age}, gender {gender} ismarried {isMarried} here is the descritpion {desc} "


#write a function to find factorial
def factorial(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n-1)
    
#write the code to connect with the database
