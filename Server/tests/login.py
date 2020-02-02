#!/usr/bin/env python3

import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

wd = webdriver.Firefox(executable_path = "./geckodriver")

wd.get("http://localhost:5000/login")
wd.find_element_by_css_selector("input[name=username]").send_keys("otrevor")
wd.find_element_by_css_selector("input[name=password]").send_keys("Chicken5436")
wd.find_element_by_css_selector("input[name=submit]").click()
