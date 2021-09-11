import time
from pydantic import BaseModel
from typing import Optional, List

from Application.app import app, get_db, Session, Depends
from Application.API.models import DBlikes, DBPeople


class LikesIn(BaseModel):
    """likes schema validation"""
    from_user: str
    to_user: str

    class Config:
        orm_mode = True


class LikesOut(BaseModel):
    """likes schema validation"""
    from_user: str
    to_user: str
    message: Optional[str] = 'Like Added Successfully'

    class Config:
        orm_mode = True


@app.post('/like/', response_model=LikesOut)
async def add_likes(likes: LikesIn, db: Session = Depends(get_db)):
    db_likes = create_likes(db, likes)
    return db_likes


@app.get('/like/', response_model=List[LikesIn])
async def get_likes(db: Session = Depends(get_db)):
    for i in get_like(db):
        print(i.id)
    return get_like(db)


'''Queries Section'''


def create_likes(db: Session, likes: LikesIn):
    """add like to db"""
    db_like = DBlikes(**likes.dict())

    """update people db"""

    # Get person how is liking
    db_person_who_like = db.query(DBPeople).get(likes.from_user)
    if db_person_who_like is None:
        return {'message': '{0} is not exist'.format(likes.from_user),
                'from_user': likes.from_user, "to_user": likes.to_user}
    else:
        '''Check if u already likes a person'''
        if likes.to_user in db_person_who_like.peoples_liked_by_me:
            return {'message': '{0} already like {1}'.format(likes.from_user, likes.to_user),
                    'from_user': likes.from_user, "to_user": likes.to_user}
        db_person_who_like.peoples_liked_by_me.append(likes.to_user)

    # Get person who is getting like
    db_person_whom_like = db.query(DBPeople).get(likes.to_user)
    if db_person_whom_like is None:
        return {'message': '{0} is not exist'.format(likes.to_user),
                'from_user': likes.from_user, "to_user": likes.to_user}
    else:
        db_person_whom_like.peoples_who_like_me.append(likes.from_user)

    db.add(db_like)
    db.add(db_person_who_like)
    db.add(db_person_whom_like)
    db.commit()
    db.refresh(db_like)

    return db_like


def get_like(db: Session):
    return db.query(DBlikes).all()
