import time
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
    print("Test Complete -- Game Finished")
    driver.close()

def get_info():
    with open("PicturePairsKey.txt") as file:
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
        driver.find_element_by_xpath("/html/body/section/div/ui-view/div/div[4]/div/div[1]/div[3]/div/a").click()


def play_game():
    try:
        element = EC.presence_of_element_located(
            (By.XPATH, "/html/body/section/div/ui-view/div[1]/div/div/div/div[1]/button"))
        WebDriverWait(driver, 3).until(element)
    finally:
        driver.find_element_by_xpath("/html/body/section/div/ui-view/div[1]/div/div/div/div[1]/button").click()
        try:
            element = EC.presence_of_element_located(
                (By.XPATH, "/html/body/section/div/ui-view/div[2]/div/div/div/button"))
            WebDriverWait(driver, 3).until(element)
        finally:
            driver.find_element_by_xpath("/html/body/section/div/ui-view/div[2]/div/div/div/button").click()
            if MODE == "RANDOM":
                random_game_driver()
            elif MODE == "MIN":
                min_score_game_driver()
            elif MODE == "MAX":
                max_score_game_driver()
            else:
                random_game_driver()



def random_game_driver():
    # we need to get the num of rounds:
    round_marker_list = driver.find_element_by_xpath(
        "/html/body/section/div/ui-view/aside/div[2]/ul").find_elements_by_css_selector("li")
    round_count = len(round_marker_list)
    assert round_count == 10
    round_complete = 0
    # main driver of game
    while round_complete < round_count:
        time.sleep(7.5)
        # at onset of round, we need to get all the elements of the game:
        round_option_list = []
        for i in range(1, 4):
            round_option_list.append(driver.find_element_by_xpath("//*[@id=\"app-container\"]/div[" + str(i) + "]"))
        assert len(round_option_list) == 3
        values_guessed = set()
        correct = False
        while not correct:
            guess = get_rand_num()
            if guess not in values_guessed:
                option = round_option_list[guess]
                values_guessed.add(guess)
                option.click()
                attribute = option.get_attribute("class")
                print(attribute)
                if attribute == "option-container ng-scope true" or attribute == "option-container ng-scope ng-animate true-add":
                    round_option_list.clear()
                    values_guessed.clear()
                    attribute = ""
                    round_complete += 1
                    correct = True
                    print(str(round_complete) + " rounds complete out of " + str(round_count))
                else:
                    time.sleep(3)

# this driver attempts to play the game to get a score of sixty or above. The way that this happens is that
# the first six questions are guaranteed to succeed, and the final four are random, like above.
def min_score_game_driver():
    # we need to get the num of rounds:
    round_marker_list = driver.find_element_by_xpath(
        "/html/body/section/div/ui-view/aside/div[2]/ul").find_elements_by_css_selector("li")
    round_count = len(round_marker_list)
    assert round_count == 10
    round_complete = 0
    min_needed = int(round_count * .6)
    while round_complete <= min_needed:
        time.sleep(7.5)
        # at onset of round, we need to get all the elements of the game:
        round_path = driver.find_element_by_xpath("/html/body/section/div/ui-view/div[3]/div/div[2]/div[1]/div/div/img").get_attribute("src")
        for i in range (1, 4):
            guess = driver.find_element_by_xpath("// *[ @ id = \"app-container\"] / div["+str(i)+"] / div[3] / div[2] / img").get_attribute("src")
            if guess == round_path:
                num = i
                break
        driver.find_element_by_xpath("// *[ @ id = \"app-container\"] / div["+str(num)+"]").click()
        round_complete+=1
    while round_complete < round_count:
        time.sleep(7.5)
        # at onset of round, we need to get all the elements of the game:
        round_option_list = []
        for i in range(1, 4):
            round_option_list.append(driver.find_element_by_xpath("//*[@id=\"app-container\"]/div[" + str(i) + "]"))
        assert len(round_option_list) == 3
        values_guessed = set()
        correct = False
        while not correct:
            guess = get_rand_num()
            if guess not in values_guessed:
                option = round_option_list[guess]
                values_guessed.add(guess)
                option.click()
                attribute = option.get_attribute("class")
                print(attribute)
                if attribute == "option-container ng-scope true" or attribute == "option-container ng-scope ng-animate true-add":
                    round_option_list.clear()
                    values_guessed.clear()
                    attribute = ""
                    round_complete += 1
                    correct = True
                else:
                    time.sleep(3)





# this driver attempts to play the game to get a score of 100%
def max_score_game_driver():
    # we need to get the num of rounds:
    round_marker_list = driver.find_element_by_xpath(
        "/html/body/section/div/ui-view/aside/div[2]/ul").find_elements_by_css_selector("li")
    round_count = len(round_marker_list)
    assert round_count == 10
    round_complete = 0
    while round_complete <= round_count:
        time.sleep(7.5)
        # at onset of round, we need to get all the elements of the game:
        round_path = driver.find_element_by_xpath(
            "/html/body/section/div/ui-view/div[3]/div/div[2]/div[1]/div/div/img").get_attribute("src")
        for i in range(1, 4):
            guess = driver.find_element_by_xpath(
                "// *[ @ id = \"app-container\"] / div[" + str(i) + "] / div[3] / div[2] / img").get_attribute("src")
            if guess == round_path:
                num = i
                break
        driver.find_element_by_xpath("// *[ @ id = \"app-container\"] / div[" + str(num) + "]").click()
        round_complete += 1


def get_rand_num():
    return randint(0, 2)


main()
