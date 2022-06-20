from typing import List, Optional

from sqlalchemy import delete, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.engine.row import RowMapping
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio.engine import AsyncConnection

from tgbot.database.tables import admins, users, projects


class Repo:
    """Db abstraction layer"""

    def __init__(self, conn: AsyncConnection):
        self.conn: AsyncConnection = conn

    # users
    async def add_user(
        self,
        user_id: int,
        firstname: str,
        fullname: str,
        lastname: Optional[str],
        username: Optional[str],
        lang: Optional[str] = None
    ) -> None:
        """Store user in DB, ignore duplicates

        :param user_id: User's telegram id
        :type user_id: int
        :param firstname: User's firstname
        :type firstname: str
        :param fullname: User's fullname
        :type fullname: str
        :param lastname: User's lastname
        :type lastname: Optional[str]
        :param lastname: User's username
        :type lastname: Optional[str]
        :param lang: Language str in ISO 639-1 standart
        :type lang: Optional[str]
        """
        # Create insert statement
        stmt = insert(users).values(
            user_id=user_id,
            firstname=firstname,
            fullname=fullname,
            lastname=lastname,
            username=username,
            lang=lang
        ).on_conflict_do_nothing()

        # Execute statement
        await self.conn.execute(stmt)
        # Commit changes
        await self.conn.commit()
        return

    async def get_user(self, user_id: int) -> Optional[RowMapping]:
        """Returns user from database by user id

        :param user_id: User telegram id
        :type user_id: int
        :return: User data from database or None if user not exists
        :rtype: Optional[dict]
        """
        # Create statement
        stmt = select(users).where(
            users.c.user_id == user_id
        )

        # Execute statement
        res = await self.conn.execute(stmt)
        try:
            # Try to return one result
            return res.mappings().one()

        except NoResultFound:
            # If no results found return None
            return None

    async def list_users(self) -> list:
        """List all bot users"""
        # Create statement
        stmt = select(users)

        # Execute statement
        res = await self.conn.execute(stmt)
        # Return all found data in list of dicts or None
        return res.mappings().all()

    async def update_user_lang(self, user_id: int, lang: str) -> None:
        """Updates user language

        :param user_id: User's telegram id
        :type user_id: int
        :param lang: Language str in ISO 639-1 standart
        :type lang: str
        """
        # Create statement
        stmt = update(users).values(
            lang=lang
        ).where(
            users.c.user_id == user_id
        )

        # Execute statement
        await self.conn.execute(stmt)
        # Save changes
        await self.conn.commit()
        return

    # admins
    async def add_admin(self, user_id: int) -> None:
        """Store admin in DB, ignore duplicates

        :param user_id: User telegram id
        :type user_id: int
        """
        # Create statement
        stmt = insert(admins).values(
            user_id=user_id
        ).on_conflict_do_nothing()

        # Execute statement
        await self.conn.execute(stmt)
        # Save changes
        await self.conn.commit()
        return

    async def is_admin(self, user_id: int) -> bool:
        """Checks user is admin or not

        :param user_id: User telegram id
        :type user_id: int
        :return: User is admin boolean
        :rtype: bool
        """
        # Create statement
        stmt = select(admins).where(
            admins.c.user_id == user_id
        )

        # Execute statement
        res = await self.conn.execute(stmt)
        try:
            # If one result found return True
            res.mappings().one()
            return True

        except NoResultFound:
            # If no results found return False
            return False

    async def del_admin(self, user_id: int) -> int:
        """Delete admin from DB by user id

        :param user_id: User telegram id
        :type user_id: int
        :return: Deleted row count
        :rtype: int
        """
        # Create statement
        stmt = delete(admins).where(
            admins.c.user_id == user_id
        )

        # Execute statement
        res = await self.conn.execute(stmt)
        # Save changes
        await self.conn.commit()
        # Return deleted row count
        return res.rowcount

    async def list_admins(self) -> List[RowMapping]:
        """List all bot admins"""
        # Create statement
        stmt = select(admins)

        # Execute statement
        res = await self.conn.execute(stmt)
        # Return all found data in list of dicts or None
        return res.mappings().all()
    
    # projects
    async def add_project(self, owner_id: int, name: str, description: str) -> None:
        """Stores project info DB, ignore duplicates

        :param owner_id: Project owner telegram id
        :type owner_id: int
        :param name: Project name
        :type name: str
        :param description: Project description
        :type description: str
        """
        # Create statement
        stmt = insert(projects).values(
            owner_id=owner_id,
            name=name,
            description=description
        ).on_conflict_do_nothing()

        # Execute statement
        await self.conn.execute(stmt)
        # Commit changes
        await self.conn.commit()
        return
    
    async def get_project_by_id(self, project_id: int) -> Optional[RowMapping]:
        """Returns project from DB by project id

        :param project_id: Project id
        :type project_id: int
        :return: Project info
        :rtype: list
        """
        # Create statement
        stmt = select(projects).where(
            projects.c.project_id == project_id
        )
        # Execute statement
        res = await self.conn.execute(stmt)
        try:
            # Try to return one result
            return res.mappings().one()

        except NoResultFound:
            # If no results found return None
            return None
    
    async def get_users_projects(self, owner_id: int) -> List[RowMapping]:
        """Returns all users project from DB by owner_id

        :param owner_id: Project owner telegram id
        :type owner_id: int
        :return: Projects list
        :rtype: list
        """
        # Create statement
        stmt = select(projects).where(
            projects.c.owner_id == owner_id
        )
        
        # Execute statement
        res = await self.conn.execute(stmt)
        # Return all results
        return res.mappings().all()

    async def del_project_by_id(self, project_id: int) -> int:
        """Remove project from DB by project id

        :param project_id: Project id
        :type project_id: int
        :return: Removed row count
        :rtype: int
        """
        # Create statement
        stmt = delete(projects).where(
            projects.c.project_id == project_id
        )

        # Execute statement
        res = await self.conn.execute(stmt)
        # Save changes
        await self.conn.commit()
        # Return deleted row count
        return res.rowcount
