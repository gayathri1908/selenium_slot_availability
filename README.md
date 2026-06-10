# 🎯 Selenium Slot Availability Monitor

Automatically monitors websites for available slots or tickets and sends an email alert the moment something opens up — no manual checking needed.

---

## 📌 What It Does

- Checks **BookMyShow** for movie/event ticket availability
- Checks **Apollo Hospitals** for doctor appointment slots
- Runs **silently in the background** (headless browser — no window opens)
- Sends an **instant email** the moment a slot or ticket becomes available
- Monitors **multiple sites simultaneously** using threads

---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/gayathri1908/selenium_slot_availability.git
cd selenium_slot_availability
```

### 2. Install dependencies
```bash
pip install selenium webdriver-manager
```

### 3. Configure your email

Open `monitor.py` and update these lines:
```python
SENDER_EMAIL        = "your_email@gmail.com"
SENDER_APP_PASSWORD = "your_app_password"   # Gmail App Password
RECEIVER_EMAIL      = "your_email@gmail.com"
```

> **How to get Gmail App Password:**
> Go to Google Account → Security → 2-Step Verification → App Passwords → Generate

### 4. Run
```bash
python monitor.py
```

---

## ⚙️ How It Works

```
monitor.py starts
    │
    ├── Thread 1 → Opens BookMyShow URL (headless)
    │               ↓ every 10 seconds
    │               Checks for: "Book Now", "Select Seats", "Buy Tickets"
    │               If found → sends email instantly ✅
    │
    └── Thread 2 → Opens Apollo URL (headless)
                    ↓ every 10 seconds
                    Checks for: time slots (9:00 AM, 10:30 AM etc.)
                    If found → sends email instantly ✅
```

---

## 📁 Project Structure

```
selenium_slot_availability/
│
├── monitor.py          # Main script — run this
└── README.md
```

---

## 🔧 Adding Your Own Sites

In `monitor.py`, add a new entry to the `SITES` list:

```python
SITES = [
    {
        "name"           : "My Site",
        "url"            : "https://example.com/booking",
        "type"           : "movie",    # or "doctor"
        "check_interval" : 10,         # seconds between checks
    },
]
```

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `selenium` | Browser automation |
| `webdriver-manager` | Auto-installs ChromeDriver |
| `smtplib` | Sending email alerts |
| `threading` | Monitor multiple sites at once |

---

## ⚠️ Notes

- Requires **Google Chrome** installed on your machine
- IRCTC is not supported — it blocks headless browsers with CAPTCHA
- Keep the terminal open while monitoring — script runs continuously until availability is found

---

## 👩‍💻 Author

**Gayathri** — [github.com/gayathri1908](https://github.com/gayathri1908)
