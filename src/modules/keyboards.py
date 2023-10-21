from vkbottle import Keyboard, KeyboardButtonColor, Text

from db.models import Hedgehog


class Mykeyboard:

    start_keyboard = (
        Keyboard(inline=True)
        .add(
            Text("Проверить", {"admin": "check"}),
            KeyboardButtonColor.POSITIVE
        )
    )

    my_hedgehog = (
        Keyboard(inline=True)
        .add(
            Text("инфо", {"command": "hedgehog_info"}),
            KeyboardButtonColor.POSITIVE
        )
    )

    def hedgehog_info(eat: bool) -> Keyboard:

        keyboard = Keyboard(inline=True)
        if eat:
            keyboard.add(
                Text("покормить", {"command": "feed_hedgehog"}),
                KeyboardButtonColor.POSITIVE
            )
            keyboard.row()
        keyboard.add(
            Text("ёжик", {"command": "my_hedgehog"}),
            KeyboardButtonColor.POSITIVE
        )

        return keyboard
