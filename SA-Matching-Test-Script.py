import time
from collections import defaultdict
from random import random, randint
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import *

driver = webdriver.Chrome('C:\\Users\\ezrag\\Documents\\Winter2020-21 Internship\\chromedriver.exe')


def main():
    get_info()
    driver.get("https://teach.speakagent.com/#/")
    login()
    play_game()


def get_info():
    with open("MatchingKey.txt") as file:
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
    time.sleep(.5)
    driver.find_element_by_xpath("/html/body/div[1]/div/div/div/div[2]/div/div[1]/div/form/div[4]/button").click()
    time.sleep(5)
    go_to_picture_from_home()


# Goes from main menu to game Picture Perfect
def go_to_picture_from_home():
    try:
        element = EC.presence_of_element_located(
            (By.XPATH, "/html/body/section/div/ng-include[1]/div/div/nav/ul[2]/li[3]/a"))
        WebDriverWait(driver, 3).until(element)
    finally:
        driver.find_element_by_xpath("/html/body/section/div/ng-include[1]/div/div/nav/ul[2]/li[3]/a").click()
        driver.find_element_by_xpath(
            "/html/body/section/div/ui-view/div/div/div/div/div[2]/div[6]/div/div/a[2]").click()
        driver.find_element_by_xpath("/html/body/section/div/ui-view/div/div[4]/div/div[1]/div[1]/div/a").click()


def play_game():
    try:
        element = EC.presence_of_element_located(
            (By.XPATH, "/html/body/section/div/ui-view/div[1]/div/div/div/div[1]/button"))
        WebDriverWait(driver, 3).until(element)
    finally:
        driver.find_element_by_xpath("/html/body/section/div/ui-view/div[1]/div/div/div/div[1]/button").click()
        try:
            element = EC.presence_of_element_located(
                (By.XPATH, "/html/body/section/div/ui-view/div[2]/div/div/div/div/div/div[2]/button/span"))
            WebDriverWait(driver, 5).until(element)
        finally:
            driver.find_element_by_xpath(
                "/html/body/section/div/ui-view/div[2]/div/div/div/div/div/div[2]/button/span").click()
            game_driver()


def game_driver():
    round_marker_list = driver.find_element_by_xpath(
        "/html/body/section/div/ui-view/div[3]/div").find_elements_by_xpath("./div")
    item_num = len(round_marker_list)
    total_pairs = item_num / 2
    complete = 0
    completed_pairs = set()
    guessed_pairs = []
    for i in range(item_num):
        guessed_pairs.append(set())
    while complete < total_pairs:
        print(guessed_pairs)
        print(completed_pairs)
        randNum1 = get_rand_num(item_num)
        while randNum1 in completed_pairs:
            randNum1 = get_rand_num(item_num)
        round_marker_list[randNum1].click()
        time.sleep(3)
        randNum2 = get_rand_num(item_num)
        while randNum2 == randNum1 or randNum2 in completed_pairs or randNum2 in guessed_pairs[randNum1]:
            randNum2 = get_rand_num(item_num)
        round_marker_list[randNum2].click()
        time.sleep(3)
        if complete != total_pairs - 1:
            if driver.find_element_by_xpath(
                    "/html/body/section/div/ui-view/div[3]/div/div[" + str(randNum1 + 1) + "]/div").get_attribute(
                    "class") == "card-spaceholder ng-scope":
                completed_pairs.add(randNum1)
                completed_pairs.add(randNum2)
                complete += 1
                print(str(complete) + " match(es) found")
            else:
                guessed_pairs[randNum1].add(randNum2)
                guessed_pairs[randNum2].add(randNum1)
            time.sleep(3)
        else:
            complete += 1
    time.sleep(3)
    print("Game Complete!")


def get_rand_num(size):
    return randint(0, size - 1)


main()
