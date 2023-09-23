from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import argparse
import time

def check_plate(plate):
    url = "https://www.vicroads.vic.gov.au/registration/buy-sell-or-transfer-a-vehicle/check-vehicle-registration/vehicle-registration-enquiry"

    # Setup Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode

    # Start the WebDriver
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    # Wait for the page to load
    time.sleep(5)

    # Find the input field and enter the plate number
    input_field = driver.find_element_by_name("ph_pagebody_0$phthreecolumnmaincontent_1$panel$VehicleSearch$RegistrationNumberCar$RegistrationNumber_CtrlHolderDivShown")
    input_field.send_keys(plate)
    input_field.send_keys(Keys.RETURN)

    # Wait for the results to load
    time.sleep(5)

    # Extract and print the results
    results = driver.find_element_by_id("result")
    print(results.text)

    # Close the WebDriver
    driver.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Check plate number.')
    parser.add_argument('-plate', type=str, help='Plate number in the format XXXXXX')
    args = parser.parse_args()
    check_plate(args.plate)
