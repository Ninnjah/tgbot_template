from typing import List

from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware

from tgbot.models.role import UserRole


class RoleMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]

    def __init__(self, admin_list: List[int]):
        super().__init__()
        self.admin_list = admin_list

    async def pre_process(self, obj, data, *args):
        if not getattr(obj, "from_user", None):
            data["role"] = None
        elif any((
            obj.from_user.id in self.admin_list,
            await data["repo"].is_admin(obj.from_user.id)
        )):
            data["role"] = UserRole.ADMIN
        else:
            data["role"] = UserRole.USER

    async def post_process(self, obj, data, *args):
        del data["role"]
