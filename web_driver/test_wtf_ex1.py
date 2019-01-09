import random
import time
from selenium import webdriver


use_animation = True
users = ['Sam Cooke', 'Mistah Nelson', 'John Smith']


def pause(wait=use_animation, time_out=0.5):
    if wait:
        time.sleep(time_out)


for user in users:
    d = webdriver.Chrome()
    d.get('http://localhost:5000/')
    #
    d.find_element_by_name('username').send_keys(user)
    pause()
    test_age = random.randint(18, 99)
    d.find_element_by_name('age').send_keys(test_age)
    pause()
    d.find_element_by_name('accept_rules').click()
    # d.find_elements_by_class_name('submit')[0].click()
    # d.find_element_by_class_name('submit').click()
    pause()
    d.find_element_by_name('sub_mittor').click()
    #
    pause()
    d.close()

print("Test finished!")
