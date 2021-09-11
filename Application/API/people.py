import time
from pydantic import BaseModel
from typing import Optional, List
import sqlalchemy

from Application.app import app, get_db, Session, Depends
from Application.API.models import DBPeople, DBlikes


class PeopleCreateRequest(BaseModel):
    """people schema validation"""
    name: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class PeopleGetResponse(BaseModel):
    """people schema validation"""
    name: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    peoples_liked_by_me: Optional[list] = []
    peoples_who_like_me: Optional[list] = []
    likes: Optional[list] = []

    class Config:
        orm_mode = True


class PeopleCreateResponse(BaseModel):
    """people schema validation"""
    message: Optional[str] = 'Person Added Successfully'

    class Config:
        orm_mode = True


'''Routes section'''


@app.post('/person/', response_model=PeopleCreateResponse)
async def add_person(people: PeopleCreateRequest, db: Session = Depends(get_db)):
    try:
        db_people = create_person(db, people)
    except sqlalchemy.exc.IntegrityError as err:
        db_people = {"message": '{} already exist'.format(people.name)}
    return db_people


@app.get('/peoples/', response_model=List[PeopleGetResponse])
def get_peoples(db: Session = Depends(get_db)):
    return q_get_peoples(db)


@app.get('/peoples/without_likes', response_model=List[PeopleGetResponse])
def get_peoples_without_likes(db: Session = Depends(get_db)):
    return q_get_peoples_without_like(db)


@app.get('/peoples/unhappy', response_model=List[PeopleGetResponse])
def get_unhappy_peoples(db: Session = Depends(get_db)):
    return q_get_unhappy_peoples(db)


@app.get('/peoples/favorites', response_model=List[PeopleGetResponse])
def get_favorites(db: Session = Depends(get_db)):
    return q_get_favorites(db)


@app.delete('/peoples/', response_model=PeopleCreateResponse)
async def delete_peoples(db: Session = Depends(get_db)):
    return delete_all_peoples(db)


'''Queries Section'''


def create_person(db: Session, people: PeopleCreateRequest):
    db_people = DBPeople(**people.dict())
    db.add(db_people)
    db.commit()
    db.refresh(db_people)

    return {"message": '{} added successfully'.format(people.name)}


def q_get_peoples(db: Session):
    return db.query(DBPeople).all()


def q_get_peoples_without_like(db: Session):
    peoples = db.query(DBPeople).all()
    peoples_without_likes = []
    for i in peoples:
        if len(i.likes) == 0:
            peoples_without_likes.append(i)
    return peoples_without_likes


def q_get_unhappy_peoples(db: Session):
    peoples = db.query(DBPeople).all()
    unhappy_peoples = []
    for person in peoples:
        if len(person.peoples_liked_by_me) != 0 and len(person.peoples_who_like_me) != 0:
            for p in set(person.peoples_who_like_me):
                if p in person.peoples_liked_by_me:
                    break
            else:
                unhappy_peoples.append(person)
    return unhappy_peoples


def q_get_favorites(db: Session):
    peoples = db.query(DBPeople).all()
    favorites = []
    for person in peoples:
        if len(person.peoples_who_like_me) != 0:
            if len(favorites) != 0:
                if len(set(person.peoples_who_like_me)) > len(set(favorites[-1].peoples_who_like_me)):
                    favorites[-1] = person
                elif len(set(person.peoples_who_like_me)) == len(set(favorites[-1].peoples_who_like_me)):
                    favorites.append(person)
            else:
                favorites.append(person)

    return favorites


def delete_all_peoples(db: Session):
    try:
        delete_people = db.query(DBPeople).delete()
        delete_likes = db.query(DBlikes).delete()
        db.commit()
        return {'message': 'Deleted peoples successfully'}
    except:
        db.session.rollback()
        return {'message': 'Delete peoples failed'}

