from fastapi import FastAPI, Depends, HTTPException, status
from typing import Annotated, Any

blogs = {
    "1": "Generative AI Blog",
    "2": "Machine Learning Blog",
    "3": "Deep Learning Blog"
}


users = {
    "8": "Ahmed",
    "9": "Mohammed"
}

class GetObjectOr404():
    def __init__(self, model) -> None:
        self.model = model
    
    def __call__(self, id:str) :
        obj = self.model.get(id)
        if not obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Object ID {id} not found")
        return obj
    
app = FastAPI(title="Learn Dependency Injection")
blog_dependency = GetObjectOr404(blogs)
user_dependency = GetObjectOr404(users)

@app.get('/blog/{id}')
def get_blog(user: Annotated[str, Depends(blog_dependency)]):
    return user


@app.get('/user/{id}')
def get_user(blog: Annotated[str, Depends(user_dependency)]):
    return blog
