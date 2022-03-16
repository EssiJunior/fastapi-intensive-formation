from fastapi import status, Depends , HTTPException, Response, APIRouter
from .. import models, schemas, oauth2
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, asc
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/", response_model= List[schemas.PostOut])
def getPosts(db: Session = Depends(get_db), current_user: models.User=
Depends(oauth2.get_current_user), limit: int = 10, skip :int =0, search: Optional[str] = ""):
    #cursor.execute("""SELECT * FROM posts""")
    #result = cursor.fetchall()
    #posts = db.query(models.Post).filter(models.Post.content.contains(search)).limit(limit).offset(skip).all()
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id 
    == models.Post.id,isouter=True).group_by(models.Post.id).order_by(asc(models.Post.id)).filter(models.Post.content.contains(search)).limit(limit).offset(skip).all()
    
    return posts

@router.get("/{identifier}", response_model=schemas.PostOut)
def getPost(identifier: int, db: Session = Depends(get_db), current_user: models.User=
Depends(oauth2.get_current_user)):
    #post = get_post(id)
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id == models.Post.id,isouter=True).group_by(models.Post.id).order_by(asc(models.Post.id)).filter(models.Post.id == id).first()
    print(post)
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id {identifier} is not accessible")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message": f"post with id {id} is not accessible"}
    
    #if current_user.id != post.user_id:
    #    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Not authorize to perform action")

    return post

#payload: dict = Body(...) ---> Take data from the body
@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.Post)
def createPost(post: schemas.PostCreate,db: Session = Depends(get_db), current_user: models.User=
Depends(oauth2.get_current_user)):
    #my_posts.append(post.dict())
    #response.status_code = status.HTTP_201_CREATED
    #cursor.execute(f"""INSERT INTO posts(title,content,published) VALUES ('{post.title}','{post.content}','{post.published}') RETURNING *""")
    #result = cursor.fetchone()
    #connection.commit()
    #**post.dict() == title=post.title, content=post.content, published= post.published
    print(current_user.id)
    print(type(current_user))
    print(current_user.email)
    post = models.Post(user_id=current_user.id, **post.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    
    return post

@router.delete("/{identifier}", status_code = status.HTTP_204_NO_CONTENT)
def deletePost(identifier: int,db: Session = Depends(get_db), current_user: models.User=
Depends(oauth2.get_current_user)):
    #cursor.execute(f"""DELETE FROM posts WHERE id = {id} RETURNING *""")
    #response = cursor.fetchone()
    response = db.query(models.Post).filter(models.Post.id == identifier)
    if response.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id {identifier} is not accessible")

    if user_id == identifier:
        response.delete(synchronize_session=False)
        db.commit()
        
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    return "delete operation"
    #if response != None:    
    #    connection.commit()
    #    return {"message": "post deleted!","data": "response"}
    #else:
    #    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"No index {id}")

@router.put("/{identifier}", response_model=schemas.Post)
def updatePost(identifier: int, post: schemas.PostCreate,db: Session = Depends(get_db)):
    #cursor.execute(f"""UPDATE posts SET title = '{post.title}', content = '{post.content}', published = '{post.published}' WHERE id = {id} RETURNING *""")
    #response = cursor.fetchone()
    
    #if response != None:
    #    connection.commit()
    #    return {"message": "post updated!","data": response}
    #else:
    #    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"No index {id}")
    response = db.query(models.Post).filter(models.Post.id == identifier)
    if response.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id {identifier} is not accessible")

    response.update(post.dict(),synchronize_session="False")
    db.commit()
    
    return response.first()
