import sys
import time
import telepot

import math
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.loop import MessageLoop

numbers={}
cntr=0
flagOfDo=0
result=1

def handle(msg):
    global flagOfLevel
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='احسب', callback_data='1')]
    ])
    content_type, chat_type, chat_id = telepot.glance(msg)
#    print(msg)

    global flagOfDo
    global cntr
    global result
    
    if msg['text']=='/start':
        bot.sendMessage(chat_id,"(Tmax in motor indction)🧲مرحبا بك😇 في بوت حاسبة اعظم عزم للماطور الحثي"
"\n (E1=400/√3 ) :الجهد التطبيقي  في سوال يكون لاين لذلك يجب تحويلة للفيز  \n"        
"\nقانون السرعة التزامنية :Ns=120*Fs/p \n"
"\n (E2=K*E1 ) :ستنادستيل أي أم أف المحتثة  \n"
"\n (Tmax=3/2⨉πNs⨉E2^2/2⨉X2 ) :قانون اعظم عزم  \n"
"\nمطور البوت:@taher_ja9👨‍💻\n"
"\n هيا لنبدا 👇👇\n"
"\n (fs)الان أرسل التردد\n")

        flagOfDo=1
        cntr=0
        return
        
    numbers[cntr]=float(msg['text'])
    
    if cntr==4:
        bot.sendMessage(chat_id,'اضغط على احسب , وذا جنت بمجموعة راقب خاص',reply_markup=keyboard)
        cntr=0
        result=0
    
    if result==1:
        if flagOfDo==1:
            bot.sendMessage(chat_id,'(Number Of Poles 🅿) :ارسل عدد الأقطاب ')
            flagOfDo=2
            cntr=1
            return
    if result==1:
        if flagOfDo==2:
            bot.sendMessage(chat_id,'(ratio of stator to rotor turns"K" )أرسل  نسبة الجزء الثابت الى متحرك ')
            flagOfDo=3
            cntr=2
            return  
    if result==1:
        if flagOfDo==3:
            bot.sendMessage(chat_id,': (E1) أرسل قيمة فولطية الفيز')
            flagOfDo=4
            cntr=3
            return  
    if result==1:
        if flagOfDo==4:
            bot.sendMessage(chat_id,': (X2)إرسل قيمة الممانعة ')
            flagOfDo=0
            cntr=4
            return
        else:
            bot.sendMessage(chat_id,'أرسل التردد f  تردد مرات ثابت 50 ')
            flagOfDo=1
            return
#     bot.sendMessage(chat_id, message)




def on_callback_query(msg):
	
    query_id, from_id, query_data=telepot.glance(msg, flavor='callback_query')    
    #    print(msg)
    global result
    global numbers

    if query_data=='0':
        bot.sendMessage(from_id,'لتحديث بوت اضغط /start',reply_markup=keyboard)
        numbers={}
        
    elif query_data=='1':
        bot.sendMessage(from_id,'Tmax: ''=' + str((3)/((6.28)*((120*numbers[0])/(numbers[1])/60))*((math.pow(((numbers[3])/(math.sqrt(3))/numbers[2]),2))/(2*numbers[4]))))
        bot.sendMessage(from_id,'لتحديث بوت اضغط /start')
        result=1
        numbers={}
        
    else:
        bot.sendMessage(from_id,'أعد المحاولة')
        result=1
        bot.sendMessage(from_id,'لتحديث بوت اضغط /start')
       	   
bot = telepot.Bot('2105639269:AAF0R2xtnq6uB72kFSEkEirR814CxqbY9Q0')
MessageLoop(bot, {'chat': handle,
                  'callback_query': on_callback_query}).run_as_thread()
print ('Listening ...')

while 1:
    time.sleep(10)

    # dispatcher.add_error_handler(error_callback)

    if WEBHOOK:
        LOGGER.info("Using webhooks.")
        updater.start_webhook(listen="0.0.0.0",
                              port=PORT,
                              url_path=TOKEN)

        if CERT_PATH:
            updater.bot.set_webhook(url=URL + TOKEN,
                                    certificate=open(CERT_PATH, 'rb'))
        else:
            updater.bot.set_webhook(url=URL + TOKEN)

    else:
        LOGGER.info("Using long polling.")
        updater.start_polling(timeout=15, read_latency=4, clean=True)

    updater.idle()


if __name__ == '__main__':
    LOGGER.info("Successfully loaded modules: " + str(ALL_MODULES))
    main()
