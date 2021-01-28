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
        driver.find_element_by_xpath("/html/body/section/div/ui-view/div/div[4]/div/div[1]/div[12]/div/a/div[1]").click()
        play_game()

def play_game():
    driver.find_element_by_xpath("/html/body/section/div/ui-view/div[1]/div/div/div[1]/div/button").click()
    #Sometimes it doesnt read the sentence. Just reload the script.
    sentence = driver.find_element_by_xpath("/html/body/section/div/ui-view/div[2]/div/div/div[2]/div[2]/p").text
    while sentence == "":
        sentence = driver.find_element_by_xpath("/html/body/section/div/ui-view/div[2]/div/div/div[2]/div[2]/p").text
    time.sleep(5)
    driver.find_element_by_xpath("/html/body/section/div/ui-view/div[2]/div/div/div[4]/div/button").click()
    # We are gong to start with option 1:
    driver.find_element_by_xpath("/html/body/section/div/ui-view/div[6]/div/div[1]/div[1]/div/h1").click()
    driver.find_element_by_xpath("/html/body/section/div/ui-view/div[6]/div/div[2]/div/button").click()
    easy_game_driver(sentence)



def easy_game_driver(sentence):
    if sentence == "":
        driver.quit()
        quit()
    #word bank:     /html/body/section/div/ui-view/div[7]/div/div[1]/div/div
    # specific box: /html/body/section/div/ui-view/div[7]/div/div[1]/div/div/div[4]/div/div/div[1]
    word_order = sentence.split()
    section_num = sentence.split(".")
    total_rounds = len(section_num)-1
    print(section_num)
    print(word_order)
    spot = 0
    for i in range(total_rounds):
        words = driver.find_element_by_xpath("/html/body/section/div/ui-view/div[7]/div/div[1]/div/div").find_elements_by_xpath("div/div/div/div[1]")
        word_choices = []
        for item in words:
            if item.text != "":
                word_choices.append(item)
                print(item.text)
        print(word_choices)
        slots = driver.find_element_by_xpath("/html/body/section/div/ui-view/div[7]/div/div[3]/div/div").find_elements_by_xpath("div/div/div/div[1]")
        print(len(slots))
        for item in slots:
            time.sleep(2)
            if item.text == "":
                cont = False
                word_spot = 0
                posit = None
                while(not cont):
                    first = word_choices[word_spot].text
                    sec = word_order[spot]
                    if word_choices[word_spot].text == word_order[spot]:
                        cont = True
                        posit = word_choices[word_spot]
                        word_choices.remove(posit)
                    else:
                        word_spot += 1
                posit.click()
                time.sleep(.25)
                item.click()
            spot +=1
        time.sleep(7)
        if i != total_rounds - 1:
            driver.find_element_by_xpath("/html/body/section/div/ui-view/div[8]/button").click()
            time.sleep(2)
            driver.find_element_by_xpath("/html/body/section/div/ui-view/div[4]/div[3]/button").click()
            time.sleep(5)




main()


