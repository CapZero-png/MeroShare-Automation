import json
import time
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

FRONTEND_URL = "https://meroshare.cdsc.com.np"

TARGET_SCRIPT = "Palpa Cement Industries Limited" #Update as needed

# Load accounts
with open("accounts.json", "r") as f:
    accounts = json.load(f)

def apply_ipo(account):
    print(f"\n Processing {account['name']}")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Set True to run headless
        page = browser.new_page()
        page.goto(FRONTEND_URL)
        page.wait_for_timeout(1000)

        try:
            # Select DP
            page.wait_for_selector(".select2-selection", timeout=1000)
            page.click(".select2-selection")
            page.wait_for_selector(".select2-search__field", timeout=1000)
            page.fill(".select2-search__field", str(account["dp_id"]))
            page.keyboard.press("Enter")
        except PlaywrightTimeoutError:
            browser.close()
            print("❌ Failed to select Depository Participant (DP)")
            return

        try:
            # Login
            page.fill("#username", account["username"])
            page.fill("#password", account["password"])
            page.click('button[type="submit"]')
        except PlaywrightTimeoutError:
            browser.close()
            print("❌ Failed entering username/password")
            return

        # Wait for navigation and ASBA page link
        try:
            page.wait_for_timeout(1000)
            page.wait_for_selector("a[href*='asba']", timeout=1000)
        except PlaywrightTimeoutError:
            browser.close()
            print("❌ Login failed or ASBA page not found")
            return

        # Go to My ASBA
        page.goto(FRONTEND_URL + "/#/asba")
        page.wait_for_timeout(1000)

        # Select the IPO to apply
        try:
            # Wait for IPO rows to load
            page.wait_for_selector(".row.align-items-center", timeout=1000)
            ipo_rows = page.query_selector_all(".row.align-items-center")

            selected_row = None
            for row in ipo_rows:
                company_name = row.query_selector(".company-name span[tooltip='Company Name']").inner_text().strip()
                if company_name.upper() == TARGET_SCRIPT.upper():
                    selected_row = row
                    break

            if not selected_row:
                print(f"❌ IPO not found")
            else:
                # Click Apply button
                apply_btn = selected_row.query_selector(".btn-issue")
                apply_btn.click()

            selected_row.click()
            page.wait_for_timeout(1000)

            # Fill IPO form
            # Wait for bank dropdown and select bank
            page.wait_for_selector("#selectBank", timeout=100000)
            page.select_option("#selectBank", str(account["bank_id"]))


            # Wait for account number dropdown to appear
            page.wait_for_selector("#accountNumber", timeout=5000)

            # Wait for bank dropdown and select bank number
            page.wait_for_selector("#accountNumber", timeout=10000)
            page.select_option("#accountNumber", str(account["account_number"]))
            
            # Fill Applied Kitta
            # Slowly type Applied Kitta
            applied_kitta = str(account["applied_kitta"])
            page.fill("#appliedKitta", "")  
            page.type("#appliedKitta", applied_kitta, delay=200) 

            # Wait a little to let the frontend calculate the amount
            page.wait_for_timeout(1000)

            # Get calculated amount
            amount_value = page.eval_on_selector("#amount", "el => el.value")


            # Fill CRN
            page.fill("#crnNumber", account["crn"])


            # Tick disclaimer
            page.check("#disclaimer")


            # Submit
            page.wait_for_selector("button[type='submit']", state="visible", timeout=000)

            # Optional: check if it's disabled
            is_disabled = page.eval_on_selector("button[type='submit']", "el => el.disabled")
            if is_disabled:
                print("❌ Proceed button is disabled")
            else:
                page.click("button[type='submit']")

        except Exception as e:
            print(f"❌ Unable to click Proceed button for {account['name']}: {e}")

        # After clicking Proceed
        try:
            # Wait for transaction PIN input
            page.wait_for_timeout(3000)
            page.wait_for_selector("#transactionPIN", timeout=1000)
            page.fill("#transactionPIN", str(account["transaction_pin"]))
            page.wait_for_timeout(3000)

        except Exception as e:
            print(f"❌ Error submitting transaction PIN for {account['name']}: {e}")
        
        # After entering transaction PIN
        try:
            buttons = page.query_selector_all("button[type='submit']")
            if len(buttons) >= 2:
                buttons[1].click()  # second button
                print(f"✅ IPO Applied Successfully for {account['name']}")
                page.wait_for_timeout(5000)  # wait a few seconds for confirmation
            else:
                print("❌ Could not find the second submit button")
                    
        except Exception as e:
            print(f"❌ Error clicking final Apply button for {account['name']}: {e}")

        #finally:
            page.wait_for_timeout(1000)
            browser.close()


# Loop through accounts
for account in accounts:
    apply_ipo(account)
    time.sleep(2)
