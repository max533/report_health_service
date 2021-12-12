import ast
import datetime
import json
import logging
import os
import random
import sys
import time

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

logger.setLevel(os.environ.get('LOG_LEVEL', 'DEBUG'))
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(os.environ.get('LOG_LEVEL', 'DEBUG'))
log_format = '%(asctime)s - %(module)s - line_number : %(lineno)d - %(name)s - %(levelname)s - %(message)s'
formatter = logging.Formatter(log_format)
handler.setFormatter(formatter)
logger.addHandler(handler)


class HealthReportService:

    employee_id = os.environ.get('EMPLOYEE_ID', None)
    report_form_url = os.environ.get('REPORT_FORM_URL', None)
    report_page_url = os.environ.get('REPORT_PAGE_URL', None)
    login_form_url = os.environ.get('LOGIN_FORM_URL', None)
    login_page_url = os.environ.get('LOGIN_PAGE_URL', None)
    delay_time_range = int(os.environ.get('DELAY_TIME_RANGE', None))

    def __init__(self):
        referer_site_path = os.environ.get('REFERER_SITE_PATH', None)
        user_agent_path = os.environ.get('USER_AGENT_PATH', None)

        with open(referer_site_path) as f:
            contents = f.read()
            referer_sites = ast.literal_eval(contents)
            referer_site = random.choice(referer_sites)

        with open(user_agent_path) as f:
            user_agent_dict = json.load(f)
            user_agents = []
            for user_agent in user_agent_dict['browsers'].values():
                user_agents.extend(user_agent)
            user_agent = random.choice(user_agents)

        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", # noqa
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "Host": "familyweb.wistron.com",
            "Sec-Ch-Ua": "\" Not;A Brand\";v=\"99\", \"Google Chrome\";v=\"91\", \"Chromium\";v=\"91\"",
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": user_agent,
            "Referer": referer_site,
        }

        with requests.session() as session:
            self.session = session
            self.check_login_page()
            self.user_login()
            self.check_report_page()
            self.report_health_status()

    def check_login_page(self):
        delay_time = random.randint(1, self.delay_time_range)
        time.sleep(delay_time)

        try:
            res = self.session.get(self.login_page_url)
        except Exception as err:
            error_info = {
                "user": self.employee_id,
                "error_message": err,
                "url": self.login_page_url
            }
            logger.error(error_info, exc_info=True)
            raise requests.ConnectionError

        if res.status_code != 200:
            error_info = {
                "user": self.employee_id,
                "error_message": res.text,
                "status_code": res.status_code,
                "url": self.login_page_url,
            }
            logger.error(error_info)
            raise requests.ConnectionError

    def user_login(self):
        delay_time = random.randint(1, self.delay_time_range)
        time.sleep(delay_time)

        login_payload = {"userpass": self.employee_id}
        session = self.session

        try:
            res = session.post(self.login_form_url, data=login_payload, headers=self.headers)
        except Exception as err:
            error_info = {
                "user": self.employee_id,
                "error_message": err,
                "url": self.report_page_url
            }
            logger.error(error_info, exc_info=True)

        soup = BeautifulSoup(res.text, features="html.parser")
        form_hidden_data = soup.find_all("input", type='hidden')

        self.form_hidden_fields = {}
        for from_field in form_hidden_data:
            self.form_hidden_fields[from_field['name']] = from_field['value']

        self.session = session
        self.cookie = session.cookies.copy()

    def check_report_page(self):
        delay_time = random.randint(1, self.delay_time_range)
        time.sleep(delay_time)

        try:
            res = self.session.get(self.report_page_url)
        except Exception as err:
            error_info = {
                "user": self.employee_id,
                "error_message": err,
                "url": self.report_page_url
            }
            logger.error(error_info, exc_info=True)
            raise requests.ConnectionError

        if res.status_code != 200:
            error_info = {
                "user": self.employee_id,
                "error_message": res.text,
                "status_code": res.status_code,
                "url": self.report_page_url,
            }
            logger.error(error_info)
            raise requests.ConnectionError

    def report_health_status(self):
        report_status = "not complete"
        while report_status == "not complete":
            delay_time = random.randint(1, self.delay_time_range)
            time.sleep(delay_time)

            session = self.session
            health_report_payload = {
                'measure_date': datetime.date.today().strftime("%Y/%m/%d"),
                'symptom': 1,
                'commute_way': os.environ.get('COMMUTE_WAY', 5),
                'notice': 1,
                'notice_home': 1,
            }
            health_report_payload.update(self.form_hidden_fields)
            logger.debug(len(health_report_payload))
            logger.debug(health_report_payload)
            try:
                res = session.post(
                    self.report_form_url,
                    data=health_report_payload,
                    headers=self.headers,
                    cookies=self.cookie,
                )
            except Exception as err:
                error_info = {
                    "user": self.employee_id,
                    "error_message": err,
                    "url": self.report_page_url
                }
                logger.error(error_info, exc_info=True)
                raise requests.ConnectionError

            report_successfully_content = '回報資料已經順利送出！'
            report_repeatedly_content = '此日期的回報已經存在了！'

            if res.status_code == 200 and report_successfully_content in res.text:
                report_status = 'complete'
                log_message = {
                    'user': self.employee_id,
                    'report_status': report_status,
                    'report_date': datetime.date.today().strftime("%Y/%m/%d"),
                }
                logger.info(log_message)
            elif res.status_code == 200 and report_repeatedly_content in res.text:
                report_status = 'complete but repeatedly'
                log_message = {
                    'user': self.employee_id,
                    'report_status': report_status,
                    'report_date': datetime.date.today().strftime("%Y/%m/%d"),
                }
                logger.info(log_message)
            else:
                log_message = {
                    'user': self.employee_id,
                    'report_status': 'not complete',
                    'status_code': res.status_code,
                    'error_message': res.text
                }
                logger.warning(log_message)


if __name__ == '__main__':
    start_time = datetime.datetime.now()

    HealthReportService()

    end_time = datetime.datetime.now()
    duration = end_time - start_time
    logger.info(f"This health report program takes {duration.seconds} s")
