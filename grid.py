from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time

# Define the URL of the Selenium Grid Hub
hub_url = "http://192.168.1.19:4444/wd/hub"

# Define desired capabilities for the browser (e.g., Chrome)
chrome_options = webdriver.ChromeOptions()


# Create a remote WebDriver instance
driver = webdriver.Remote(command_executor=hub_url, options=chrome_options)

# Now you can use the 'driver' object to automate the browser
driver.get("https://www.youtube.com/")
time.sleep(4)
print(driver.title)

# Close the browser when done
driver.quit()
