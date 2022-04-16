import wamsg
import re
import sys
import codecs
import os
import shutil

def import_message_file(filename):
    with codecs.open(filename, "r", encoding='utf-8') as f:
        text_lines = []
        for item in f:
            text_lines.append(item)
    return text_lines


def extract_messages_from_text(text_lines):
    date_format = "^[0-9]+/[0-9]+/[0-9]+"
    time_format = "([01]?[0-9]|2[0-3])\.[0-5][0-9]"
    sender_format = "-.+?\:"

    message_suffix = ""
    messages = []

    for item in reversed(text_lines):
        if len(item) > 0:
            try:
                date_group = re.search(date_format, item).group()
                time_group = re.search(time_format, item).group()
                sender = re.search(sender_format, item).group().strip(':').strip('- ')
                text = item[re.search(sender_format, item).span()[1]+1:]
                # text = text.replace('<','').replace('>','')
                if "<Media omitted>" in text:
                    text = text.replace("<Media omitted>", "Media omitted")
                text = text.replace('IMG-','<img src="IMG-')
                text = text.replace('.jpg','.jpg" width=280>')
                text = text.replace('PTT-','<audio controls src="PTT-')
                text = text.replace('.opus','.opus">')
                messages.append(wamsg.WAMSG(date_group, time_group, sender, text))
                message_suffix = ""
            except:
                message_suffix += (" " + item).strip('\n')
    return list(reversed(messages))

"""<audio
  src="AudioTest.ogg"
  autoplay>
  Your browser does not support the <code>audio</code> element.
</audio>"""


def display_messages(messages):
    for msg in messages:
        print(f'Date: {msg.date} Time: {msg.time} Sender: {msg.sender} Message: {msg.text}')   
    
def generate_html(sender, messages):
    html_header = '<!DOCTYPE html>\n<html>\n<head>\n<link rel="stylesheet" href="imessage.css">\n</head>\n<body>\n'
    h1 = f'<h1>WhatsApp Chat with {sender}</h1>\n'
    chat_div_class = '<div class="chat">\n'
    me_div_class = '  <div class="mine messages">\n'
    remote_div_class = '  <div class="yours messages">\n'
    message_div_class = '    <div class="message last">\n'
    end_message_div = '     </div>\n'
    end_sender_div = '   </div>\n'
    end_chat_div = ' </div>\n'
    
    output_file_text = html_header
    output_file_text += h1
    output_file_text += chat_div_class

    
    for msg in messages:
        if sender in msg.sender:
            output_file_text += remote_div_class
        else:
            output_file_text += me_div_class
        output_file_text += message_div_class
        output_file_text += "      " + msg.text + '\n'
        output_file_text += end_message_div
        output_file_text += msg.date + " " + msg.time + "\n"
        output_file_text += end_sender_div
        
    output_file_text += end_chat_div

    return output_file_text

    
def export_file(filepath, html_text):
    output_file=codecs.open(filepath + "/" "chat.html",'w',"utf-8")
    output_file.write(html_text)
    output_file.close()

    
def main():
    full_path = sys.argv[1]
    filename = os.path.basename(full_path)
    filepath = os.path.dirname(full_path)

    print(filename)
    sender = filename.replace("WhatsApp Chat with ","").replace(".txt","")
    messages_list = import_message_file(full_path)
    messages = extract_messages_from_text(messages_list)
    # print("--------Messages List------------")
    # print(list(messages))
    # print("--------Messages------------")
    # display_messages(messages)
    # print("--------Messages List------------")
    # print(list(messages))
    html_text = generate_html(sender, messages)
    export_file(filepath, html_text)
    shutil.copy("imessage.css", filepath)
    
if __name__ == "__main__":
    main()