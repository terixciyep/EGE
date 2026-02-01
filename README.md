# EGE

Telegram bot for Russian history EGE exam preparation.

## Features
- `/start` - Select a topic and start the quiz
- Answer questions from the selected topic
- Get instant feedback on your answers

## Requirements
- Python 3.11+
- Telegram bot token

## Setup

1. Clone the repository
2. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
3. Edit `.env` and add your bot token:
   ```env
   BOT_TOKEN=your_bot_token_here
   ```
4. (Optional) Add channel ID for subscription check:
   ```env
   # Числовой ID канала (обязательно числовой формат)
   REQUIRED_CHANNEL_ID=-1001234567890

   # Ссылка на канал для кнопки подписки
   CHANNEL_LINK=https://t.me/your_channel
   ```

   **Как получить ID канала:**
   - Перешлите любое сообщение из канала боту @userinfobot
   - Или используйте бота @getmyid_bot (добавьте его в канал как админа)

## Run
```bash
pip install -r requirements.txt
python main.py
```
