# watch-later

A "watch later" list you manage through a Telegram bot. Save video links with a
title, pull a random one when you're ready to watch, and remove it once you're
done — all backed by a small Rust API and a JSON file on disk.

## How it works

The project is split in two different services

- backend/ -- a Rust API (built with Axum) that stores videos as JSON and
exposes endpoints to add, fetch, and remove them.
- telegram_bot/ -- a Python Telegram Bot (built with aiogram) that talks
to the backend over HTTP and gives you a chat interface for managing your list.

```text
You (Telegram) -> telegram_bot (aiogram) -> backend (Axum API) -> data/videos.json
```

## Features

- add a video by sending a link and a title, guided step-by-step by the bot
- pull a random unwatched video from your list
- remove a watched video
- link validation

## Project Structure

```text
watch-later/
├── backend/           # Rust API server
│   ├── src/
│   │   ├── main.rs    # Axum app, routes, HTTP handlers
│   │   └── data.rs    # Video model, JSON persistence, business logic
│   └── Cargo.toml
├── telegram_bot/       # Python Telegram bot
│   ├── src/
│   │   └── tg_bot/
│   │       ├── main.py             # Entry point, bot polling
│   │       ├── config.py           # Settings, logging setup
│   │       ├── client.py           # HTTP client for the backend API
│   │       └── handlers/
│   │           ├── default_handlers.py     # /start, /stop
│   │           ├── add_video_handlers.py   # Add-video conversation flow
│   │           └── get_video_handler.py    # Random video / skip / remove flow
│   ├── logs/           # Bot log files (created automatically)
│   ├── pyproject.toml
│   └── uv.lock
├── data/                # JSON storage for videos (created automatically)
├── LICENSE
└── README.md
```

## Dependencies

- Rust and Cargo
- Python 3.11+ and uv for the bot
- A Telegram bot token from `@BotFather`

## Setup

### 0. Installation

```bash
git clone https://github.com/matgo1/watch-later.git
cd watch-later
```

### 1. Backend

```bash
cd backend
cargo run
```

*or*

```bash
cd backend
cargo build --release
./target/release/watch-later
```

By default, the API runs at `http://127.0.0.1:3000`

### 2. Telegram bot

Create a `.env` inside `telegram_bot/` with your bot token:

```env
BOT_TOKEN=your_telegram_bot_token_here
```

Then install dependencies and run the bot:

```bash
cd ../telegram_bot
uv sync
uv run bot
```

> Make sure the backend is running first -- the bot depends on it for all
> video operations

## Usage

Once both services are running, open a cat with your bot on Telegram:

| Command    | What it does         |
|:-----------|:---------------------|
| `/start`   | Activates the bot    |
| `/stop`    | Deactivates the bot  |
| `/add`     | Add a video          |
| `/get_ran` | Shows a random video |

When viewing a random video, you can:

- **Choose the video** -- removes it from the list (marking as watched)
- **Skip** -- shows another random video instead

## Backend API

| Method | Endpoint  | Description                                            |
|--------|-----------|--------------------------------------------------------|
| `GET`  | `/random` | Returns a random saved video                           |
| `POST` | `/add`    | Adds a new video (`{ "title": "...", "link": "..." }`) |
| `POST` | `/remove` | Removes a video by its link (raw JSON string body)     |

Videos are stored as pretty-printed JSON in `data/videos.json`,
created automatically on first run.

## Tech Stack

### Backend

- axum -- web framework
- tokio -- async runtime
- serde / serde_json -- JSON serialization
- rand -- random video selection

### Telegram bot

- aiogram -- Telegram Bot API framework
- aiohttp -- async HTTP client for talking to the backend
- pydantic-settings -- environment-based configuration
- uv -- dependency manager

## TODO

- Make video not show twice when cycle
- Make databases and place on server so you don't need to download bot to use

## License

GNU General Public License v3.0
