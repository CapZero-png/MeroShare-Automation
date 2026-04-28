import json
import time
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

FRONTEND_URL = "https://meroshare.cdsc.com.np"
TARGET_SCRIPT = "Suryakunda Hydro Electric Ltd."  # Change as needed


# Load accounts
with open("accounts.json", "r") as f:
    accounts = json.load(f)


def check_ipo_status(account):
    print(f"\nChecking IPO status for {account['name']}")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # headless=True if you don't want UI
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

            # Login
            page.fill("#username", account["username"])
            page.fill("#password", account["password"])
            page.click('button[type="submit"]')

            # Wait for ASBA
            page.wait_for_selector("a[href*='asba']", timeout=1000)
            page.goto(FRONTEND_URL + "/#/asba")

        except PlaywrightTimeoutError:
            print("❌ Login failed or ASBA page not found")
            browser.close()
            return

        try:
            # Go to Application Report
            page.click("span:has-text('Application Report')")
            page.wait_for_timeout(3000)

            # Find IPO row
            ipo_rows = page.query_selector_all(".row.align-items-center")

            target_row = None
            for row in ipo_rows:
                company_name_el = row.query_selector(".company-name span[tooltip='Company Name']")
                if not company_name_el:
                    continue
                company_name = company_name_el.inner_text().strip().upper()
                if company_name == TARGET_SCRIPT.upper():
                    target_row = row
                    break

            if not target_row:
                print(f"❌ {TARGET_SCRIPT} not found in Application Report")
                browser.close()
                return

            # Click Report button
            report_btn = target_row.query_selector(".btn-issue")
            if report_btn:
                report_btn.click()
                page.wait_for_timeout(3000)

                # Read status (Alloted / Not Alloted)
                try:
                    status_row = page.locator("div.row:has(label[for='boid'])")
                    labels = status_row.locator("div.input-group label")
                    status_text = labels.nth(-2).inner_text().strip()
                    if status_text == "10":
                        print(f"✅ Alloted 10 units\n")
                    elif status_text == "Not Alloted":
                        print(f"❌ Sorry! Not Alloted\n")
                    else:
                        print(f"Unknown status: {status_text}")
                except PlaywrightTimeoutError:
                    print("⚠️ Status element not found")

            else:
                print("❌ Report button not found for IPO")

        except Exception as e:
            print(f"🔥 Error while checking status: {e}")

        finally:
            browser.close()


# Run for all accounts
for account in accounts:
    check_ipo_status(account)
    time.sleep(2)
