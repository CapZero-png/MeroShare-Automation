# MeroShare IPO Automation Bot

This project contains automation scripts to:
* Apply for IPOs (`ipo_apply.py`)
* Check IPO results (`ipo_check_status.py`)

## Important Notice
* All setup steps below are one-time only. (Except for updating "Target_Script")
* This project was developed with the help of AI, so some parts may not be perfect and could require adjustments.
* Keep your account credentials secure at all times.


# One-Time Setup Guide
Follow these steps before running the scripts.

## 1. Install Python
Download Python from:
https://www.python.org/downloads/
Install Python 3.10 or newer.

During installation:
* Make sure to check "Add Python to PATH"

### Verify Installation
Open terminal or command prompt and run:
python --version
You should see the installed Python version.

## 2. Install Required Libraries
Run the following command:
pip install requests playwright

## 3. Install Playwright Browsers
Run:
playwright install


## 4. Install Chromium

Run:

playwright install chromium

This installs the browser used by the scripts.

# Account Setup

Locate the file:

accounts.json

Update it with your account details:

```json
[
  {
    "name": "Your Name",
    "username": "mero_share_username",
    "password": "mero_share_password",
    "bank_id": "bank_id_here",
    "dp_id": "dp_id_here",
    "crn": "crn_number",
    "account_number": "bank_account_number",
    "applied_kitta": 10,
    "transaction_pin": "transaction_pin"
  }
]
```

---

## How to Get Bank ID

1. Open the MeroShare website
2. Before logging in:

   * Right click and select Inspect
   * Go to the Network tab
3. Log in
4. Navigate to "My ASBA"
5. In the Network tab:

   * Click on `bank/`
6. Copy the Bank ID (not the bank code)


# Script Configuration

## IPO Application

Open:

ipo_apply.py

Find:

TARGET_SCRIPT = "IPO_NAME"


Replace with the IPO name.


## IPO Result Check

Open:

ipo_check_status.py

Find:

TARGET_SCRIPT = "IPO_NAME"


Replace with the IPO name.

---

# Running the Scripts

## Apply for IPO

python ipo_apply.py


## Check IPO Result

 ipo_check_status.py



# Notes

* Ensure all details in `accounts.json` are correct
* Ensure sufficient balance in your bank account
* Transaction PIN is required for submission
* Do not share your `accounts.json` file

---
# Troubleshooting

## Python not recognized

python3 --version


## pip issues

python -m pip install --upgrade pip

## Playwright issues


playwright install


## Script errors

* Verify credentials
* Verify bank_id
* The MeroShare interface may have changed


# Disclaimer

This project is for educational purposes only. Use at your own risk.


# Contribution

You are free to modify or improve the scripts.
