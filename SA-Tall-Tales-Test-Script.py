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
        driver.find_element_by_xpath("/html/body/section/div/ui-view/div/div[4]/div/div[1]/div[8]/div/a").click()
        play_game()

def play_game():
    try:
        element = EC.presence_of_element_located(
            (By.XPATH, "/html/body/section/div/ui-view/div[1]/div/div/div/div/div/div[1]/button"))
        WebDriverWait(driver, 3).until(element)
    finally:
        driver.find_element_by_xpath("/html/body/section/div/ui-view/div[1]/div/div/div/div/div/div[1]/button").click()
        try:
            element = EC.presence_of_element_located(
                (By.XPATH, "/html/body/section/div/ui-view/div[1]/div/div/div/div/div/button/span"))
            WebDriverWait(driver, 3).until(element)
        finally:
            driver.find_element_by_xpath("/html/body/section/div/ui-view/div[1]/div/div/div/div/div/button/span").click()
            random_game_driver()

def random_game_driver():

    not_pair = defaultdict()
    time.sleep(3)
    close_popup = "/html/body/div[1]/div/div/div/div[1]/div/div[2]/button"
    round_marker_list = driver.find_element_by_xpath(
        "//*[@id=\"page-content-wrapper\"]/div/div/div[3]/p[1]").find_elements_by_xpath("./span/span/span[2]")
    print(len(round_marker_list))
    time.sleep(3)
    round_marker_list[0].click()
    print(driver.window_handles)
    time.sleep(2)
    word_bank_button_list = driver.find_element_by_xpath("/html/body/div[1]/div/div/div/div[2]/div").find_elements_by_xpath("./div/span[2]")
    word_bank = []
    for item in word_bank_button_list:
        word_bank.append(item.text)
        not_pair[item.text] = defaultdict()
    total_size = len(word_bank)
    print(total_size)
    driver.find_element_by_xpath(close_popup).click()
    blank_spots = [None]*total_size
    finished = False
    spots = set()
    complete = set()
    while not finished:
        j = 0
        random.shuffle(word_bank)
        #Random num part
        for i in range(total_size):
            if i in complete:
                blank_spots[i] = None
                print("Blank Spots" + str(blank_spots))
            else:
                position = get_rand_num(total_size)
                while position in spots:
                    position = get_rand_num(total_size)
                blank_spots[i] \
                    = word_bank[j]
                spots.add(position)
                print("Blank Spots" + str(blank_spots))
                j+=1
        counter = 0
        #Actual Guessing Game part
        for blank_spot in range(len(round_marker_list)):
            if blank_spots[counter] is not None:
                round_marker_list[blank_spot].click()
                item = None
                print(item)
                j = 0
                print(str(blank_spots[blank_spot]) + ": This is the word")
                time.sleep(10)
                while item != str(blank_spots[blank_spot]):
                    j += 1
                    item = driver.find_element_by_xpath("/html/body/div[1]/div/div/div/div[2]/div/div[" + str(j) + "]/span[2]").text
                    print(item)
                time.sleep(3)
                driver.find_element_by_xpath("/html/body/div[1]/div/div/div/div[2]/div/div[" + str(j) + "]/span[2]").click()
                time.sleep(3)
            counter +=1
        time.sleep(5)
        driver.find_element_by_xpath("/html/body/section/div/ui-view/div[1]/div/div/div/div[2]/div[2]/button[2]").click()
        incorrect = set()
        time.sleep(10)
        round_marker_list = driver.find_element_by_xpath(
            "//*[@id=\"page-content-wrapper\"]/div/div/div[3]/p[1]").find_elements_by_xpath("./span/span/span/span[1]")
        k = 0

        temp = []
        for square in round_marker_list:
            print(square.get_attribute("class"))
            if square.get_attribute("class") == "square square-choice-incorrect":
                incorrect.add(square)
                temp.append(blank_spots[k])
                blank_spots[k] = 0
                print(temp)
            else:
                complete.add(k)
                blank_spots[k]=None
                temp.append(None)
                print(temp)
            k += 1
        word_bank = temp
        if incorrect.__sizeof__() == 0:
            finished = True
        spots.clear()
        k=0

#/html/body/section/div/ui-view/div[1]/div/div/div/div[3]/p[1]/span[2]/span/span/span[1]
#//*[@id="page-content-wrapper"]/div/div/div[3]/p[1]/span[2]/span/span/span[1]
#//*[@id="page-content-wrapper"]/div/div/div[3]/p[1]/span[2]/span/span/span[2]



    #/html/body/div[1]/div/div/div/div[2]/div/div[1]/span[2]

    #/html/body/div[1]/div/div/div/div[2]/div/div[1]/span[2]

def get_rand_num(size):
    return randint(0, size - 1)
#    text = word_tokenize("Hello everyone, my  is Ezra. I hope you are all doing well!")
# output = nltk.pos_tag(text)
# print(output)



main()