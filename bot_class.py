import json, requests, datetime
                        
class WABot():
    def __init__(self, json):
        self.json = json
        self.dict_messages = json['messages']
        self.APIUrl = 'https://eu41.chat-api.com/instance12345/'
        self.token = 'abcdefg'
        
    def send_requests(self, method, data):
        url = f"{self.APIUrl}{method}?token={self.token}"
        headers = {'Content-type': 'application/json'}
        answer = requests.post(url, data=json.dumps(data), headers=headers)
        return answer.json()
    
    def send_message(self, chatId, text):
        data = {"chatId" : chatId,
                "body" : text}
        answer = self.send_requests('sendMessage', data)
        return answer
    
    def welcome(self,chatId, noWelcome = False):
        welcome_string = ''
        if (noWelcome == False):
            welcome_string = "WhatsApp Demo Bot Python\n"
        else:
            welcome_string = """Incorrect command
            Commands:
            1. chatId - show ID of the current chat
            2. time - show server time
            3. me - show your nickname
            4. file [format] - get a file. Available formats: doc/gif/jpg/png/pdf/mp3/mp4
            5. ptt - get a voice message
            6. geo - get a location
            7. group - create a group with the bot"""
        return self.send_message(chatId, welcome_string)
    
    def show_chat_id(self,chatId):
        return self.send_message(chatId, f"Chat ID : {chatId}")
    
    def me(self, chatId, name):
        return self.send_message(chatId, name)
    
    def processing(self):
        if self.dict_messages != []:
            for message in self.dict_messages:
                text = message['body'].split()
                if not message['fromMe']:
                    id  = message['chatId']
                    if text[0].lower() == 'hi':
                        return self.welcome(id)
                    elif text[0].lower() == 'time':
                        return self.time(id)
                    elif text[0].lower() == 'chatId':
                        return self.show_chat_id(id)
                    elif text[0].lower() == 'me':
                        return self.me(id, message['senderName'])
                    elif text[0].lower() == 'file':
                        return self.file(id, text[1])
                    elif text[0].lower() == 'ptt':
                        return self.ptt(id)
                    elif text[0].lower() == 'geo':
                        return self.geo(id)
                    elif text[0].lower() == 'group':
                        return self.group(message['author'])
                    else:
                        return self.welcome(id, True)
                else: return 'NoCommand'