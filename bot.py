import telebot, json, os
from telebot import types
TOKEN = "8786421089:AAE9lt5ZQ5OhPSf6KS49lgnNopabA-5Yn0U"
ADMIN_ID = 8717647733
SHAM_CODE = "fe5af1fd68feb771a6e80921a9f3e3a3"
FIVESIM_ID = "4613891"
bot = telebot.TeleBot(TOKEN, parse_mode="Markdown")
BAL_FILE = "balances.json"
def load_bal():
    if os.path.exists(BAL_FILE):
        try: return json.load(open(BAL_FILE, encoding='utf-8'))
        except: return {}
    return {}
def save_bal(d): json.dump(d, open(BAL_FILE, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
balances = load_bal()
def main_kb():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.add("📱 ارقام واتساب","✈️ ارقام تلجرام","🎮 شحن 42 لعبة","💻 شحن البرامج","📸 رشق انستا متابعين","❤️ رشق انستا لايكات","🎵 رشق تيك توك","🟧 رشق كواي","📢 رشق قنوات واتساب","✅ توثيق تلجرام","💰 شحن شام كاش","👤 رصيدي")
    return kb
@bot.message_handler(commands=['start'])
def start(m):
    uid=str(m.from_user.id)
    if uid not in balances: balances[uid]=0; save_bal(balances)
    bot.send_message(m.chat.id, f"🌟 Amar Store - ID {FIVESIM_ID}\n💰 رصيدك {balances.get(uid,0)}$\n20 خدمة", reply_markup=main_kb())
@bot.message_handler(func=lambda m: True)
def handler(m):
    uid=str(m.from_user.id); txt=m.text or ""
    if SHAM_CODE in txt:
        nums=[float(s) for s in txt.replace('$',' ').split() if s.replace('.','',1).isdigit()]; amount=nums[-1] if nums else 0
        if amount>0:
            bot.send_message(m.chat.id, f"📩 استلمنا {amount}$ قيد المراجعة")
            bot.send_message(ADMIN_ID, f"💰 شحن من {m.from_user.id}\n{txt}\n/add {m.from_user.id} {amount}")
    else:
        if uid!=str(ADMIN_ID): bot.send_message(ADMIN_ID, f"رسالة من {m.from_user.id}: {txt}")
        bot.send_message(m.chat.id, "✅ تم")
@bot.message_handler(commands=['add'])
def add_cmd(m):
    if m.from_user.id!=ADMIN_ID: return
    try:
        _, target, amount = m.text.split(); amount=float(amount); balances[target]=balances.get(target,0)+amount; save_bal(balances)
        bot.send_message(m.chat.id, f"✅ شحنت {amount}$")
        bot.send_message(int(target), f"✅ شحنت {amount}$ - الجديد {balances[target]}$")
    except Exception as e: bot.send_message(m.chat.id, f"{e}")
bot.infinity_polling()
