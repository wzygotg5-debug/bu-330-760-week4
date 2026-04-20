# Week 4 Starter: Math Agent

A ReAct agent that solves questions using tool calls.

## Video Walkthrough
https://youtu.be/CyG9EXWI3_g

## Setup

Install uv if you don't have it.

Copy .env.example to .env and add your API key:

cp .env.example .env

Then edit .env and replace your-key-here with your API key.

To use a different provider, change the MODEL variable in agent.py and set the matching key in .env.

Make sure .env is in your .gitignore so you don't commit your key.

## Run

uv run agent.py

uv will install dependencies automatically on first run.

The agent will work through each question in math_questions.md and print the ReAct trace (Reason / Act / Result) for each one.

## Files

agent.py - the ReAct agent
calculator.py - calculator tool
products.json - product catalog with prices
math_questions.md - the questions the agent solves
.env.example - template for your API key
