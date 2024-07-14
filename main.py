from fastapi import FastAPI,HTTPException;
from blogs import blog


app = FastAPI()

@app.get("/")
def main():
  return  {
    "ok":True
  }


@app.get("/blog")
def main(start: int = 1, end: int = 10):
    if start < 0:
        raise HTTPException(status_code=400, detail="Start must be greater than or equal to 0")
    return {
        "blog": blog[start-1:end]
    }
  
@app.get('/blog/{id}')
def get_blog(id: int):
    try:
        for i in blog:
            if i['id'] == id:
                return {
                    "id": id,
                    "title": i.get("title"),
                    "content": i.get("content")
                }
        raise HTTPException(status_code=404, detail="Invalid blog id")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid blog id format")   
   
