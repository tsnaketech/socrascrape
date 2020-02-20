#!/usr/bin/python3
# -*- coding: utf-8 -*-

###### Import ########

import csv
import os
import re
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from time import sleep

import constant

###### Variable ######

folder = "./geckodriver/"
exec_path = folder + "geckodriver.exe"
log_file = folder + "geckodriver.log"

url = constant.url

room = constant.room
student = constant.username

###### Function ######

def checkProgress(browser):
    progress = browser.find_element_by_class_name("quiz-progress-text").text
    progress = progress.split()
    return (progress[0] == progress[2])

def getQuestion(browser):
    return browser.find_element_by_class_name("question-text").text

def passList(browser):
    if (browser.find_element_by_class_name("mc-answer-area")):
        browser.find_element_by_class_name("answer-option-letter").click()

def passTextArea(browser):
    if (browser.find_element_by_class_name("question-answer-container")):
        browser.find_element_by_class_name("fr-question-textarea").send_keys('so good')

def clickNext(browser):
    browser.find_element_by_id("submit-button").click()

###### Program #######

if __name__ == "__main__":
    browser = webdriver.Firefox(executable_path=exec_path, service_log_path=log_file)
    browser.get(url)
    sleep(1)
    browser.find_element_by_id("studentRoomName").send_keys(room)
    browser.find_element_by_id("studentLoginButton").click()
    sleep(3)
    try:
        browser.find_element_by_id("student-name-input").send_keys(student)
    except:
        sleep(5)
        browser.find_element_by_id("student-name-input").send_keys(student)
    browser.find_element_by_id("submit-name-button").click()
    sleep(3)

    with open('questions.csv', mode='w',newline='') as f:
        writer = csv.writer(f, delimiter=";")
        while True:
            question = getQuestion(browser)
            print(question)
            try:
                passList(browser)
            except:
                passTextArea(browser)
            writer.writerow([question])
            if(checkProgress(browser)):
                break
            clickNext(browser)
    browser.quit()
    exit(0)