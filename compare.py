from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time 


def norm_text(string):
    string = string.replace("\n"," ")
    string = " ".join([t.strip() for t in string.split()])
    return string 

def extract_difference(string1, string2):
    # Tìm vị trí bắt đầu sự khác biệt
    #gia su string 2 < string 1
    start_diff_index = 0
    
    # Tìm vị trí bắt đầu sự khác biệt
    # for i in range(min(len(string1), len(string2))):
    #     if string1[i] != string2[i]:
    #         start_diff_index = i
    #         break
    # else:
    #     # Nếu không có sự khác biệt trong đoạn đầu
    #     if len(string1) == len(string2):
    #         return ""  # Không có sự khác biệt
    #     start_diff_index = min(len(string1), len(string2))

    # # Tìm sự khác biệt từ vị trí bắt đầu
    # difference = string1[start_diff_index:]
    start_index, end_index = 0 , 0
    flag = False
    for i in range(len(string2)):
        if string1[i] != string2[i]:
            start_index = i
            flag = True 
            break      
    
    if flag == False :
        start_index = len(string2) - 1 # the final index of the list 

    string1_reverse = string1[::-1]
    string2_reverse = string2[::-1]

    flag = False 
    for i in range(len(string2_reverse)):
        # print(i)
        if string1_reverse[i] != string2_reverse[i]:
            end_index = i
            flag = True
            break 
    if flag == False :
        end_index = len(string2_reverse) - 1 # the final index of the list 

    # print('len', len(string2_reverse))
    # print(start_index , end_index)
    return string1[start_index : -(end_index) - 1 ]

def craw():
    # Khởi tạo trình duyệt Chrome
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')  # Optional, run in headless mode if you don't need a UI
    # options.add_argument('--disable-gpu')  # Disable GPU acceleration (optional)
    # options.add_argument('--no-sandbox')  # Added for certain environments

    # Automatically download and set up ChromeDriver
    # service = Service(ChromeDriverManager().install())
    service = Service('./chromedriver')
    driver = webdriver.Chrome(service=service, options=options)

    # Truy cập vào URL bài báo khoa học
    driver.get('https://ieeexplore.ieee.org/abstract/document/9078366')

    try:
        # # Chờ cho thẻ <a> hiển thị và có thể click được
        # citation_link = WebDriverWait(driver, 10).until(
        #     EC.element_to_be_clickable((By.XPATH, '//a[@class="anchor anchor-primary" and @data-sd-ui-side-panel-opener="true" and @data-xocs-content-id="b24" and @data-xocs-content-type="reference" and @href="#b24" and @name="bb24"]'))
        # )

        citation_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'context_ref_1_1'))  # Sử dụng ID để tìm thẻ <a>
        )
        # Click vào thẻ <a>
        citation_link.click()
        print("Đã click vào thẻ citation.")

        # Chờ cho panel hoặc phần tử mới xuất hiện sau khi click
        time.sleep(3)  # Đợi để panel hoặc phần tử mới xuất hiện (thời gian có thể điều chỉnh)

        # Lưu trạng thái DOM sau khi click
        new_dom = driver.page_source

        with open('new_element.txt' , 'w') as f:
            new_dom = BeautifulSoup(new_dom, 'html.parser')
            f.write(new_dom.get_text())

    finally:
        # Đóng trình duyệt
        driver.quit()

if __name__ == '__main__':
    # string1 = """1. L. D. Baskar, J. Hellendoorn, B. De Schutter and Z. Papp, "Traffic control and intelligent vehicle highway systems: A survey", IET Intell. Transp. Syst., vol. 5, no. 1, pp. 38-52, Mar. 2011.Show All ReferencesShow All ReferencesAuthorsFiguresReferencesCitationsKeywordsMetricsFootnotes More Like This Efficient Deep Learning Hyperparameter Tuning Using Cloud Infrastructure: Intelligent Distributed Hyperparameter Tuning with Bayesian Optimization in the Cloud2019 IEEE 12th International Conference on Cloud Computing (CLOUD)Published: 2019Deep Learning on Active Sonar Data Using Bayesian Optimization for Hyperparameter Tuning2020 25th International Conference on Pattern Recognition (ICPR)Published: 2021Show MoreReferencesReferences is not available for this document.IEEE Personal AccountChange username/passwordPurchase DetailsPayment OptionsView Purchased DocumentsProfile InformationCommunications PreferencesProfession and EducationTechnical interestsNeed Help? US & Canada: +1 800 678 4333  Worldwide: +1 732 981 0060  Contact & Support FollowAbout IEEE Xplore | Contact Us | Help | Accessibility | Terms of Use | Nondiscrimination Policy | IEEE Ethics Reporting | Sitemap | IEEE Privacy Policy A not-for-profit organization, IEEE is the world's largest technical professional organization dedicated to advancing technology for the benefit of humanity.  © Copyright 2024 IEEE - All rights reserved, including rights for text and data mining and training of artificial intelligence and similar technologies.""" 
    # string2 = """AuthorsFiguresReferencesCitationsKeywordsMetricsFootnotes More Like This Efficient Deep Learning Hyperparameter Tuning Using Cloud Infrastructure: Intelligent Distributed Hyperparameter Tuning with Bayesian Optimization in the Cloud2019 IEEE 12th International Conference on Cloud Computing (CLOUD)Published: 2019Deep Learning on Active Sonar Data Using Bayesian Optimization for Hyperparameter Tuning2020 25th International Conference on Pattern Recognition (ICPR)Published: 2021Show MoreReferencesReferences is not available for this document.IEEE Personal AccountChange username/passwordPurchase DetailsPayment OptionsView Purchased DocumentsProfile InformationCommunications PreferencesProfession and EducationTechnical interestsNeed Help? US & Canada: +1 800 678 4333  Worldwide: +1 732 981 0060  Contact & Support FollowAbout IEEE Xplore | Contact Us | Help | Accessibility | Terms of Use | Nondiscrimination Policy | IEEE Ethics Reporting | Sitemap | IEEE Privacy Policy A not-for-profit organization, IEEE is the world's largest technical professional organization dedicated to advancing technology for the benefit of humanity.  © Copyright 2024 IEEE - All rights reserved, including rights for text and data mining and training of artificial intelligence and similar technologies."""
    
    # # string1, string2 = 'abcdef' , 'cdef'


    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')  # Optional, run in headless mode if you don't need a UI
    # options.add_argument('--disable-gpu')  # Disable GPU acceleration (optional)
    # options.add_argument('--no-sandbox')  # Added for certain environments

    # # Automatically download and set up ChromeDriver
    # # service = Service(ChromeDriverManager().install())
    service = Service('./chromedriver')
    driver = webdriver.Chrome(service=service, options=options)

    # Truy cập vào URL bài báo khoa học
    driver.get('https://www.sciencedirect.com/science/article/pii/S0952197623002282')

    try:
        # # Chờ cho thẻ <a> hiển thị và có thể click được
        citation_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//a[@class="anchor anchor-primary" and @data-sd-ui-side-panel-opener="true" and @data-xocs-content-id="b35" and @data-xocs-content-type="reference" and @href="#b35" and @name="bb35"]'))
        )

        # citation_link = WebDriverWait(driver, 10).until(
        #     EC.element_to_be_clickable((By.ID, 'ref-link-section-d7069354e385'))  # Sử dụng ID để tìm thẻ <a>
        # )
        # Click vào thẻ <a>
        citation_link.click()
        print("Đã click vào thẻ citation.")

        # Chờ cho panel hoặc phần tử mới xuất hiện sau khi click
        time.sleep(3)  # Đợi để panel hoặc phần tử mới xuất hiện (thời gian có thể điều chỉnh)

        # Lưu trạng thái DOM sau khi click
        new_dom = driver.page_source
        
        with open('new_element.txt' , 'w') as f:
            new_dom = BeautifulSoup(new_dom, 'html.parser')
            f.write(new_dom.get_text())

    finally:
        # Đóng trình duyệt
        driver.quit()


    with open('old_text.txt' , 'r') as f:
        old_text = f.read().strip()

    with open('new_element.txt' , 'r') as f:
        new_text = f.read().strip()

    print(extract_difference(norm_text(new_text), norm_text(old_text)))