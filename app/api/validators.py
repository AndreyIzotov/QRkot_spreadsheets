from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    '''Проверяет название проекта на уникальность.'''
    new_project_name = await charity_project_crud.get_project_by_name(project_name, session)
    if new_project_name is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def check_project_exists(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    project = await charity_project_crud.get(project_id, session)
    if not project:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден!'
        )
    return project


async def check_project_invest(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    '''Проверяет внесённую сумму в проект.'''
    project = await charity_project_crud.get(project_id, session)
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
    await check_project_exists(project_id, session)
    return project


async def check_project_update(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession,
) -> CharityProject:
    '''Только для суперюзеров.
    Редактирование проекта'''
    project = await charity_project_crud.get(project_id, session)
    if not project:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден!'
        )
    if project.fully_invested is True:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!'
        )
    if obj_in.full_amount and obj_in.full_amount < project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Нельзя установить требуемую сумму меньше уже вложенной.'
        )
    if obj_in.name and obj_in.name != project.name:
        await check_name_duplicate(obj_in.name, session)

    return project
