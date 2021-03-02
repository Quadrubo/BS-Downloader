from selenium import webdriver
from time import sleep
import os
import shutil

# The profile where I enabled the VPN previously using the GUI.
from selenium.webdriver.common.keys import Keys

OPERA_DLFOLDER = "C:\OperaDownloads"
OPERA_PROFILE = r'C:\\Users\\julwe\\AppData\\Roaming\\Opera Software\\Opera Stable'
OPERA_BIN = r'C:\\Users\\julwe\\AppData\\Local\\Programs\Opera\\74.0.3911.107\\opera.exe'

opera_profile = OPERA_PROFILE
options = webdriver.ChromeOptions()
options.add_argument('user-data-dir=' + opera_profile)
options.add_argument("disable-blink-features=AutomationControlled")
options._binary_location = OPERA_BIN
driver = webdriver.Opera(executable_path='./operadriver.exe', options=options)

website = input("Website: ")

save_dir = input("Save dir: ")

input("Press Enter if your Opera Downloads are empty, there are no other tabs open in Opera and ublockorigin blocks popups from your site.")
already_exist = int(input("How many already exist? "))


driver.get(website)

curr_window = driver.current_window_handle

table = driver.find_element_by_xpath('//*[@id="root"]/section/table')

tr_list = table.find_elements_by_tag_name('tr')

folgen_arr = []

for entry in tr_list:
    folge_link = entry.find_elements_by_tag_name('a')[0].get_attribute('href')
    folge_nbr = entry.find_elements_by_tag_name('a')[0].text
    folge_name = entry.find_elements_by_tag_name('a')[1].text
    folge_name = folge_name.replace("\\", "")
    folge_name = folge_name.replace("/", "")
    folge_name = folge_name.replace(":", "")
    folge_name = folge_name.replace("*", "")
    folge_name = folge_name.replace("?", "")
    folge_name = folge_name.replace("\"", "")
    folge_name = folge_name.replace("<", "")
    folge_name = folge_name.replace(">", "")
    folge_name = folge_name.replace("|", "")

    tmpstr = ""

    flnbrle = 4 - len(folge_nbr)
    for i in range(flnbrle):
        tmpstr += "0"

    tmpstr += folge_nbr
    folge_nbr = tmpstr

    folgen_arr.append([folge_link, folge_nbr, folge_name, ""])

print(folgen_arr)

sleep(1)

title_líst = []

folge_counter = 0
for folge in folgen_arr:
    if folge_counter < already_exist:
        for file in os.listdir(OPERA_DLFOLDER):
            print(file)
            ending = file.rsplit(".")[-1]
            if file in title_líst:
                continue
            else:
                folgen_arr[folge_counter][3] = file
                title_líst.append(file)
                break
        folge_counter += 1
        continue

    driver.get(folge[0])

    sleep(1)

    play_button = driver.find_element_by_xpath('//*[@id="root"]/section/div[8]/div[1]')

    play_button.click()

    sleep(5)

    loop = True
    while loop:
        vscheck = driver.find_element_by_xpath("/html/body/div[4]")
        sleep(1)
        if "visible" in vscheck.get_attribute("style"):
            print("Captcha found, Human needed O.O")
        else:
            print("Captcha solved. Good job Human :)")
            loop = False

    sleep(1)

    driver.get(driver.find_element_by_xpath('//*[@id="root"]/section/div[8]/a').get_attribute('href'))

    dnl_link = driver.find_element_by_tag_name('source').get_attribute('src')

    """
    try:
        driver.switch_to.window(driver.window_handles[1])
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    except:
        print("Error")
    """

    driver.get(dnl_link)

    input("If you downloaded the file, press Enter!")

    for file in os.listdir(OPERA_DLFOLDER):
        print(file)
        ending = file.rsplit(".")[-1]
        if ending == "opdownload":
            file = file[0:-11]
            print(file)
        if file in title_líst:
            continue
        else:
            folgen_arr[folge_counter][3] = file
            title_líst.append(file)
            break

    sleep(1)

    folge_counter += 1

    for file in os.listdir(OPERA_DLFOLDER):
        ending = file.rsplit(".")[-1]
        if ending == "opdownload":
            continue
        elif ending == "mp4":
            folgen_arr_counter = 0
            for folge in folgen_arr:
                if folge[3] == file:
                    os.rename(os.path.join(OPERA_DLFOLDER, file), os.path.join(OPERA_DLFOLDER, folge[1] + ".mp4"))
                    folgen_arr[folgen_arr_counter][3] = folge[1] + ".mp4"
                    tl_counter = 0
                    for dings in title_líst:
                        if dings == file:
                            title_líst[tl_counter] = folge[1] + ".mp4"
                            break
                        tl_counter += 1
                    break
                folgen_arr_counter += 1

            print(folgen_arr)
            print(title_líst)

downloading = False
while downloading:
    for file in os.listdir(OPERA_DLFOLDER):
        if file.rsplit(".")[-1] == "opdownload":
            downloading = True
    print("Still downloading, will wait...")
    sleep(1)

for file in os.listdir(OPERA_DLFOLDER):
    for folge in folgen_arr:
        if folge[3] == file:
            # new_name = folge[1] + "_" + folge[2] + ".mp4"
            new_name = folge[3].split(".")
            new_name = int(new_name[0])
            new_name = str(new_name) + ".mp4"
            os.rename(os.path.join(OPERA_DLFOLDER, file), os.path.join(OPERA_DLFOLDER, new_name))


for file in os.listdir(OPERA_DLFOLDER):
    shutil.move(os.path.join(OPERA_DLFOLDER, file), os.path.join(save_dir, file))


driver.quit()