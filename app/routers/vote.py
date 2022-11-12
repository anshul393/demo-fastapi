from fastapi import status,HTTPException,Depends,APIRouter,Response
from .. import schemas,database,oauth2,models
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote : schemas.Vote,db : Session = Depends(database.get_db),user_idd : int = Depends(oauth2.get_current_user)):


    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Post with post_id {vote.post_id} does not exist')

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,models.Vote.user_id == user_idd)
    found_vote = vote_query.first()


    if vote.dir == 1 and found_vote:
        raise HTTPException(status_code= status.HTTP_409_CONFLICT,detail=f'user with user_id {user_idd} has already liked the post with post_id {vote.post_id}')
    elif vote.dir == 1:
        new_vote = models.Vote(post_id = vote.post_id,user_id = user_idd)
        db.add(new_vote)
        db.commit()

        return {"message" : "successfuly added vote"}
    elif vote.dir == 0 and found_vote:
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message" : "successfuly deleted vote"}
    elif vote.dir == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Not found")


