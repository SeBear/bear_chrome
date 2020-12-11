import re
import os
import requests
import threading

import selenium.webdriver

import urllib.parse as URLdecode
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains


class Chrome(selenium.webdriver.Chrome):

    def __init__(self,
                 working_dir=os.path.abspath(os.curdir),
                 download_dir="\\Downloads\\",
                 DEBUG = False,
                 **kwargs):
        """
        Initiazizing Chrome and its deafult load directory
        :type workingDir: path-like:
        :type download_dir: path-like:
        """

        # настройка chrome
        def chrome_set_options(binary_location=working_dir + "\\chrome-bin\\chrome.exe"):
            """
            :type binary_location: path-like:
            """
            options = selenium.webdriver.ChromeOptions()
            # options.add_experimental_option("prefs",{"download.default_directory": workingDir + "\\puraches\\" + number ,"download_restrictions": 0}) #Место загрузки по умолчанию
            options.binary_location = binary_location
            options.headless = not DEBUG
            return options

        self.w_dir = working_dir
        super().__init__('chromedriver.exe', options=chrome_set_options())
        self.page_load_time = 3
        self.loader = FileLoader(download_dir)

    def await_for_element_presentation(self, by_method, expression, scroll_into_view = True):
        if by_method == 'XPATH':
            is_presented = expected_conditions.presence_of_element_located((By.XPATH, expression))
        elif by_method == 'NAME':
            is_presented = expected_conditions.presence_of_element_located((By.NAME, expression))
        elif by_method == 'PART_OF_LINK':
            is_presented = expected_conditions.presence_of_element_located((By.PARTIAL_LINK_TEXT, expression))
        elif by_method == 'ID':
            is_presented = expected_conditions.presence_of_element_located((By.ID, expression))
        elif by_method == 'CSS_SELECTOR':
            is_presented = expected_conditions.presence_of_element_located((By.CSS_SELECTOR, expression))
        else:
            raise ValueError("No search method called ", f"{by_method}",
                             " declared in Chrome.await_for_element_presentation.")
        try:
            element = WebDriverWait(self, self.page_load_time).until(is_presented)
            ActionChains(self).move_to_element(element).perform()
            return element
        except TimeoutException:
            print("Can not find element by", by_method, expression)

    def move_to(self, element):
        ActionChains(self).move_to_element(element).perform()

    def popup(self):

        def _ancestor():
            self.current_window_handle()

        alert = self.switch_to.alert()
        ancestor = _ancestor()

        def do_nothing():
            self.switch_to.window(ancestor)
        def yes():
            alert.accept()
        def no():
            alert.dismiss()
        def text():
            text = alert.get_text()
        def send(str):
            alert.send_keys(str)

class FileLoader():

    def __init__(self, load_folder="Downloads"):
        self.set_directory(load_folder)

    def set_directory(self, load_folder=""):
        self.load_dir = f"{os.path.abspath(os.curdir)}\\{load_folder}"
        self.ensure_load_dir_exists()

    def ensure_load_dir_exists(self):
        try:
            os.mkdir(self.load_dir)
        except FileExistsError:
            pass

    def form_default_header(self, hostname):
        """
            IDK how but it works almost everywhere
            TODO: Get info how the fuck it works
            """
        headers = {"Host": f"{hostname}",
                   "Connection": "keep-alive",
                   "Upgrade-Insequre-Requests": "1",
                   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 YaBrowser/19.12.4.25 Yowser/2.5 Safari/537.36",
                   "Sec-Fetch-User": "?1",
                   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
                   "Sec-Fetch-Size": "same-origin",
                   "Sec-Fetch-Mode": "navigate",
                   # "Accept-Encoding": "gzip, deflate, br",
                   "Accept-Language": "ru,en;q=0.9"}
        return headers

    def download(self, link, params=""):
        """
        :type link: http-link:
        :type params: dict {"id": user-id}: sql-args: goes-after-\"?":

        Method to load files;
        Get header "hostname" from link
        Create folder to load in
        Generate headers
        Form request
        Get filename
        Download // w-open: req: 1024B chunks
        """
        hostname = re.match(r"https://(.*?)/.*?", link)[1]
        self.ensure_load_dir_exists()
        # TODO: Do it when HEADERS are not sent (NO **ARGS). Add **args and if-check
        headers = self.form_default_header(hostname)
        request = requests.get(link, params=params, headers=headers)

        def get_filename(request):
            try:
                disp = request.headers['Content-Disposition']
            except KeyError:
                disp = "filename=\"NAME_NOT_FOUND\""
            name = re.search(r"filename=\"(.*?)\"", disp)[1]
            encodedName = name.encode("ISO-8859-1", errors="ignore")
            name = str(encodedName, encoding="utf-8")
            return name

        def ensure_filename_not_exists(name):
            i = 1
            encodedName = name
            while encodedName in os.listdir(self.load_dir):
                encodedName = re.search(r"(.*?)(\..*?\Z)", name)[1] + "(" + str(i) + ")" + \
                              re.search(r"(.*?)(\..*?\Z)", name)[2]
                i = i + 1
            name = encodedName
            name = URLdecode.unquote(name)
            return name

        def download(name, load_dir, request):
            with open(load_dir + "\\" + name, 'wb') as f:
                for chunk in request.iter_content(chunk_size=1024):
                    if chunk: f.write(chunk)

        filename = ensure_filename_not_exists(get_filename(request))
        download(filename, self.load_dir, request)

    def download_many(self, links):
        """
        :type links: list
        """
        for cur_link in links:
            self.download(cur_link)
