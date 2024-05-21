from fastapi import FastAPI, Depends 
from typing import Annotated

def depfunc1(): 
    
    return "Zain"

def depfunc2(): 
    return "ATTiq"

app = FastAPI(dependencies=[Depends(depfunc1), Depends(depfunc2)])


@app.get('/')
def index():
    return "indexpage"
@app.get('/main/{fname}')
def get_name(fname:str, mname:Annotated[str, Depends(depfunc1)], lname:Annotated[str, Depends(depfunc2)]):
    return f"{fname} {mname} {lname}"
