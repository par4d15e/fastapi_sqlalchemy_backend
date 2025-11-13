from collections.abc import Iterator

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.core.database import engine
from app.models.heroes import Hero, HeroTeamLink, Team

router = APIRouter()


def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session


@router.post("/heroes/", response_model=Hero)
def create_hero(hero: Hero, session: Session = Depends(get_session)) -> Hero:
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero


@router.get("/heroes/", response_model=list[Hero])
def read_heroes(offset: int = 0, limit: int = 100, session: Session = Depends(get_session)) -> list[Hero]:
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes


@router.get("/heroes/{hero_id}", response_model=Hero)
def read_hero(hero_id: int, session: Session = Depends(get_session)) -> Hero:
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero


@router.put("/heroes/{hero_id}", response_model=Hero)
def update_hero(hero_id: int, hero: Hero, session: Session = Depends(get_session)) -> Hero:
    db_hero = session.get(Hero, hero_id)
    if not db_hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    hero_data = hero.model_dump(exclude_unset=True)
    for key, value in hero_data.items():
        setattr(db_hero, key, value)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero


@router.delete("/heroes/{hero_id}")
def delete_hero(hero_id: int, session: Session = Depends(get_session)) -> dict[str, bool]:
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
    return {"ok": True}


@router.post("/teams/", response_model=Team)
def create_team(team: Team, session: Session = Depends(get_session)) -> Team:
    session.add(team)
    session.commit()
    session.refresh(team)
    return team


@router.get("/teams/", response_model=list[Team])
def read_teams(session: Session = Depends(get_session)) -> list[Team]:
    teams = session.exec(select(Team)).all()
    return teams


@router.post("/heroteamlinks/", response_model=HeroTeamLink)
def create_hero_team_link(link: HeroTeamLink, session: Session = Depends(get_session)) -> HeroTeamLink:
    session.add(link)
    session.commit()
    session.refresh(link)
    return link