#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  2 14:17:27 2018

@author: tnightengale
"""

import os
import sys
import time
import datetime
import random
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class kijiji():
    
    def __init__(self):
        self.current_dir = os.getcwd()
        self.create_title_list()
        self.description = open('description.txt','r').read()
        print('Titles list is {}'.format(self.titles))
        self.current_ad_title = open('titles.txt','r').read()
        self.current_ad_price = open('price.txt','r').read()
        with open('category.txt', 'r') as file:
        # Read the first line from the file
            first_line = file.readline().strip()  # strip() removes leading/trailing whitespaces

            # Split the line by commas and store categories in a list
            self.categories = first_line.split(',')
        self.condition = open('condition.txt','r').read()
        self.phonebrand = open('phonebrand.txt','r').read()
        self.phonebrand_carrier = open('phonebrand_carrier.txt','r').read()
        # run headless browser
        self.headless = FirefoxOptions()
        self.headless.headless = True
    
    @staticmethod
    def is_page_fully_loaded(driver):
        return driver.execute_script("return document.readyState") == "complete"
        
    def create_price_schedule(self):
        '''
        Asks for a lower an upper bound and 
        generates a price schedule to cycle through.
        '''
        upper = int(input('Enter your upper price bound: '))
        lower = int(input('Enter your lower price bound: '))
        self.price_schedule = list(range(lower,upper,10))
    
    def schedule_choice(self):
        '''
        Returns decending values from the price_schedule
        attribute until the lower bound is hit and then
        only return the lower bound.
        '''
        if len(self.price_schedule) == 1:
            current_price = self.price_schedule[0]
        else:
            current_price = self.price_schedule.pop()
        
        return current_price
        
    def create_title_list(self):
        '''
        Reads the titles.txt file in the
        folder the script is run in and 
        creates a list of titles and
        assigns it to self.titles.
        '''
        file = open('titles.txt','r')
        self.titles = []
        while True:
            line = file.readline().strip()
            if line == '':
                break
            else:
                self.titles.append(line)
        file.close()
    
    def random_title(self):
        '''
        Returns a random title from the created
        list of titles.
        '''
        return self.titles[random.randint(0,len(self.titles)-1)]
        
        
    def next_url(self,new_url):
        '''
        Waits till new page is loaded.
        '''
        current = self.kjj.current_url
        self.kjj.get(new_url)
        wait = time.time() + 10 # add 10 second time out
        while current == self.kjj.current_url and time.time() < wait:
            time.sleep(1)
            
    def next_click(self,e_to_click):
        '''
        Waits till next click is loaded.
        '''
        current = self.kjj.current_url
        e_to_click.click()
        wait = time.time() + 10 # add 10 second time out
        while current == self.kjj.current_url and time.time() < wait:
            time.sleep(1)
            
            
    def access_kijiji(self):
        '''
        Create driver and go to Kijiji.
        '''

        # create headless driver
        self.kjj = webdriver.Firefox(options=self.headless)
        # go to kijiji
        self.next_url('https://www.kijiji.ca/')
        time.sleep(5)
        wait = WebDriverWait(self.kjj, 20)
        sign_in_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Sign In")))
        
        sign_in_link.click()
        time.sleep(2)
        self.login()

    
    
    def post_ad(self):
        '''
        Post an ad once logged in.
        '''
        time.sleep(5)
        wait = WebDriverWait(self.kjj, 60)
        post_ad_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Post ad")))
        post_ad_link.click()
        
        # randomly choose ad title and send keys
        WebDriverWait(self.kjj, 60).until(EC.presence_of_element_located((By.ID, "AdTitleForm")))
        title = self.kjj.find_element(By.ID,'AdTitleForm')
        self.current_ad_title = self.random_title()
        title.send_keys(self.current_ad_title)
        
        wait = WebDriverWait(self.kjj, 60)
        next_button_link = wait.until(EC.element_to_be_clickable((By.TAG_NAME, "button")))
        next_button_link.click()
        
        # # click suggested categoryZ
        # categories_link = WebDriverWait(self.kjj, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[contains(@class, "suggestedCategory")]')))
        # categories_link.click()
        
        # categories_link = WebDriverWait(self.kjj, 60).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(.,"Buy & Sell")]')))
        # categories_link.click()
        
        # click suggested categoryZ
        
        elements = self.kjj.find_elements(By.XPATH, '//*[contains(@class, "suggestedCategory")]')
        print(elements)
        if elements:
            elements[0].click()
            print('Suggested Category Clicked')
        else:
            for category in self.categories:
                try:
                    xpath_expression = f'//button[contains(., "{category.strip()}")]'
                    categories_link = WebDriverWait(self.kjj, 20).until(EC.element_to_be_clickable((By.XPATH, xpath_expression)))
                    categories_link.click()
                    print(category)
                except TimeoutException:
                    print(f"Timed out while waiting for {category}, continuing with the next category...")
                    continue
        
        print('Category selected')
        time.sleep(5)
        label_element = WebDriverWait(self.kjj, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'label[for="forsaleby_s-delr"]'))
        )
        label_element.click()
        
        label_element = WebDriverWait(self.kjj, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'label[for="fulfillment_s-delivery"]'))
        )
        label_element.click()
        
        label_element = WebDriverWait(self.kjj, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'label[for="fulfillment_s-shipping"]'))
        )
        label_element.click()
        
        label_element = WebDriverWait(self.kjj, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'label[for="fulfillment_s-curbside"]'))
        )
        label_element.click()
        
        label_element = WebDriverWait(self.kjj, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'label[for="payment_s-cashless"]'))
        )
        label_element.click()
        
        label_element = WebDriverWait(self.kjj, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'label[for="payment_s-cashaccepted"]'))
        )
        label_element.click()
        
        # Locate the dropdown element
        condition_dropdown = self.kjj.find_element(By.ID, 'condition_s')

        # Create a Select object
        select = Select(condition_dropdown)

        # Select the option by its value
        select.select_by_value(self.condition)
        
        
        # Locate the dropdown element
        phonebrand_dropdown = self.kjj.find_element(By.ID, 'phonebrand_s')

        # Create a Select object
        select = Select(phonebrand_dropdown)

        # Select the option by its value
        select.select_by_value(self.phonebrand)
                        
                # Locate the dropdown element
        phone_Carrier_dropdown = self.kjj.find_element(By.ID, 'phonecarrier_s')

        # Create a Select object
        select = Select(phone_Carrier_dropdown)

        # Select the option by its value
        select.select_by_value(self.phonebrand_carrier)
        
        # self.kjj.find_element(By.CSS_SELECTOR, 'label[for="fulfillment_s-delivery"]').click()
                
        # choose and enter ad price
        WebDriverWait(self.kjj, 60).until(EC.presence_of_element_located((By.ID, "PriceAmount")))
        price = self.kjj.find_element(By.ID,'PriceAmount')
        price.send_keys(self.current_ad_price)
        
        # enter description
        desc = self.kjj.find_element(By.TAG_NAME,'textarea')
        desc.send_keys(self.description)
        
        # Change directory to where the images are located
        os.chdir('C:/Users/HILL PATEL/Downloads/kijiji_autoposter-master (1)/kijiji_autoposter-master/')

        # List all image files in the 'images' directory
        image_list = os.listdir('images')

        # Locate the file input field
        upload = self.kjj.find_element(By.CLASS_NAME, 'imageUploadButtonWrapper')
        upload = upload.find_element(By.TAG_NAME, 'input')

        # Iterate over each image file and upload it
        for pic in image_list:
            # Construct the absolute path to the image file
            absolute_path = os.path.abspath(os.path.join('images', pic))
            print("Absolute path:", absolute_path)
            
            # Upload the image file
            upload.send_keys(absolute_path)
        
        # wait for pics to load
        time.sleep(20)
        
        # click submit
        post_ad_link = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Post Your Ad"]')))
        post_ad_link.click()
        time.sleep(20)        
        
        print(
                'Ad posted successfully.',
                '\nCurrent title is {}.'.format(self.current_ad_title),
                '\nCurrent price is {}.'.format(self.current_ad_price)
                )
            
    
    def delete_ad(self):
        wait = WebDriverWait(self.kjj, 60)
        # go to ad page
        self.next_url('https://www.kijiji.ca/m-my-ads/active/1')
        time.sleep(5)
        tbody_element = self.kjj.find_element(By.TAG_NAME,'tbody')
        div_elements = tbody_element.find_elements(By.XPATH,'.//div[not(@class)]')
        for div_element in div_elements:
            # Flag variable to track if the inner loop breaks
            inner_loop_broken = False
            
            # Find all links within the current div_element
            links = div_element.find_elements(By.XPATH, './/a[@href]')
            for link in links:
                # Check if the link contains the current_ad_title
                if self.current_ad_title in link.get_attribute("innerHTML"):
                    # Find the delete button associated with this div_element and click it
                    delete_button = div_element.find_element(By.XPATH, './/span[text()="Delete"]/ancestor::button')
                    delete_button.click()
                    
                    # Set the flag to True to indicate that the inner loop has broken
                    inner_loop_broken = True
                    break  # Exit the inner loop after clicking the delete button
                    
            # Check if the inner loop was broken
            if inner_loop_broken:
                break  # Exit the outer loop if the inner loop was broken

                # Wait for the overlay to be present
        button = WebDriverWait(self.kjj, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Prefer not to say"]')))

        # Click the button
        button.click()
        button = WebDriverWait(self.kjj, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Delete My Ad"]')))

        # Click the button
        button.click()
        
                        
        # go into ad
        # self.click_by_text(self.kjj.find_element(By.TAG_NAME,'a'),'a',self.current_ad_title)
        
        # # check for replies
        # reply_element = self.kjj.find_element_by_class_name('ad-replies')
        # replies = int(reply_element.text)
        # print('\nCurrent number of replies is {}.'.format(replies))
        # if replies > 0:
        #     print('\nYou have {} replies in your inbox. Ad not deleted.'.format(replies))
        #     print('\nPress "ctrl + c" to quit the program.')
        #     input('\nPress "Enter" to continue the loop and delete the ad: ')
        
        # click delete ad
        # self.click_by_text(self.kjj.find_element(By.TAG_NAME,'a'),'a','Delete Ad')
        
        # # click "not selling anymore"
        # self.click_by_text(self.kjj.find_element(By.TAG_NAME,'li'),'li','Not selling it anymore')
        
        print('Ad deleted.')


        
    def login(self):
        time.sleep(5)
        
        WebDriverWait(self.kjj, 60).until(EC.presence_of_element_located((By.ID, "username")))
        user = self.kjj.find_element(By.ID,'username')
        user.send_keys("hillpatel1357@gmail.com")
        
        WebDriverWait(self.kjj, 60).until(EC.presence_of_element_located((By.ID, "password")))
        password = self.kjj.find_element(By.ID,'password')
        password.send_keys("pbR.fSb^G^Sku5g")
                           
        WebDriverWait(self.kjj, 60).until(EC.presence_of_element_located((By.ID, "login-submit")))
        self.next_click(self.kjj.find_element(By.ID, "login-submit"))
    
    def click_by_text(self, function, search, text):
        '''
        Take in a driver, find elements by
        tag, return element with matching text.
        '''
        elements = function(search)
        text_list = [i.text for i in elements]
        self.next_click(elements[text_list.index(text)])
    
    def close(self):
        self.kjj.close()
        print('Browser closed')

def d_str(date_time_object):
    '''
    Takes in a datetime object and outputs "yyyy/mm/dd hh:mm.ss".
    '''
    dt = date_time_object
    return dt.strftime('%Y/%m/%d %H:%M:%S')

def main(wait_hours):
    browser = kijiji()
    
    while True:
        
        # post ad
        time_stamp = d_str(datetime.datetime.now())
        print('Loop start. The current time is {}.'.format(time_stamp))
        
        browser.access_kijiji()
        
        browser.post_ad()
        
        # browser.close()
        
        # pause if current hour is between 24 and 6
        #print('Checking if time is between 12am and 6am.')
        #dt = datetime.datetime.now()
        #seven_am = datetime.datetime(dt.year,dt.month,dt.day,7,0)
        #night_time = dt.hour in [24,1,2,3,4,5,6]
            
        # wait 4hrs or hours arg
        wait_time = datetime.timedelta(minutes=0)
        sleep_time = datetime.datetime.now() + wait_time
        
        # wait till 
        sleep_time_stamp = d_str(sleep_time) #d_str(max(seven_am,sleep_time))
        print('Sleeping loop till {}.'.format(sleep_time_stamp))
        while datetime.datetime.now() < sleep_time: #or night_time:
            time.sleep(1)
        
        # delete ad
        print('Deleting ad...')
        # browser.access_kijiji()
        
        browser.delete_ad()
        
        # browser.close()
        
        # sleep 60 seconds
        print('sleeping 60 seconds before reposting...')
        time.sleep(60)
        
        
    
if __name__ == '__main__':
    try:
        hours_option = int(sys.argv[1])
    except:
        hours_option = 4
    main(hours_option)
