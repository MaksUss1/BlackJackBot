from aiogram import Bot, Dispatcher, executor, types
from random import choice

bot = Bot('6006107342:AAFGXOXmF5FPOUN0C6y6vbdMC11nJ3INGOg')
dp = Dispatcher(bot)

coloda = {2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 'J': 2, 'Q': 3, 'K': 4, 'A': 11}

player = list
player_sum = int
ai = list
ai_sum = int


async def play(message):
    global player, ai, player_sum, ai_sum

    player = [choice(list(coloda)) for _ in range(2)]
    player_sum = sum([coloda[x] for x in player])
    ai = [choice(list(coloda)) for _ in range(2)]
    ai_sum = sum([coloda[x] for x in ai]) if player else 0

    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton('взять карту'), types.KeyboardButton('вскрыться'))

    await message.answer(f'карты врага: ***** (*****)\nтвои карты: {player} ({player_sum})', reply_markup=markup)


async def get_card(message):
    global player, player_sum

    if player: player.append(choice(list(coloda)))
    player_sum = sum([coloda[x] for x in player]) if player else 0

    await message.answer(f'карты врага: ***** (*****)\nтвои карты: {player} ({player_sum})')


async def view(message):
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton('играть'))
    await message.answer(f'карты врага: {ai} ({ai_sum})\nтвои карты: {player} ({player_sum})', reply_markup=markup)
    if ai_sum > player_sum or player_sum > 21:
        await message.answer('поражение :(')
    elif player_sum > ai_sum or ai_sum > 21:
        await message.answer('победа :)')
    else:
        await message.answer('ничья :/')


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton('играть'))

    await message.answer('Чтобы начать играть введи "играть"', reply_markup=markup)


@dp.message_handler()
async def main(message: types.Message):
    if message.text == 'играть':
        await play(message)
    elif message.text == 'взять карту':
        await get_card(message)
    elif message.text == 'вскрыться':
        await view(message)

executor.start_polling(dp)
