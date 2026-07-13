# 🎯 BookMyShow Slot Availability Monitor

Automatically monitors a BookMyShow event/movie page for ticket availability and sends an email alert the moment tickets open up — no manual checking needed.

---

## 📌 What It Does

- Checks **BookMyShow** for movie/event ticket availability
- Runs **silently in the background** (headless browser — no window opens)
- Sends an **instant email** the moment tickets become available
- Can monitor **multiple BookMyShow pages simultaneously** using threads

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

Open `slot_availablity.py` and update these lines:
```python
SENDER_EMAIL        = "your_email@gmail.com"
SENDER_APP_PASSWORD = "your_app_password"   # Gmail App Password
RECEIVER_EMAIL      = "your_email@gmail.com"
```

> **How to get Gmail App Password:**
> Go to Google Account → Security → 2-Step Verification → App Passwords → Generate

### 4. Run
```bash
python slot_availablity.py
```

---

## ⚙️ How It Works

```
slot_availablity.py starts
    │
    └── Thread → Opens BookMyShow URL (headless)
                  ↓ every 10 seconds
                  Checks for: "Book Now", "Select Seats", "Buy Tickets"
                  If found → sends email instantly ✅
```

---

## 📁 Project Structure

```
selenium_slot_availability/
│
├── slot_availablity.py   # Main script — run this
└── README.md
```

---

## 🔧 Adding Your Own Sites

In `slot_availablity.py`, add a new entry to the `SITES` list:

```python
SITES = [
    {
        "name"           : "My Event",
        "url"            : "https://in.bookmyshow.com/events/your-event/EVXXXXXXX",
        "check_interval" : 10,   # seconds between checks
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
| `threading` | Monitor multiple pages at once |

---

## ⚠️ Notes

- Requires **Google Chrome** installed on your machine
- Keep the terminal open while monitoring — script runs continuously until availability is found

---

## 👩‍💻 Author

**Gayathri** — [github.com/gayathri1908](https://github.com/gayathri1908)
