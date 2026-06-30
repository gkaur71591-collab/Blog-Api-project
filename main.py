from fastapi import FastAPI,Depends,HTTPException, Query
from sqlalchemy.orm import Session
from database import engine,SessionLocal
import model,schemas
from auth import create_token,verify_token
model.base.metadata.create_all(bind=engine)
app = FastAPI()

#db dependency
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
# login api
@app.post("/login")
def login():
    return {
        "access_token":create_token({"user":"admin"}),
        "token_type":"bearer"
    }

@app.get("/")
def home():
    return {"message":"Welcome to my blog API"}

#create blog(protected)
@app.post("/blogs",response_model=schemas.BlogResponse)
def create_blog(blog:schemas.BlogCreate,db:Session=Depends(get_db),user=Depends(verify_token)):
    new_blog=model.Blog(title=blog.title,content=blog.content)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

# read all blogs
@app.get("/blogs")
def get_blogs(page:int=1,limit:int=5, search:str=Query(default=""), db:Session=Depends(get_db),user=Depends(verify_token)):
    query=db.query(model.Blog)
    if search:
        query=query.filter(model.Blog.title.ilike(f"%{search}%"))
    total=query.count()
    start=(page-1)*limit
    end=start+limit
    blogs=query.offset(start).limit(limit).all()
    return {
        "page":page,
        "limit":limit,
        "total":total,
        "data":blogs

    }

#get blog by id (protected)
@app.get("/blogs/{id}",response_model=schemas.BlogResponse)
def get_blog(id:int,db:Session=Depends(get_db),user=Depends(verify_token)):
    blog=db.query(model.Blog).filter(model.Blog.id==id).first()
    if not blog:
        raise HTTPException(
            status_code=404,detail="blog not found"
        )
    return blog 

#update blog (protected)
@app.put("/blog/{id}",response_model=schemas.BlogResponse)
def update_blog(id:int,blog:schemas.BlogCreate, db:Session=Depends(get_db),user=Depends(verify_token)):
    existing_blog=db.query(model.Blog).filter(model.Blog.id==id).first()
    if not existing_blog:
        raise HTTPException(status_code=404,detail="not found blog")
    existing_blog.title=blog.title
    existing_blog.content=blog.content
    db.commit()
    db.refresh()
    return existing_blog

#delete blog
@app.delete("/blog/{id}")
def delete_blog(id:int,blog:schemas.BlogCreate,db:Session=Depends(get_db),user=Depends(verify_token)):
    blog=db.query(model.Blog).filter(model.Blog.id==id)
    if not blog:
        raise HTTPException(
            status_code=404,
            detail="not found"
        )
        
    blog.delete()
    db.commit()
    return {
            "message":"deleted successfully"
        }
