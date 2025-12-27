# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Telegram bot for Russian history EGE (Unified State Exam) preparation. Users select a topic, answer multiple-choice questions, and receive instant feedback.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the bot
python main.py
```

## Architecture

Single-file bot (`main.py`) built with aiogram 3.x using FSM (Finite State Machine) for conversation flow.

**State machine flow:**
1. `choosing_topic` - User selects a topic from inline keyboard
2. `answering` - User answers shuffled questions from selected topic

**Data source:** Questions loaded from `fic.xlsx` Excel file at startup. Each sheet represents a topic. Row format: Question | Option1 | Option2 | Option3 | Option4 | CorrectAnswer

**Key components:**
- `QuizState` - FSM states for conversation management
- `load_quiz_from_xlsx()` - Parses Excel sheets into topic-keyed question dictionaries
- `QUIZ_DATA` - Global dict holding all questions, loaded once at startup

## Dependencies

- `aiogram` - Telegram Bot API framework (async)
- `openpyxl` - Excel file parsing
