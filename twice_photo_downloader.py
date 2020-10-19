from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from tqdm import tqdm
import re, os, uuid, datetime, sys, ctypes
import urllib.request
import requests, warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)


download_title = []
download_url = []
download_img = []

page_to = 0
page_from = 0
select = 0
index_data = 0
path = ''
counting = 1
re_chk = True
driver = None

mina = r'\b미나\b|\b블랙스완\b|\b미나리\b|\b미구리\b|\b펭귄\b|\b임미나\b'
jungyeon = r'\b정연\b|\b윾\b|\b유장꾸\b|\b정연맘\b'
tzuyu = r'\b쯔위\b|\b조쯔위\b|\b쯔뭉이\b'
jihyo = r'\b지효\b|\b죠\b|\b리더효\b|\b효리다\b'
nayeon = r'\b나연\b|\b맏내\b|\b나봉\b|\b나봉스\b|\b나부기\b'
chaeyeong = r'\b채영\b|\b챙\b|\b아기맹수\b|\b딸기공주\b'
sana = r'\b사나\b|\b사나[짱쨩]\b|\b샤샤\b|\b샤나\b|\b사또떨\b|\b사토끼\b|\b사낫찌\b'
dahyeon = r'\b둡\b|\b다현\b|\b두부\b|\b둡저씨\b'
momo = r'\b모모\b|\b모모링\b|\b모구리\b'

def OpenWebBrowser():
    global driver
    if driver == None:
        driver = webdriver.Chrome('chromedriver')
        driver.get('https://nid.naver.com/nidlogin.login')
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#PM_ID_ct > div.header > div.special_bg > div > div.area_logo > h1 > a > span')))
    else:
        pass

def Init():
    global download_img, download_title, download_url, page_from, page_to, path, select, index_data, counting, re_chk

    download_title.clear()
    download_url.clear()
    download_img.clear()

    page_to = 0
    page_from = 0
    select = 0
    index_data = 0
    path = ''
    counting = 1
    re_chk = True

def SelectMember(index):
    global select, path
    if index == 1:
        select = mina
        path = 'Mina'
    elif index == 2:
        select = jungyeon
        path = 'Jungyeon'
    elif index == 3:
        select = tzuyu
        path = 'Tzuyu'
    elif index == 4:
        select = jihyo
        path = 'Jihyo'
    elif index == 5:
        select = nayeon
        path = 'Nayeon'
    elif index == 6:
        select = chaeyeong
        path = 'Chaeyeong'
    elif index == 7:
        select = sana
        path = 'Sana'
    elif index == 8:
        select = dahyeon
        path = 'Dahyeon'
    elif index == 9:
        select = momo
        path = 'Momo'
    elif index == 0:
        select = 0
        path = 'Group'
    else:
        select = 0

def Input():
    global page_to, page_from
    print('몇 페이지 부터 몇 페이지 까지 다운로드 받을까요? [ 1-1000 페이지까지 가능 ]')
    page_from = int(input('From : '))
    page_to = int(input('To : '))
    print('어떤 멤버의 사진을 다운로드 받으실건가요? [ 숫자로만 입력! ]')
    print('[ 1.미나 2.정연 3.쯔위 4.지효 5.나연 6.채영 7.사나 8.다현 9.모모 0.전체 ]')
    index_data = int(input('입력 : '))
    SelectMember(index_data)

    if page_to < 1 or page_from > 1000:
        print('페이지 범위를 넘었습니다.\n')
        Input()

def FindPhoto():
    global driver
    print('해당 하는 멤버의 사진을 찾고있어요!')
    for i in range(page_from, page_to+1):
        URL = 'https://cafe.naver.com/twfan?iframe_url=/ArticleList.nhn%3Fsearch.clubid=29072006%26search.menuid=20%26search.boardtype=I%26search.questionTab=A%26search.totalCount=201%26search.page={0}'.format(i)
        driver.get(URL)

        iframe_element = driver.find_element_by_css_selector('iframe#cafe_main')
        driver.switch_to_frame(iframe_element)
        getdata = driver.find_elements_by_css_selector('#main-area > ul > li > dl > dt > a.m-tcol-c')
        for data in getdata:
            download_title.append(data.text)
            download_url.append(data.get_attribute('href'))

    k = 0
    while k < len(download_url):
        if select != 0:
            result = re.search(pattern=select, string=download_title[k])
            if result != None:
                k += 1
                continue
            else:
                download_url.pop(k)
                download_title.pop(k)
        else:
            break

    for j in range(0, len(download_url)):
        driver.get(download_url[j])
    
        iframe_element = driver.find_element_by_css_selector('iframe#cafe_main')
        driver.switch_to_frame(iframe_element)
    
        getdata = driver.find_elements_by_css_selector('#tbody > img')
    
        for data in getdata:
            tmp = data.get_attribute('src')
            tmp = tmp.replace('cafeptthumb-phinf','cafefiles')
            src = tmp.replace('?type=w740', '')
            download_img.append(src)

def Download():
    global path, counting
    print('해당하는 멤버의 사진을 찾았어요 총:{0}개 입니다. 다운로드 받으시겠습니까?[Y/N] : '.format(len(download_img)))
    string = input()
    if string == 'y' or string == 'Y':
        print('C드라이브에 받으시겠어요? D드라이브에 받으시겠어요?[C/D] : ')
        chk = input()
        if chk == 'c' or chk == 'C':
            print('C드라이브로 다운로드를 시작합니다.')
            directory = 'C:\\TwicePhoto\\{0}'.format(path)
            if not os.path.exists(directory): os.makedirs(directory)
            for a in download_img:
                uid = str(uuid.uuid4())
                file_path = 'C:\\TwicePhoto\\{0}\\{1}_{2}_{3}.{4}'.format(path, path, datetime.datetime.now().strftime('%y%m%d_%H%M%S'), uid.split('-')[0], a.split('.')[-1])
                urllib.request.urlretrieve(a, file_path, reporthook=dlProgress)
                counting += 1
            print('다운로드 완료!')
        elif chk == 'd' or chk == 'D':
            print('D드라이브로 다운로드를 시작합니다.')
            directory = 'D:\\TwicePhoto\\{0}'.format(path)
            if not os.path.exists(directory): os.makedirs(directory)
            for a in download_img:
                uid = str(uuid.uuid4())
                file_path = 'D:\\TwicePhoto\\{0}\\{1}_{2}_{3}.{4}'.format(path, path, datetime.datetime.now().strftime('%y%m%d_%H%M%S'), uid.split('-')[0], a.split('.')[-1])
                urllib.request.urlretrieve(a, file_path, reporthook=dlProgress)
                counting += 1
        else:
            print('잘못 입력하셨습니다. 다시 진행해 주세요.')
            Download()
    elif string == 'n' or string == 'N':
        print('처음 화면으로 돌아갑니다.')
        return False
    else:
        print('잘못 입력하셨습니다. 다시 진행해 주세요.')
        Download()
    print('다운로드 완료!')

def dlProgress(count, blockSize, totalSize):
    global counting
    percent = ((count*blockSize)*100)/totalSize
    if percent > 100:
        percent = 100
    sys.stdout.write('\r다운로드 중... %d%%[전체 %d개 중 %d개 다운로드 완료]' % (percent, len(download_img), counting))
    sys.stdout.flush()
    

def CheckRestart():
    global re_chk
    re_chk = input('다시 사용하시겠습니까?[Y/N] : ')
    if re_chk == 'Y' or re_chk == 'y':
        re_chk = True
        Init()
    elif re_chk == 'N' or re_chk == 'n':
        re_chk = False
    else:
        print('잘못 입력하셨습니다. 다시 진행하여 주십시요.')
        CheckRestart()

if __name__ == "__main__":
    ctypes.windll.kernel32.SetConsoleTitleW("TWICE 사진 다운로더 [⊙Copyright(c)2019 SEOL GANG All rights reserved.]")
    while re_chk:
        Input()
        OpenWebBrowser()
        FindPhoto()
        if Download() == False:
            continue
        CheckRestart()
    print('사용해주셔서 감사합니다. [⊙Copyright(c)2019 SEOL GANG All rights reserved.]')
    driver.quit()
    sys.exit(1)