from vkbottle.dispatch.rules import ABCRule
from vkbottle.bot import Message


class admin_rule(ABCRule[Message]):

    async def check(self, event: Message) -> bool:

        members = await event.ctx_api.messages.get_conversation_members(event.peer_id)
        admins = [member.member_id for member in members.items if member.is_admin]

        return event.from_id in admins
