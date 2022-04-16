import wamsg
import re

with open("WhatsApp Chat with My Friend.txt", "r", encoding='utf-8') as f:
    list2 = []
    for item in f:
        number = 0
        list2.append(item)
print(list2)

date_format = "^[0-9]+/[0-9]+/[0-9]+"
time_format = "[0-9]+\:[0-9]+ ?[AP]?M? -"
sender_format = "-.+?\:"
for item in list2:
    try:
        date_group = re.search(date_format, item).group()
        time_re = re.search(time_format, item)
        time_group = time_re.group().strip(' - ')
        sender = re.search(sender_format, item).group().strip(':').strip('- ')
        message = re.search(f"{sender}\:.*", item).group().strip(f"{sender}: ")
        print(f'Date: {date_group} Time: {time_group} Sender: {sender} Message: {message}')
    except:
        print("no date on this line")
