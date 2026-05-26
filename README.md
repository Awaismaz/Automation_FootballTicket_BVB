# Borussia Dortmund Ticket Automation

A Selenium-based purchase-assistant for Borussia Dortmund (BVB) home-match tickets. Logs in, watches a configured match, and walks the checkout flow the moment seats become available — built because BVB matchday tickets sell out in seconds.

## How it works

`Dortmund.py` drives a headed Chrome session via Selenium:

1. Authenticates against the BVB ticket portal
2. Polls the seat-selection page for the target match
3. Picks available seats matching your preferences
4. Walks through the basket / checkout up to (but not through) the final purchase confirmation — leaving the human in the loop for payment

## Quick start

```bash
pip install -r requirements.txt
python Dortmund.py
```

> ⚠️ Selenium needs a ChromeDriver matching your installed Chrome version. The bundled `chromedriver.exe` may be outdated.

Edit `Dortmund.py` to set:

- Your account credentials (use environment variables — don't hard-code)
- The target match
- Seat preferences (block, category, quantity)

## Notes

- Intended for personal use only. Respect the ticket portal's terms of service.
- Does not bypass any CAPTCHA / anti-bot protection — it just shortens the manual click-through.

## Files

```
Automation_FootballTicket_BVB/
├── Dortmund.py        # Main automation script
├── chromedriver.exe   # Selenium driver (replace with your version)
└── requirements.txt
```
