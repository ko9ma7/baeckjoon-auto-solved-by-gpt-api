import time
import openai
import pyperclip
import pyautogui

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from my_module.create_chrome_driver import create_driver


def execute_macro():
    # api key
    api_key = r'여기에 개인 API를 입력'

    openai.api_key = api_key

    # chrome driver create
    driver = create_driver()

    # solved ac connect
    driver.get(r'https://solved.ac/')
    time.sleep(1)

    # 문제 text click
    quiz_text = driver.find_element(By.CSS_SELECTOR, '#__next > nav > div > div.css-fwjeue > span:nth-child(2) > a')
    time.sleep(1)
    quiz_text.click()
    time.sleep(1)

    # bronze quiz click
    quiz_text = driver.find_element(By.CSS_SELECTOR,
                                    '#__next > div.css-1948bce > div.css-qijqp5 > table > tbody > tr:nth-child(3) > td:nth-child(2) > a > div')
    time.sleep(1)
    quiz_text.click()
    time.sleep(1)

    # quiz number and quiz name parsing
    quiz_num = driver.find_element(By.CSS_SELECTOR,
                                   '#__next > div.css-1948bce > div:nth-child(4) > div.css-qijqp5 > table > tbody > tr:nth-child(1) > td:nth-child(1) > div > div > div > span > a > span')
    quiz_num = quiz_num.text

    quiz_text = driver.find_element(By.CSS_SELECTOR,
                                    '#__next > div.css-1948bce > div:nth-child(4) > div.css-qijqp5 > table > tbody > tr:nth-child(1) > td:nth-child(2) > span > div > div.css-ov1ktg > span.css-3c2y35 > div > a > span > span')
    quiz_name = quiz_text.text
    time.sleep(1)

    # quiz baeckjonn site connect
    quiz_text.click()
    time.sleep(1)

    # quiz info parsing
    quiz_content_quiz = driver.find_element(By.CSS_SELECTOR, '#problem_description > p').text
    quiz_content_input = driver.find_element(By.CSS_SELECTOR, '#problem_input > p').text
    quiz_content_output = driver.find_element(By.CSS_SELECTOR, '#problem_output > p').text
    quiz_content_example_input = driver.find_element(By.CSS_SELECTOR, '#sample-input-1').text
    quiz_content_example_output = driver.find_element(By.CSS_SELECTOR, '#sample-output-1').text
    time.sleep(2)

    # create quiz question
    gpt_question = f"Baekjoon '{quiz_num}' coding test quiz" \
                   f"'{quiz_name}' python code please. " \
                   f"\n'{quiz_content_quiz}'" \
                   f"\n' {quiz_content_input}'" \
                   f"\n'{quiz_content_output}'" \
                   f"'{quiz_content_example_input}'" \
                   f"\nThis is quiz example input" \
                   f"'{quiz_content_example_output}'" \
                   f"\nand this is quiz example output"
    print(gpt_question)

    # submit btn click
    submit_quiz_text = driver.find_element(By.CSS_SELECTOR,
                                           'body > div.wrapper > div.container.content > div.row > div:nth-child(2) > ul > li:nth-child(2) > a')
    time.sleep(1)
    submit_quiz_text.click()
    time.sleep(1)

    # gpt answer create
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": gpt_question
            }
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # gpt answer response
    content = response.choices[0].message.content
    print('-' * 10)

    # python code of gpt answer parsing
    code_start = content.find('```') + 3  # '```' 다음의 인덱스를 찾습니다.
    code_end = content.rfind('```')  # 마지막 '```'의 인덱스를 찾습니다.
    code = content[code_start:code_end].strip()
    code = code.replace('python', '')
    print(code)

    # baeckjoon tab by code input div
    for _ in range(30):
        pyautogui.hotkey('tab')

    # python code clipboard copy and paste
    pyperclip.copy(code)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)

    # submit button click
    btn_submit = driver.find_element(By.CSS_SELECTOR, '#submit_button')
    time.sleep(1)
    btn_submit.click()
