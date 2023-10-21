from vkbottle import Keyboard, KeyboardButtonColor, Text


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

    def hedgehog_info(
        eat: bool,
        send_working: bool,
        pick_working: bool
    ) -> Keyboard:

        keyboard = Keyboard(inline=True)
        if eat:
            keyboard.add(
                Text("покормить", {"command": "feed_hedgehog"}),
                KeyboardButtonColor.POSITIVE
            )
            keyboard.row()
        if pick_working:
            keyboard.add(
                Text("забрать с работы", {"command": "pick_from_work"}),
                KeyboardButtonColor.POSITIVE
            )
            keyboard.row()
        if send_working:
            keyboard.add(
                Text("отправить на работу", {"command": "send_to_work"}),
                KeyboardButtonColor.POSITIVE
            )
            keyboard.row()
        keyboard.add(
            Text("ёжик", {"command": "my_hedgehog"}),
            KeyboardButtonColor.POSITIVE
        )

        return keyboard
