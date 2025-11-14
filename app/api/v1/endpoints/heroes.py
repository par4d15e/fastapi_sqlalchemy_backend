from collections.abc import Sequence

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.crud import crud
from app.models.heroes import Hero, HeroTeamLink, Team

router = APIRouter()


@router.post("/heroes/", response_model=Hero)
def create_hero(hero: Hero, session: Session = Depends(crud.get_session)) -> Hero:
    return crud.create_hero(hero, session)


@router.get("/heroes/", response_model=list[Hero])
def read_heroes(
    offset: int = 0,
    limit: int = 100,
    session: Session = Depends(crud.get_session),
) -> Sequence[Hero]:
    return crud.read_heroes(offset, limit, session)


@router.get("/heroes/{hero_id}", response_model=Hero)
def read_hero(hero_id: int, session: Session = Depends(crud.get_session)) -> Hero:
    hero = crud.read_hero(hero_id, session)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero


@router.put("/heroes/{hero_id}", response_model=Hero)
def update_hero(hero_id: int, hero: Hero, session: Session = Depends(crud.get_session)) -> Hero:
    db_hero = crud.read_hero(hero_id, session)
    if not db_hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    hero_data = hero.model_dump(exclude_unset=True)
    return crud.update_hero(db_hero, hero_data, session)


@router.delete("/heroes/{hero_id}")
def delete_hero(hero_id: int, session: Session = Depends(crud.get_session)) -> dict[str, bool]:
    hero = crud.read_hero(hero_id, session)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    crud.delete_hero(hero, session)
    return {"ok": True}


@router.post("/teams/", response_model=Team)
def create_team(team: Team, session: Session = Depends(crud.get_session)) -> Team:
    return crud.create_team(team, session)


@router.get("/teams/", response_model=list[Team])
def read_teams(session: Session = Depends(crud.get_session)) -> list[Team]:
    return crud.read_teams(session)


@router.post("/heroteamlinks/", response_model=HeroTeamLink)
def create_hero_team_link(
    link: HeroTeamLink, session: Session = Depends(crud.get_session)
) -> HeroTeamLink:
    return crud.create_hero_team_link(link, session)
