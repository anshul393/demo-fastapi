from app import oauth2
from .. import models,schemas,utils
from fastapi import status,HTTPException,Depends,APIRouter,Response
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from typing import List, Optional

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]  # to differentiate in documentation between users and post HTTP method
) 


@router.get("/",response_model= List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),user_id : int = Depends(oauth2.get_current_user),limit : int =10 ,skip : int = 0,search : Optional[str] = ""):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() 

    results = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id == models.Post.id,isouter = True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() 
    ##### Here limit ,skip,search are query parameters which  comes after ? in the url ip-address/endpoint?query-parameters
 
    ##### To add multiple query parameters use & and to provide space use % 
    # print(type(results[0]["Post"]))
    return results

# @app.post("/createposts")
# def create_post(recieved_data : dict = Body(...)):
#     print(recieved_data)
#     return {"message": f"title : {recieved_data['title']} and content : {recieved_data['content']}"}

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse)
def create_post(post : schemas.PostCreate,db: Session = Depends(get_db),user_id : int = Depends(oauth2.get_current_user)):               # BaseModel extract the data by itself and do all the validation by itself # extracted data gets stored in pydantic model and can be converted into dictionary
    
    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""",(post.title,post.content,post.published))
    # new_posts = cursor.fetchone() # It will fetch the new created_post

    # conn.commit() # To save changes in the database permanantly
    
    post = post.dict()
    post["owner_id"] =  int(user_id)
    new_post = models.Post(**post) #title = post.title, content = post.content, published = post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post

@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id:int,response: Response,db: Session = Depends(get_db),user_id : int = Depends(oauth2.get_current_user)):         
    
    # id: int will try to convert recieved id into int and validate it         
    # # fastapi automatically extract the id from path parameter and it can be passed to the function . It will come as string
    # cursor.execute("""SELECT * from posts WHERE id = %s""",(str(id),))
    # post = cursor.fetchone()
    post = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id == models.Post.id,isouter = True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if post:
        return post
    else:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message" : f"post with id {id} was not found"}
        #Instead of setting response and sending message separatly , it can be done more effeciently using HTTPException
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} was not found")


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db: Session = Depends(get_db),user_id : int = Depends(oauth2.get_current_user)):
    
    # cursor.execute("""DELETE from posts WHERE id = %s RETURNING *""", (str(id),))
    # deleted_post = cursor.fetchone()

    # conn.commit()
    
    post = db.query(models.Post).filter(models.Post.id == id)
    post_ = post.first()

    
    if not post_:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} was not found")
    
    elif post_.owner_id == user_id:
        post.delete(synchronize_session=False)
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"Not authorized to perform requested action")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}")
def update_post(id:int,post:schemas.PostCreate,db: Session = Depends(get_db),user_id : int = Depends(oauth2.get_current_user)):
    
    # cursor.execute("""UPDATE posts SET title = %s,content = %s, published = %s WHERE id = %s RETURNING *""",(post.title,post.content,post.published,str(id)))
    # updated_post = cursor.fetchone()

    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post_ = post_query.first()
    if not post_:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} was not found")
    
    elif post_.owner_id == user_id:
        post_query.update(post.dict(),synchronize_session=False)
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"Not authorized to perform requested action")

    return {"data" : "successful"}

    