import string
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
        play_game()

def play_game():
    diagram_one()
    print(words)
    diagram_two()
    diagram_three()
    diagram_four()

def diagram_one():
    driver.find_element_by_xpath("/html/body/section/div/ui-view/div/div[4]/div/div[1]/div[6]/div/a/div[2]").click()
    driver.find_element_by_xpath("/html/body/section/div/ui-view/div[1]/div[1]/button").click()
    driver.find_element_by_xpath("/html/body/section/div/ui-view/div[2]/div/div/div/div/div/button/span").click()
    word_location = driver.find_element_by_xpath("/html/body/section/div/ui-view/div[3]/div/div[4]/div[1]").find_elements_by_xpath("./div/div[2]")
    global words
    words = []
    for item in word_location:
        words.append(item.text)
    time.sleep(2)
    driver.find_element_by_xpath("/html/body/section/div/ui-view/aside/div[2]/a").click()

def diagram_two():
    driver.find_element_by_xpath("/html/body/section/div/ui-view/div/div[4]/div/div[1]/div[11]/div/a/div[2]").click()
    driver.find_element_by_xpath("/html/body/section/div/ui-view/div[1]/div[1]/button").click()
    driver.find_element_by_xpath("/html/body/section/div/ui-view/div[2]/div/div/div/div/div/button/span").click()
    word_opts = driver.find_element_by_xpath("/html/body/section/div/ui-view/div[3]/div/div[3]/div[2]/div/div").find_elements_by_xpath("./div/div/div/div[1]")
    #/html/body/section/div/ui-view/div[3]/div/div[3]/div[2]/div/div
    #/html/body/section/div/ui-view/div[3]/div/div[3]/div[2]/div/div/

    blanks = driver.find_element_by_xpath("/html/body/section/div/ui-view/div[3]/div/div[3]/div[1]/div/div/div").find_elements_by_xpath("./div/div/div")
    for item in word_opts:
        text = item.text
        i = 0
        while words[i] != text:
            i+=1
        item.click()
        blanks[i].click()
        time.sleep(5)
    driver.find_element_by_xpath("/html/body/section/div/ui-view/div[3]/div/div[1]/h3/div").click()
    time.sleep(2)
    driver.find_element_by_xpath("/html/body/div/div/div/div/div/div/h3/a[2]").click()


def diagram_three():
    driver.find_element_by_xpath("/html/body/section/div/ui-view/div/div[4]/div/div[1]/div[15]/div/a/div[2]").click()
    driver.find_element_by_xpath("/html/body/section/div/ui-view/div[1]/div[1]/button").click()
    driver.find_element_by_xpath("/html/body/section/div/ui-view/div[2]/div/div/div/div/div/button/span").click()
    blanks = driver.find_element_by_xpath("/html/body/section/div/ui-view/div[3]/div/form/div").find_elements_by_xpath("./div/input")
    i = 0
    for item in blanks:
        item.send_keys(words[i])
        i+=1
        time.sleep(3)
    driver.find_element_by_xpath("/html/body/section/div/ui-view/div[3]/div/div[1]/h3/div/button").click()
    driver.find_element_by_xpath("/html/body/div/div/div/div/div/div/h3/a[2]").click()

def diagram_four():
    driver.find_element_by_xpath("/html/body/section/div/ui-view/div/div[4]/div/div[1]/div[16]/div/a/div[2]").click()
    driver.find_element_by_xpath("/html/body/section/div/ui-view/div[1]/div[1]/button").click()
    driver.find_element_by_xpath("/html/body/section/div/ui-view/div[2]/div/div/div/div/div/button/span").click()
    driver.find_element_by_xpath("/html/body/section/div/ui-view/div[3]/div/div[5]/div[3]/h3[1]/button/span").click()
    input = driver.find_element_by_xpath("/html/body/section/div/ui-view/div[3]/div/div[5]/div[4]/textarea")
    for i in range(300):
        input.send_keys(random.choice(string.ascii_letters))
    time.sleep(5)
    driver.find_element_by_xpath("/html/body/section/div/ui-view/div[3]/div/div[5]/button[2]").click()
    driver.find_element_by_xpath("/html/body/div/div/div/div/div/div/h3/div/a").click()


main()