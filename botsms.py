import telegram
import requests
import datetime
import time
from telegram.ext import Updater, CommandHandler
import multiprocessing


bot_token = '6161077804:AAFB_xauU7pIWL6Kglx3NcWZEVfNytbqQXQ'
bot = telegram.Bot(token=bot_token)
def sms(update, context):
    # Kiểm tra xem thời gian giữa các lần sử dụng lệnh có đủ lớn không
    current_time = time.time()
    last_used_time = context.user_data.get('last_used_time', 0)
    if current_time - last_used_time < 30: # 300 giây = 5 phút
        # Thông báo cho người dùng rằng còn ... giây nữa mới có thể tiếp tục sử dụng lệnh
        remaining_time = int(30 - (current_time - last_used_time))
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Bạn cần đợi {remaining_time} giây trước khi sử dụng lại lệnh.")
        return
    phone_number = context.args[0]
    url1 = "https://kid.io.vn/api/10api.php?phone={}&key=khenglee".format(phone_number)
    url2 = "https://kid.io.vn/api/10api.php?phone={}&key=khenglee".format(phone_number)

    response1 = requests.get(url1)
    response2 = requests.get(url2)

    update.message.reply_text(text=response1.text)
    context.user_data['last_used_time'] = current_time
def reply(update, context):
    message = update.message.text.lower()
    chat_id = update.message.chat_id

    if 'spam đâu vậy' in message:
        bot.send_message(chat_id=chat_id, text='soạn tin nhắn /sms sdt')
    elif 'spam như nào' in message:
        bot.send_message(chat_id=chat_id, text='soạn tin nhắn /sms sdt')
    else:
        bot.send_message(chat_id=chat_id, text='Xin lỗi, tôi không hiểu câu hỏi của bạn.')
def main():
    updater = Updater(bot_token, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('sms', sms))
    dispatcher.add_handler(CommandHandler('grant', grant_permission))
    updater.start_polling()
    updater.idle()
    # Bắt đầu một tiến trình giám sát bot
    monitor_process = multiprocessing.Process(target=monitor_bot, args=(updater,))
    monitor_process.start()

    updater.idle()

def monitor_bot(updater):
    while True:
        # Kiểm tra trạng thái hoạt động của bot
        if not updater.is_running:
            print('Bot is not running. Restarting...')
            updater.start_polling()

        time.sleep(10)  # Chờ 10 giây trước khi kiểm tra lại
def grant_permission(update, context):
    user_id = update.message.from_user.id
    permissions = telegram.ChatPermissions(can_send_messages=True)
    context.bot.restrict_chat_member(chat_id=update.effective_chat.id, user_id=user_id, permissions=permissions)
    update.message.reply_text('Bạn đã được cấp quyền sử dụng lệnh /sms mà không cần đợi thời gian giữa các lần sử dụng.')
if __name__ == '__main__':
    main()
