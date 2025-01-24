from aiogram import F, types
from aiogram.types import FSInputFile
from signature import BotSettings
from keyboards.client_kb import ReplyKb as kb

REQUIRED_CHANNEL = "@megatestbota"  # Замените на имя вашего канала


class Client:
    def __init__(self, bot: BotSettings):
        self.bot = bot.bot
        self.dp = bot.dp
        self.db = bot.db


    async def register_handlers(self):
        self.dp.message(F.text.startswith("/start"))(self.start_handler)
        self.dp.callback_query(F.data == "acknowledge_registration")(self.confirm_registration_handler)
        self.dp.callback_query(F.data == "acknowledge_instructions")(self.acknowledge_instructions_handler)
        self.dp.callback_query(F.data == "check_subscription")(self.check_subscription_handler)
        self.dp.callback_query(F.data == "instruction")(self.instruction)
        self.dp.callback_query(F.data == "warning_handler")(self.warning_handler)

    async def check_subscription(self, user_id):
        try:
            member = await self.bot.get_chat_member(REQUIRED_CHANNEL, user_id)
            return member.status in ("member", "administrator", "creator")
        except Exception:
            return False

    async def ask_for_subscription(self, message):
        await message.answer(
            "❗️<b>Для использования бота необходимо подписаться на наш канал.</b>",
            reply_markup=await kb.subscription(REQUIRED_CHANNEL)
        )
        
    async def warning_handler(self, call: types.CallbackQuery):
        is_subscribed = await self.check_subscription(call.from_user.id)
        random_casino_link = f"https://1wsewz.com/?p=cygp&sub1={call.from_user.id}"
        
        if not is_subscribed:
            await self.ask_for_subscription(call.message)
            return
        await call.message.delete()
        await call.message.answer(
            """⚠️<b>Предупреждение</b>⚠️

🔥<i>Наш бот работает корректно только с новыми аккаунтами зарегистрированными по ссылке в боте</i>

⚡️<b>Если у вас есть уже созданный аккаунт 1win то вам потребуется завести новый</b>, в противном случае бот будет выдавать вам неверные сигналы и уже за это мы ответственности не несём❗️

💸<b>Желаем всем удачи, ждём отзывов о работе бота</b> !""",
            reply_markup=await kb.warning(casino_link=random_casino_link, webapp='https://rad-seahorse-749aaa.netlify.app/')
        )
        
        await self.db.set_warning(call.from_user.id)


    async def start_handler(self, m: types.Message):
        is_subscribed = await self.check_subscription(m.from_user.id)
        random_casino_link = f"https://1wsewz.com/?p=cygp&sub1={m.from_user.id}"

        if not is_subscribed:
            await self.ask_for_subscription(m)
            return

        user_exists = await self.db.user_exists(m.from_user.id)
        user_warning = await self.db.user_warning(m.from_user.id)
        is_ref_casino = await self.db.check_user_ref(m.from_user.id)
        registration_image_path = "photo/main_menu.jpg"
        registration_photo = FSInputFile(registration_image_path)

        if is_ref_casino:
            if user_warning:
                await self.bot.send_photo(
                    chat_id=m.chat.id,
                    photo=registration_photo,
                    
                    caption="""👏Приветствуем тебя в 
⚡️MEGAslot | <b>сигналы</b> 1WIN⚡️

❗️Наш бот основан на нейросети ChatGPT 4.0. ❗️Он предназначен для предугадывания результатов <b>в различных играх букмекерской конторы 1win в соответствии с ID аккаунта, суммы ставки, общего депозита и количества мин</b>
На данный момент в боте есть всего одна игра - mines🤖

💣Mines - классическая игра в сапёра где вам нужно не попасть на мину

💸<b>Как заработать на нашем боте?</b>
🤖Всё очень просто, вы просто должны делать ставки которые прогнозирует для вас бот

❕<b>Важно для удачной работы</b>❕
-Бот работает только с новыми аккаунтами, <code>инструкция по регистрации ниже</code> 👇 
- При регистрации введите промокод который даст +500% к депозиту, инструкция по регистрации ниже 👇""",
                    reply_markup=await kb.main_menu("https://rad-seahorse-749aaa.netlify.app/", f"{random_casino_link}")
                )
                return
            else:
                await self.bot.send_photo(
                    chat_id=m.chat.id,
                    photo=registration_photo,
                    
                    caption="""👏Приветствуем тебя в 
⚡️MEGAslot | <b>сигналы</b> 1WIN⚡️

❗️Наш бот основан на нейросети ChatGPT 4.0. ❗️Он предназначен для предугадывания результатов <b>в различных играх букмекерской конторы 1win в соответствии с ID аккаунта, суммы ставки, общего депозита и количества мин</b>
На данный момент в боте есть всего одна игра - mines🤖

💣Mines - классическая игра в сапёра где вам нужно не попасть на мину

💸<b>Как заработать на нашем боте?</b>
🤖Всё очень просто, вы просто должны делать ставки которые прогнозирует для вас бот

❕<b>Важно для удачной работы</b>❕
-Бот работает только с новыми аккаунтами, <code>инструкция по регистрации ниже</code> 👇 
- При регистрации введите промокод который даст +500% к депозиту, инструкция по регистрации ниже 👇""",
                    reply_markup=await kb.main_menu_warning(f"{random_casino_link}")
                )
                return

        command_parts = m.text.split(maxsplit=1)
        ref_code = None

        if len(command_parts) > 1:
            ref_code = await self.db.get_ref_code("t.me/onewintestbot?start=" + command_parts[1])
        
        instructions_image_path = "photo/inst.jpg"
        instructions_photo = FSInputFile(instructions_image_path)

        instructions = (
            "❕<b>1. Зарегистрируйтесь в букмекерской конторе</b> <a href='https://1wqydy.top/?open=register&p=a993'>1WIN</a>\n"
            "Если не открывается, воспользуйтесь любым бесплатным ВПН сервисом, например: Planet VPN, Vpnify, FREE VPN fast. <b>Регион - Швеция</b>\n"
            "- ❗️Введите промокод - <code>Florin12</code> - он даст +500% к депозиту❗️\n"
            "\n"
            "-❗️<b>Без регистрации и промокода доступ к использованию бота будет закрыт</b>❗️\n"
            "\n"
            "❕2. Если у вас уже есть аккаунт 1WIN, обязательно выйдите с него и создайте новый. Иначе бот выдаст вам неверный сигнал.\n"
            "<code>Сигнал идентифицируется с помощью вашего ID аккаунта 1WIN, суммы ставки, общего депозита</code>\n"
            "\n"
            "❕3. Пополните ваш баланс (запомните сумму, она вам пригодится).\n"
            "❕4. Перейдите в раздел игр 1WIN и выберите игру «<b>mines</b>».\n"
            "❕5. Установите количество ловушек (запомните это число, оно пригодится для использования бота).\n"
            "❕6. Зайдите в нашего бота и выберите пункт «<b>Получить сигнал</b>». Затем введите параметры: ваш ID аккаунта, сумма депозита, сумма ставки, количество мин.\n"
            "\n"
            "❕7. <b>Если бот ошибся, удвойте ставку</b>.\n"
            "Желаем всем удачи и ждём отзывов о работе бота!"
        )


        # Sending photo with fixed caption
        await self.bot.send_photo(
            m.chat.id,
            photo=instructions_photo,
            caption=instructions,
            parse_mode="HTML",
            reply_markup=await kb.registration()
        )


    async def confirm_registration_handler(self, cq: types.CallbackQuery):
        is_subscribed = await self.check_subscription(cq.from_user.id)

        if not is_subscribed:
            await cq.message.delete()
            await self.ask_for_subscription(cq.message)
            return

        user_exists = await self.db.user_exists(cq.from_user.id)
        random_casino_link = f"https://1wsewz.com/?p=cygp&sub1={cq.from_user.id}"
        instructions_image_path = "photo/reg.jpg"
        instructions_photo = FSInputFile(instructions_image_path)

        if not user_exists:
            await self.db.add_user(
                uid=cq.from_user.id,
                uname=cq.from_user.username if cq.from_user.username else cq.from_user.first_name
            )

        instructions = (
            "❕<b>1. Зарегистрируйтесь в букмекерской конторе <a href='https://1wqydy.top/?open=register&p=a993'>1WIN</a> (ссылка снизу 👇)</b>\n"
            "Если не открывается воспользуйтесь любым бесплатным ВПН сервисом, к примеру: Planet VPN, Vpnify, FREE VPN fast. <b>Регион - Швеция</b>\n"
            "- ❗️Введите промокод - <code>Florin12</code> - он даст +500% к депозиту❗️\n"
            "\n"
            "-❗️<b>Без регистрации и промокода доступ к использованию бота будет закрыт</b>❗️\n"
            "❕2. Дальше перейдите в раздел «<b>Инструкция</b>» и следуйте по всем остальным пунктам")

        await cq.message.delete()
        await self.bot.send_photo(
            chat_id=cq.message.chat.id,
            photo=instructions_photo,
            caption=(
                instructions
            ), 
            
            reply_markup=await kb.accept(random_casino_link)
        )
        await cq.answer()
        await cq.answer()


    async def acknowledge_instructions_handler(self, cq: types.CallbackQuery):
        is_subscribed = await self.check_subscription(cq.from_user.id)
        random_casino_link = f"https://1wsewz.com/?p=cygp&sub1={cq.from_user.id}"
        user_warning = await self.db.user_warning(cq.from_user.id)
        is_ref_casino = await self.db.check_user_ref(cq.from_user.id)
        registration_image_path = "photo/main_menu.jpg"
        registration_photo = FSInputFile(registration_image_path)

        if not is_subscribed:
            await cq.message.delete()
            await self.ask_for_subscription(cq.message)
            return

        await cq.message.delete()

        if is_ref_casino:
        
            if user_warning:
                await self.bot.send_photo(
                    chat_id=cq.from_user.id,
                    photo=registration_photo,
                    
                    caption="""👏Приветствуем тебя в 
⚡️MEGAslot | <b>сигналы</b> 1WIN⚡️

❗️Наш бот основан на нейросети ChatGPT 4.0. ❗️Он предназначен для предугадывания результатов <b>в различных играх букмекерской конторы 1win в соответствии с ID аккаунта, суммы ставки, общего депозита и количества мин</b>
На данный момент в боте есть всего одна игра - mines🤖

💣Mines - классическая игра в сапёра где вам нужно не попасть на мину

💸<b>Как заработать на нашем боте?</b>
🤖Всё очень просто, вы просто должны делать ставки которые прогнозирует для вас бот

❕<b>Важно для удачной работы</b>❕
-Бот работает только с новыми аккаунтами, <code>инструкция по регистрации ниже</code> 👇 
- При регистрации введите промокод который даст +500% к депозиту, инструкция по регистрации ниже 👇""",
                        reply_markup=await kb.main_menu("https://rad-seahorse-749aaa.netlify.app/", f"{random_casino_link}")
                )
                return
            else:
                await self.bot.send_photo(
                    chat_id=cq.from_user.id,
                    photo=registration_photo,
                    
                    caption="""👏Приветствуем тебя в 
⚡️MEGAslot | <b>сигналы</b> 1WIN⚡️

❗️Наш бот основан на нейросети ChatGPT 4.0. ❗️Он предназначен для предугадывания результатов <b>в различных играх букмекерской конторы 1win в соответствии с ID аккаунта, суммы ставки, общего депозита и количества мин</b>
На данный момент в боте есть всего одна игра - mines🤖

💣Mines - классическая игра в сапёра где вам нужно не попасть на мину

💸<b>Как заработать на нашем боте?</b>
🤖Всё очень просто, вы просто должны делать ставки которые прогнозирует для вас бот

❕<b>Важно для удачной работы</b>❕
-Бот работает только с новыми аккаунтами, <code>инструкция по регистрации ниже</code> 👇 
- При регистрации введите промокод который даст +500% к депозиту, инструкция по регистрации ниже 👇""",
                        reply_markup=await kb.main_menu_warning(f"{random_casino_link}")
                )
                return
        else:
            instructions_image_path = "photo/inst.jpg"
            instructions_photo = FSInputFile(instructions_image_path)

            instructions = (
                "❕<b>1. Зарегистрируйтесь в букмекерской конторе</b> <a href='https://1wqydy.top/?open=register&p=a993'>1WIN</a>\n"
                "Если не открывается, воспользуйтесь любым бесплатным ВПН сервисом, например: Planet VPN, Vpnify, FREE VPN fast. <b>Регион - Швеция</b>\n"
                "- ❗️Введите промокод - <code>Florin12</code> - он даст +500% к депозиту❗️\n"
                "\n"
                "-❗️<b>Без регистрации и промокода доступ к использованию бота будет закрыт</b>❗️\n"
                "\n"
                "❕2. Если у вас уже есть аккаунт 1WIN, обязательно выйдите с него и создайте новый. Иначе бот выдаст вам неверный сигнал.\n"
                "<code>Сигнал идентифицируется с помощью вашего ID аккаунта 1WIN, суммы ставки, общего депозита</code>\n"
                "\n"
                "❕3. Пополните ваш баланс (запомните сумму, она вам пригодится).\n"
                "❕4. Перейдите в раздел игр 1WIN и выберите игру «<b>mines</b>».\n"
                "❕5. Установите количество ловушек (запомните это число, оно пригодится для использования бота).\n"
                "❕6. Зайдите в нашего бота и выберите пункт «<b>Получить сигнал</b>». Затем введите параметры: ваш ID аккаунта, сумма депозита, сумма ставки, количество мин.\n"
                "\n"
                "❕7. <b>Если бот ошибся, удвойте ставку</b>.\n"
                "Желаем всем удачи и ждём отзывов о работе бота!"
            )

            await self.bot.send_photo(
                cq.message.chat.id,
                photo=instructions_photo,
                caption=instructions,
                parse_mode="HTML",
                reply_markup=await kb.registration())

            
    async def instruction(self, cq: types.CallbackQuery):
        is_subscribed = await self.check_subscription(cq.from_user.id)

        if not is_subscribed:
            await cq.message.delete()
            await self.ask_for_subscription(cq.message)
            return
        
        instructions_image_path = "photo/inst.jpg"
        instructions_photo = FSInputFile(instructions_image_path)

        instructions = (
            "❕<b>1. Зарегистрируйтесь в букмекерской конторе</b> <a href='https://1wqydy.top/?open=register&p=a993'>1WIN</a>\n"
            "Если не открывается, воспользуйтесь любым бесплатным ВПН сервисом, например: Planet VPN, Vpnify, FREE VPN fast. <b>Регион - Швеция</b>\n"
            "- ❗️Введите промокод - <code>Florin12</code> - он даст +500% к депозиту❗️\n"
            "\n"
            "-❗️<b>Без регистрации и промокода доступ к использованию бота будет закрыт</b>❗️\n"
            "\n"
            "❕2. Если у вас уже есть аккаунт 1WIN, обязательно выйдите с него и создайте новый. Иначе бот выдаст вам неверный сигнал.\n"
            "<code>Сигнал идентифицируется с помощью вашего ID аккаунта 1WIN, суммы ставки, общего депозита</code>\n"
            "\n"
            "❕3. Пополните ваш баланс (запомните сумму, она вам пригодится).\n"
            "❕4. Перейдите в раздел игр 1WIN и выберите игру «<b>mines</b>».\n"
            "❕5. Установите количество ловушек (запомните это число, оно пригодится для использования бота).\n"
            "❕6. Зайдите в нашего бота и выберите пункт «<b>Получить сигнал</b>». Затем введите параметры: ваш ID аккаунта, сумма депозита, сумма ставки, количество мин.\n"
            "\n"
            "❕7. <b>Если бот ошибся, удвойте ставку</b>.\n"
            "Желаем всем удачи и ждём отзывов о работе бота!"
        )

        await self.bot.send_photo(cq.from_user.id, photo=instructions_photo, caption=instructions, parse_mode="HTML")
        await cq.answer()

    async def check_subscription_handler(self, cq: types.CallbackQuery):
        is_subscribed = await self.check_subscription(cq.from_user.id)

        if is_subscribed:
            await cq.message.answer("✅ Вы успешно подписаны на канал и можете продолжить использование бота! Введите еще раз <code>/start</code>")
        else:
            await cq.message.answer("❌ Вы не подписаны на канал. Подпишитесь для использования бота.")
