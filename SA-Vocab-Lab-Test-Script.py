from collections import defaultdict
from random import random, randint, shuffle
import time
import random
import nltk
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import *
from nltk import *

driver = webdriver.Chrome('C:\\Users\\ezrag\\Documents\\Winter2020-21 Internship\\chromedriver.exe')


def main():
    get_info()
    driver.get("https://teach.speakagent.com/#/")
    login()


def get_info():
    with open("TallTalesKey.txt") as file:
        global USERNAME
        USERNAME = file.readline()
        global P1
        P1 = file.readline()
        global P2
        P2 = file.readline()
        global MODE
        MODE = file.readline()


# Logs in to the game, bringing to main dashboard
def login():
    driver.implicitly_wait(20)
    driver.find_element_by_xpath("/html/body/section/div/ui-view/div[2]/div/div/div[1]/div/button").click()
    driver.find_element_by_xpath("/html/body/div[1]/div/div/div/div[2]/div/div[1]/div/form/div[1]/input").send_keys(
        USERNAME)
    time.sleep(.5)
    driver.find_element_by_xpath(P1).click()
    driver.find_element_by_xpath(P2).click()
    time.sleep(2)
    driver.find_element_by_xpath("/html/body/div[1]/div/div/div/div[2]/div/div[1]/div/form/div[4]/button").click()
    time.sleep(5)
    go_to_picture_from_home()


# Goes from main menu to game Picture Perfect
def go_to_picture_from_home():
    try:
        element = EC.presence_of_element_located(
            (By.XPATH, "/html/body/section/div/ui-view/div/div/div[1]/div/div[2]/div[4]/a"))
        WebDriverWait(driver, 3).until(element)
    finally:
        driver.find_element_by_xpath("/html/body/section/div/ui-view/div/div/div[1]/div/div[2]/div[4]/a").click()
        driver.find_element_by_xpath("/html/body/section/div/ui-view/div/div[4]/div/div[1]/div[9]/div").click()
        play_game()


def play_game():
    driver.find_element_by_xpath("/html/body/section/div/ui-view/div[3]/div/div/div/div[1]/button").click()
    time.sleep(2)
    driver.find_element_by_xpath("/html/body/section/div/ui-view/div[4]/div/div/div/div/button").click()
    game_driver()

def game_driver():
    word_options = driver.find_element_by_xpath("/html/body/section/div/ui-view/div[5]/div/div[1]/div[1]").find_elements_by_xpath("./h4/span")
    actual_words = []
    for item in word_options:
        actual_words.append(item.text)
    print(actual_words)
    count = 0
    #Cycle through each option in word_options
    for round in word_options:
        round.click()
        driver.find_element_by_xpath("/html/body/section/div/ui-view/div[6]/div/div/div[4]/div/button").click()
        round_opt = driver.find_element_by_xpath("/html/body/section/div/ui-view/div[7]/div/div[1]/div[2]/div/div").find_elements_by_xpath("./div/span")
        done = False
        not_select = set()
        fail_count = 0
        while not done:
            time.sleep(2)
            nums = set()
            blank_spots = driver.find_element_by_xpath("/html/body/section/div/ui-view/div[7]/div/div[1]/div[3]/div[2]").find_elements_by_xpath("./div")
            print(len(blank_spots))
            for i in range (len(blank_spots)):
                time.sleep(2)
                select = get_rand(len(round_opt))
                while select in nums or select in not_select:
                    select = get_rand(len(round_opt))
                nums.add(select)
                round_opt[select].click()
            driver.find_element_by_xpath("/html/body/section/div/ui-view/div[7]/div/div[1]/div[3]/div[4]/p/a").click()
            time.sleep(3)
            if driver.find_element_by_xpath("/html/body/section/div/ui-view/div[5]").get_attribute("class")!="game-container clearfix with-aside ng-scope":
                for num in nums:
                    print(num)
                    if round_opt[num].get_attribute("class") == "margin-left-sm color-dark-green-2 bold ng-binding color-grey line-through-cursor-none":
                        not_select.add(num)
            else:
                done = True
            nums.clear()
            fail_count += 1
            if fail_count > 3:
                time.sleep(2)
                driver.find_element_by_xpath("/html/body/section/div/ui-view/div[6]/div/div/div[4]/div/button").click()
        time.sleep(2)
        count += 1

#margin-left-sm color-dark-green-2 bold ng-binding color-grey line-through-cursor-none

def get_rand(num):
    return randint(0,num-1)
main()