# DOBROFOOT_BOT

### Created by Ivan Gavrilov

------  
#### ***Task Description:***  
***This Telegram bot is designed for automated and interactive organization of meetings. It will help users find out about the nearest meeting, sign up for football, top up and find out their balance.
For the role of administrators, the bot allows you to create training sessions and monitor the personal accounts of all users***  
_________  
### _Requirements_ 
Python version 3.8 or higher and the following modules are required for the bot to work correctly:  
```  
certifi==2024.2.2  
charset-normalizer==3.3.2  `
colorama==0.4.6  
idna==3.7  
loguru==0.7.2  
pyTelegramBotAPI==4.17.0  
python-decouple==3.6  
requests==2.31.0  
urllib3==2.2.1  
win32-setctime==1.1.0
```  
---  
### _Bot's file composition_  
The bot uses polling technology, so no additional server configuration is required.  
The following files are used in the bot:  
* main.py - main file for bot's work  
* messages.py - file containing functions for outputting various bot messages
* keyboards.py - file with functions for creating keyboards for working with the bot
* db_funcs.py -  file containing functions for CRUD concept of working with SQLite3 database
* class_user.py - file containing user, payment and training classes to initialize and foratize them before writing them to the database
* .env - file containing the token for connecting the bot to Telegram servers and link for payment. This file should be created manually and the token obtained with @BotFather should be added to it.
* requirements.txt - list of required modules and dependencies
---  
### _Preparing for start bot_  
For the bot to function, you first need to register the bot in Telegram using @BotFather.  
The received tokens should be located in the ".env" file: 
* football_bot = 'token received from @BotFather in Telegram'
* payment_link = 'payment link from bank account'
---  
### _Start bot_  
1. Virtual environment creation:  
``` 
python -m venv venv  
```  
  
2. Virtual environment activation on Windows:
```  
cd venv\Scripts\activate 
```  
  
3. Installing requirements:  
```  
pip install -r requirements.txt   
```  
  
4. Starting bot:  
```  
python main.py  
```  
---
### _After the start, the bot will start functioning in Telegram under the name [dobrofoot_bot](https://t.me/dobrofoot_bot)_

---  
### _Bot's command list:_ 
- /help - Help with bot commands
- /training_info - Information about the next training session
- /training - Sign up for training
- /balance - View your balance
- /pay - Refill your balance or pay for a training session

_For administrators:_
- /new_training - Create a new training session
- /confirm_payments - Confirm new payments
- /confirm_training - Confirm completion of the last training session
- /active_subscription - Activate subscription for a user
- /users - Get a list of all users
- /payments - Get a list of all payments
---
### If you have any questions about the bot you can write to me [@gavril_23](https://t.me/gavril_23)

---
