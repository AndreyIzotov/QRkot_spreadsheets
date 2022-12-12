from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_project_by_name(
            self,
            project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        project_name = await session.execute(
            select(CharityProject).where(
                CharityProject.name == project_name
            )
        )
        project_name = project_name.scalars().first()
        return project_name

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession
    ) -> Optional[list[dict[str, str]]]:
        projects = await session.execute(
            select(
                CharityProject.name,
                CharityProject.close_date,
                CharityProject.create_date,
                CharityProject.description).where(
                    CharityProject.fully_invested)
        )
        result = []
        for obj in projects:
            result.append({
                'name': obj.name,
                'delta': str(obj.close_date - obj.create_date),
                'description': obj.description})
        return sorted(result, key=lambda x: x['delta'])


charity_project_crud = CRUDCharityProject(CharityProject)
