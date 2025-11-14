from collections.abc import Iterator, Sequence
from typing import Any

from sqlmodel import Session, select
from app.core.database import engine
from app.models.heroes import Hero, HeroTeamLink, Team


def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session


def create_hero(hero: Hero, session: Session) -> Hero:
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero


def read_heroes(offset: int, limit: int, session: Session) -> Sequence[Hero]:
    return session.exec(select(Hero).offset(offset).limit(limit)).all()


def read_hero(hero_id: int, session: Session) -> Hero | None:
    return session.get(Hero, hero_id)


def update_hero(db_hero: Hero, hero_data: dict[str, Any], session: Session) -> Hero:
    for key, value in hero_data.items():
        setattr(db_hero, key, value)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero


def delete_hero(hero: Hero, session: Session) -> None:
    session.delete(hero)
    session.commit()


def create_team(team: Team, session: Session) -> Team:
    session.add(team)
    session.commit()
    session.refresh(team)
    return team


def read_teams(session: Session) -> list[Team]:
    return list(session.exec(select(Team)).all())


def create_hero_team_link(link: HeroTeamLink, session: Session) -> HeroTeamLink:
    session.add(link)
    session.commit()
    session.refresh(link)
    return link