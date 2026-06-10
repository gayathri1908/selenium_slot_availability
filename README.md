⏰ Slot Availability Automation using Selenium
📌 Overview

This project is a Python-based automation tool that continuously monitors slot availability on booking websites and sends instant email notifications when slots become available. It helps users quickly act on limited-time booking opportunities without manually refreshing pages.

🚀 Features
Automatically checks slot availability at regular intervals
Detects real-time changes in availability status (Available / Not Available)
Sends instant email alerts when slots are found
Runs in headless/browser automation mode using Selenium

🛠️ Tech Stack
Python
Selenium
ChromeDriver
SMTP (Email Automation)
Web Automation

⚙️ How It Works
The script opens the target booking website using Selenium
It continuously monitors the slot availability section
When a slot becomes available, it triggers an alert system
An email notification is sent to the user instantly

📧 Email Alert System
Uses Python’s SMTP library
Sends real-time notifications with slot status updates
Ensures users don’t miss booking opportunities

🎯 Future Improvements
Add Telegram/WhatsApp notifications
Deploy as a cloud-based scheduler
Improve UI for selecting different booking sites
Add database logging for slot history
