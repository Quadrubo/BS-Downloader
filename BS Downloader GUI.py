import json
import os
import shutil
import sys

from selenium import webdriver
from seleniumrequests import Opera
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import threading
from time import sleep

from PyQt5.QtCore import pyqtSlot, QDir
from PyQt5.QtWidgets import *
from datetime import datetime



class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.start_log()
        self.get_config()
        self.grid_layout = QGridLayout()

        self.image_folder = QDir.currentPath()

        self.setWindowTitle("BS Downloader 3.0.0-alpha.2")
        self.setLayout(self.grid_layout)

        # Textbox Burning Series Url
        self.label_url = QLabel(self)
        self.label_url.setText("Burning Series Url: ")
        self.grid_layout.addWidget(self.label_url, 0, 0)

        self.textbox_url = QLineEdit(self)
        self.textbox_url.setToolTip("The url of the series you want to download from Burning Series.")
        self.grid_layout.addWidget(self.textbox_url, 0, 1, 1, 3)
        self.textbox_url.editingFinished.connect(self.textbox_change)

        # Save Folder
        self.label_save_folder = QLabel(self)
        self.label_save_folder.setText("Save Folder: ")
        self.grid_layout.addWidget(self.label_save_folder, 1, 0)

        self.button_save_folder = QPushButton("Browse...")
        self.button_save_folder.setToolTip("The folder the series is gonna be saved to, can be auto selected.")
        self.grid_layout.addWidget(self.button_save_folder, 1, 1, 1, 3)

        self.button_save_folder.clicked.connect(self.on_save_folder_click)

        # Download from

        self.label_download_from = QLabel(self)
        self.label_download_from.setText("Download from: ")
        self.grid_layout.addWidget(self.label_download_from, 2, 0)

        self.textbox_download_from = QLineEdit(self)
        self.textbox_download_from.setToolTip("The Episode you want to start downloading at.")

        try:
            fcount = 0
            for file in os.listdir(self.cfg_dlfolder):
                fcount += 1
            self.textbox_download_from.setText(str(fcount + 1))
        except:
            pass
        self.grid_layout.addWidget(self.textbox_download_from, 2, 1)

        # to

        self.label_download_to = QLabel(self)
        self.label_download_to.setText("Download to: ")
        self.grid_layout.addWidget(self.label_download_to, 2, 2)

        self.textbox_download_to = QLineEdit(self)
        self.textbox_download_to.setToolTip("The Episode you want to stop downloading at.")
        self.grid_layout.addWidget(self.textbox_download_to, 2, 3)

        # Preferred Platform

        self.label_preferred_platform = QLabel(self)
        self.label_preferred_platform.setText("Preferred Platform: ")
        self.grid_layout.addWidget(self.label_preferred_platform, 3, 0)

        self.combobox_preferred_platform = QComboBox(self)
        self.combobox_preferred_platform.addItem("Vivo")
        self.combobox_preferred_platform.addItem("Streamtape")
        self.combobox_preferred_platform.addItem("Vupload")
        self.combobox_preferred_platform.addItem("Vidoza")
        self.combobox_preferred_platform.setCurrentIndex(0)
        self.combobox_preferred_platform.setToolTip("The streaming service the series will be downloaded from.")
        self.grid_layout.addWidget(self.combobox_preferred_platform, 3, 1, 1, 3)

        # Use Threading

        self.label_threading = QLabel(self)
        self.label_threading.setText("Threading: ")
        self.grid_layout.addWidget(self.label_threading, 4, 0)

        def box_change():
            if self.checkbox_threading.checkState() == 0:
                self.textbox_threading.setDisabled(True)
            else:
                self.textbox_threading.setEnabled(True)

        self.checkbox_threading = QCheckBox("Use Threading")
        self.checkbox_threading.setChecked(True)
        self.checkbox_threading.setToolTip("Simultaneous Downloads.")
        self.grid_layout.addWidget(self.checkbox_threading, 4, 1)
        self.checkbox_threading.stateChanged.connect(box_change)

        self.textbox_threading = QLineEdit(self)
        self.textbox_threading.setText("5")
        self.textbox_threading.setToolTip("How many simultaneous downloads you want.")
        self.grid_layout.addWidget(self.textbox_threading, 4, 2, 1, 2)

        # Config & Start

        self.button_config = QPushButton(self)
        self.button_config.setText("Config")
        self.button_config.setToolTip("Open the configuration.")
        self.grid_layout.addWidget(self.button_config, 5, 0)

        self.button_config.clicked.connect(self.on_config_click)

        self.button_start = QPushButton(self)
        self.button_start.setText("Start!")
        self.button_start.setToolTip("Start the download.")
        self.grid_layout.addWidget(self.button_start, 5, 1, 1, 3)

        self.button_start.clicked.connect(self.on_start_click)

    def get_config(self):
        open_conf = False

        try:
            with open('config.json') as json_file:
                data = json.load(json_file)
        except:
            open_conf = True

        try:
            self.cfg_dlfolder = data['dlfolder']
            print(self.cfg_dlfolder)
        except:
            self.cfg_dlfolder = ""
            open_conf = True

        try:
            self.cfg_profile = data['profile']
            print(self.cfg_profile)
        except:
            self.cfg_profile = ""
            open_conf = True

        try:
            self.cfg_bin = data['bin']
            print(self.cfg_bin)
        except:
            self.cfg_bin = ""
            open_conf = True

        try:
            self.cfg_ffmpeg = data['ffmpeg']
            print(self.cfg_ffmpeg)
        except:
            self.cfg_ffmpeg = ""
            open_conf = True

        try:
            self.cfg_save_folder_deutsch = data['save_deutsch']
            print(self.cfg_save_folder_deutsch)
        except:
            self.cfg_save_folder_deutsch = ""
            open_conf = True

        try:
            self.cfg_save_folder_english = data['save_english']
            print(self.cfg_save_folder_english)
        except:
            self.cfg_save_folder_english = ""
            open_conf = True

        try:
            self.cfg_save_folder_deutsch_sub = data['save_deutsch_sub']
            print(self.cfg_save_folder_deutsch_sub)
        except:
            self.cfg_save_folder_deutsch_sub = ""
            open_conf = True

        if open_conf:
            self.config_window = ConfigWindow()
            self.config_window.show()

    @pyqtSlot()
    def textbox_change(self):
        # TODO Save Folder Auto selection

        url = self.textbox_url.text().split("/")

        print(url)
        try:
            if url[2] != "bs.to" and url[2] != "burningseries.co" and url[2] != "burningseries.sx" and url[2] != "burningseries.ac" and url[2] != "burningseries.vc" and url[2] != "burningseries.cx":
                error_dialog = QMessageBox()
                error_dialog.setIcon(QMessageBox.Critical)
                error_dialog.setText("Invalid Website \"" + url[2] + "\". [TODO DOCS]")
                error_dialog.setWindowTitle("Error")
                error_dialog.exec_()
                return
        except:
            error_dialog = QMessageBox()
            error_dialog.setIcon(QMessageBox.Critical)
            error_dialog.setText("This is not a valid URL.")
            error_dialog.setWindowTitle("Error")
            error_dialog.exec_()
            return

        serie = ""
        for elem in url[4].split("-"):
            serie += elem + " "
        serie.strip()

        try:
            staffel = url[5]
            sprache = url[6]
            svfolder = ""
        except:
            error_dialog = QMessageBox()
            error_dialog.setIcon(QMessageBox.Critical)
            error_dialog.setText("Language and season of the series are missing [TODO DOCS].")
            error_dialog.setWindowTitle("Error")
            error_dialog.exec_()
            return

        search_folder = ""

        if sprache == "de":
            # Deutsch
            search_folder = self.cfg_save_folder_deutsch
            cont = True
        elif sprache == "des":
            # Deutsch SUB
            search_folder = self.cfg_save_folder_deutsch_sub
            cont = True
        elif sprache == "en":
            # English
            print("test1")
            search_folder = self.cfg_save_folder_english
            cont = True
            print("test2")
        else:
            error_dialog = QMessageBox()
            error_dialog.setIcon(QMessageBox.Critical)
            error_dialog.setText("Language \"" + sprache + "\" not supported. [TODO DOCS]")
            error_dialog.setWindowTitle("Error")
            error_dialog.exec_()
            return

        try:
            print(int(staffel))
        except:
            error_dialog = QMessageBox()
            error_dialog.setIcon(QMessageBox.Critical)
            error_dialog.setText("Invalid season \"" + staffel + "\". [TODO DOCS]")
            error_dialog.setWindowTitle("Error")
            error_dialog.exec_()
            return

        if cont:
            found = False

            for folder in os.listdir(search_folder):
                #print(folder)

                if str(folder.lower()) == str(serie.lower()):
                    print(str(folder.lower()) + " = " + str(serie.lower()))
                if str(folder.lower()) in str(serie.lower()):
                    print("huh")
                    print(str(folder.lower()) + " in " + str(serie.lower()))
                if str(serie.lower()) in str(folder.lower()):
                    print(str(serie.lower()) + " in " + str(folder.lower()))
                if str(folder.lower()) == str(serie.lower()):
                    print(str(folder.lower()) + " = " + str(serie.lower()))
                if str(folder.lower()) == str(serie.lower()):
                    print(str(folder.lower()) + " = " + str(serie.lower()))
                if str(folder.lower()) == str(serie.lower()):
                    print(str(folder.lower()) + " = " + str(serie.lower()))

                #print(serie)

                if str(folder.lower()) == str(serie.lower()) or str(folder.lower()) in str(serie.lower()) or str(serie.lower()) in str(folder.lower()) or serie.lower().find(str(folder.lower())) != -1 or folder.lower().find(str(serie.lower())) != -1:
                    svfolder = folder
                    for folder2 in os.listdir(os.path.join(search_folder, svfolder)):
                        if str(staffel) in folder2:
                            found = True
                            svfolder = os.path.join(svfolder, folder2)
                            break
                    break


            if found:
                print(svfolder)
                print(serie.lower())
                self.button_save_folder.setText(os.path.join(search_folder, svfolder))
            else:
                print("Not found")



    @pyqtSlot()
    def on_save_folder_click(self):
        print("Save Folder clicked")

        dialog = QFileDialog(self)
        dialog.setWindowTitle('Open Save Folder')
        dialog.setDirectory(self.image_folder)
        dialog.setFileMode(QFileDialog.DirectoryOnly)
        if dialog.exec_() == QDialog.Accepted:
            file_full_path = str(dialog.selectedFiles()[0])
            print(file_full_path)
            self.button_save_folder.setText(file_full_path)
        else:
            return None

    @pyqtSlot()
    def on_config_click(self):
        print("Config clicked")

        self.config_window = ConfigWindow()
        self.config_window.show()

    def on_start_click(self):
        print("Start clicked")

        self.get_config()

        thread = threading.Thread(target=self.start)
        thread.start()

    def start_log(self):
        now = datetime.now()

        if not os.path.isdir('./logs'):
            os.mkdir("./logs")

        self.log = "./logs/log-" + now.strftime("%d-%m-%y %H-%M-%S") + ".txt"

    def write_log(self, message):
        now = datetime.now()

        dt_string = now.strftime("%d/%m/%y %H:%M:%S")
        message = dt_string + " | " + str(message)

        print(message)

        file = open(self.log, "a")
        file.write(message + "\n")
        file.close()

    def threading_dl(self, cmd, THREADING, DLFOLDER):
        if THREADING == "0":
            self.write_log("Starting FFMPEG Download via \"" + str(cmd) + "\"")
            os.system(cmd)
        else:
            loop = True
            while loop:

                self.thread_counter = 0

                for file in os.listdir(DLFOLDER):
                    try:
                        os.rename(os.path.join(DLFOLDER, file), os.path.join(DLFOLDER, file))
                    except:
                        self.thread_counter += 1

                if self.thread_counter < int(THREADING):
                    self.write_log(
                        "----------------------------------Starting Thread----------------------------------")
                    ffmpeg_thread = threading.Thread(target=self.ffmpeg_download, args=(cmd,))
                    ffmpeg_thread.start()
                    self.write_log(
                        "----------------------------------Thread Started----------------------------------")
                    loop = False
                else:
                    self.write_log("Too many threads running. Sleeping 5 Seconds. (" + str(
                        self.thread_counter) + "/" + THREADING + ")")
                    sleep(5)

    def start(self):
        DLFOLDER = self.cfg_dlfolder
        PROFILEFOLDER = self.cfg_profile
        OPERABINEXE = self.cfg_bin
        WEBSITE = self.textbox_url.text()
        SAVEDIR = self.button_save_folder.text()
        FROM = self.textbox_download_from.text()
        TO = self.textbox_download_to.text()
        if self.checkbox_threading.checkState() == 0:
            THREADING = "0"
        else:
            THREADING = str(self.textbox_threading.text())

        if DLFOLDER == "" or DLFOLDER == "Browse...":
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setIcon(QMessageBox.Critical)
            msg.setText("The Opera Download Folder was not specified. Please check your config.")
            x = msg.exec_()
            return
        if PROFILEFOLDER == "" or PROFILEFOLDER == "Browse...":
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setIcon(QMessageBox.Critical)
            msg.setText("The Opera Profile Folder was not specified. Please check your config.")
            x = msg.exec_()
            return
        if OPERABINEXE == "" or OPERABINEXE == "Browse...":
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setIcon(QMessageBox.Critical)
            msg.setText("The Opera Bin exe was not specified. Please check your config.")
            x = msg.exec_()
            return
        website_test = WEBSITE.split("/")
        if WEBSITE == "" or website_test[2] != "bs.to":
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setIcon(QMessageBox.Critical)
            msg.setText("The Website is invalid or was not specified. Please enter a valid url.")
            x = msg.exec_()
            return
        if SAVEDIR == "" or SAVEDIR == "Browse...":
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setIcon(QMessageBox.Critical)
            msg.setText("The Save Direcotry is invalid or was not specified.")
            x = msg.exec_()
            return
        try:
            if FROM != "":
                FROM = int(FROM)
        except:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setIcon(QMessageBox.Critical)
            msg.setText("From is invalid or was not specified.")
            x = msg.exec_()
            return
        try:
            if TO != "":
                TO = int(TO)
        except:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setIcon(QMessageBox.Critical)
            msg.setText("To is invalid or was not specified.")
            x = msg.exec_()
            return

        PREFERRED_PLATFORM = self.combobox_preferred_platform.currentText()
        print(PREFERRED_PLATFORM)

        caps = DesiredCapabilities.OPERA
        caps['goog:loggingPrefs'] = {'performance': 'ALL'}
        options = webdriver.ChromeOptions()
        options.add_argument('user-data-dir=' + PROFILEFOLDER)
        options.add_argument("disable-blink-features=AutomationControlled")
        options._binary_location = OPERABINEXE
        driver = Opera(executable_path='./operadriver.exe', options=options, desired_capabilities=caps)

        driver.get(WEBSITE)

        loop = True
        while loop:
            try:
                table = driver.find_element_by_xpath('//*[@id="root"]/section/table')
                loop = False
            except:
                sleep(1)
                pass

        tr_list = table.find_elements_by_tag_name('tr')

        folgen_array = []

        counter = 1
        for entry in tr_list:
            if not "disabled" in entry.get_attribute("class"):
                if FROM != "":
                    if counter < FROM:
                        counter += 1
                        continue
                if TO != "":
                    if counter > TO:
                        counter += 1
                        continue
                counter += 1
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

                folgen_array.append([folge_link, folge_nbr, folge_name, ""])

        title_list = []
        folge_counter = 0

        for file in os.listdir(DLFOLDER):
            ending = file.rsplit(".")[-1]
            if ending == "opdownload":
                file = file[0:-11]
            if file in title_list:
                continue
            else:
                title_list.append(file)

        for folge in folgen_array:
            driver.get(folge[0])

            str_services_ul = ""
            str_services_ul_2 = ""

            loop = True
            while loop:
                try:
                    str_services_ul = driver.find_element_by_xpath('//*[@id="root"]/section/ul[1]')
                    str_services_ul_2 = driver.find_element_by_xpath('//*[@id="root"]/section/ul[2]')
                    loop = False
                except:
                    pass

            str_services_list = str_services_ul.find_elements_by_tag_name('a')
            str_services_list2 = str_services_ul_2.find_elements_by_tag_name('a')

            counter = 0
            for element in str_services_list:
                str_services_list[counter] = element.text.lower()
                counter += 1

            counter = 0
            for element in str_services_list2:
                str_services_list2[counter] = element.text.lower()
                counter += 1

            found = False
            found2 = False

            counter = 0
            for element in str_services_list:
                if element.lower() == PREFERRED_PLATFORM.lower():
                    found = True
                    counter += 1
                    break
                counter += 1

            if not found:
                counter = 0
                for element in str_services_list2:
                    if element.lower() == PREFERRED_PLATFORM.lower():
                        found2 = True
                        counter += 1
                        break
                    counter += 1

            if not found and not found2:
                counter = 1

            if found and counter != 1:
                driver.find_element_by_xpath('//*[@id="root"]/section/ul[1]/li[' + str(counter) + ']/a').click()

            if found2:
                driver.find_element_by_xpath('//*[@id="root"]/section/ul[2]/li[' + str(counter) + ']/a').click()

            loop = True
            while loop:
                try:
                    driver.find_element_by_xpath('//*[@id="root"]/section/div[8]/div[1]').click()
                    loop = False
                except:
                    pass

            loop = True
            msg_send = False
            sleep(1)
            while loop:
                try:
                    vscheck = driver.find_element_by_xpath("/html/body/div[4]")
                    if "visible" in vscheck.get_attribute("style"):
                        if not msg_send:
                            self.write_log("INFO: Captcha found, Human needed O.O")
                            msg_send = True
                    else:
                        self.write_log("INFO: Captcha solved. Good job Human :)")
                        loop = False
                except:
                    pass

            video_mode = driver.find_element_by_xpath('//*[@id="root"]/section/ul[1]/li[' + str(counter) + ']/a').text.lower()

            dnl_link = ""

            filecounter = 0
            for file in os.listdir(DLFOLDER):
                filecounter += 1

            if video_mode == "vivo":
                loop = True
                while loop:
                    try:
                        driver.get(
                            driver.find_element_by_xpath('//*[@id="root"]/section/div[8]/a').get_attribute('href'))
                        loop = False
                    except:
                        pass
                dnl_link = driver.find_element_by_tag_name('source').get_attribute('src')
                # driver.get(dnl_link)

                ffmpeg = self.cfg_ffmpeg
                cmd = ffmpeg + " -i \"" + dnl_link + "\" -vcodec copy -acodec copy \"" + os.path.join(DLFOLDER, str(
                    folgen_array[folge_counter][1]) + ".mp4\"")

                self.threading_dl(cmd, THREADING, DLFOLDER)

            elif video_mode == "streamtape":
                loop = True
                while loop:
                    try:
                        driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="root"]/section/div[8]/iframe'))
                        loop = False
                    except:
                        pass
                loop = True
                sleep(1)
                while loop:
                    try:
                        driver.find_element_by_xpath('/html/body/div[2]/div[1]').click()
                    except:
                        loop = False
                loop = True
                while loop:
                    try:
                        driver.find_element_by_xpath('/html/body/div[2]/div[2]/button').click()
                        loop = False
                    except:
                        pass
                driver.find_element_by_xpath('//*[@id="mainvideo"]').click()
                dnl_link = driver.find_element_by_xpath('//*[@id="mainvideo"]').get_attribute('src')
                driver.switch_to.default_content()
                # driver.get(dnl_link)

                ffmpeg = self.cfg_ffmpeg
                cmd = ffmpeg + " -i \"" + dnl_link + "\" -vcodec copy -acodec copy \"" + os.path.join(DLFOLDER, str(
                    folgen_array[folge_counter][1]) + ".mp4\"")

                self.threading_dl(cmd, THREADING, DLFOLDER)

            elif video_mode == "vidoza":
                loop = True
                while loop:
                    try:
                        driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="root"]/section/div[8]/iframe'))
                        loop = False
                    except:
                        pass
                loop = True
                while loop:
                    try:
                        driver.find_element_by_xpath('//*[@id="vplayer"]/div[1]').click()
                        loop = False
                    except:
                        pass
                loop = True
                while loop:
                    try:
                        driver.find_element_by_xpath('//*[@id="player"]/button').click()
                        loop = False
                    except:
                        pass
                loop = True
                while loop:
                    try:
                        dnl_link = driver.find_element_by_xpath('//*[@id="player_html5_api"]').get_attribute('src')
                        loop = False
                    except:
                        pass
                driver.switch_to.default_content()
                # driver.get(dnl_link)

                ffmpeg = self.cfg_ffmpeg
                cmd = ffmpeg + " -i \"" + dnl_link + "\" -vcodec copy -acodec copy \"" + os.path.join(DLFOLDER, str(
                    folgen_array[folge_counter][1]) + ".mp4\"")

                self.threading_dl(cmd, THREADING, DLFOLDER)
            elif video_mode == "vupload":
                loop = True
                while loop:
                    try:
                        test_link = driver.find_element_by_xpath('//*[@id="root"]/section/div[8]/a').get_attribute('href')
                        driver.get(test_link)
                        loop = False
                    except:
                        pass
                # Try Set to 720p
                loop = True
                while loop:
                    try:
                        sleep(1)
                        driver.find_element_by_xpath('//*[@id="vjsplayer"]/div[6]/div[3]/div[7]/button').click() # Click Settings
                        sleep(0.1)
                        driver.find_element_by_xpath('//*[@id="vjsplayer"]/div[7]/ul/li[4]').click() # Click Quality List Item
                        sleep(0.1)
                        qualities = driver.find_element_by_xpath('//*[@id="vjsplayer"]/div[7]/ul').find_elements_by_tag_name('li') # Quality Settings
                        sleep(0.1)
                        qualities[-1].click() # Click highest quality
                        loop = False
                    except:
                        pass
                loop = True
                while loop:
                    try:
                        dnl_link = driver.find_element_by_xpath('//*[@id="vjsplayer_html5_api"]').get_attribute('src')
                        loop = False
                    except:
                        pass
                # driver.get(dnl_link)

                ffmpeg = self.cfg_ffmpeg
                cmd = ffmpeg + " -i \"" + dnl_link + "\" -vcodec copy -acodec copy \"" + os.path.join(DLFOLDER, str(
                    folgen_array[folge_counter][1]) + ".mp4\"")

                self.threading_dl(cmd, THREADING, DLFOLDER)

            print("done")

            filecounter_new = filecounter
            while filecounter >= filecounter_new:
                filecounter_new = 0
                for file in os.listdir(DLFOLDER):
                    filecounter_new += 1

            self.write_log("INFO: New File found.")

            sleep(1)

            for file in os.listdir(DLFOLDER):
                ending = file.rsplit(".")[-1]
                if ending == "opdownload":
                    file = file[0:-11]
                if file in title_list:
                    continue
                else:
                    title_list.append(file)
                    folgen_array[folge_counter][3] = file

            folge_counter += 1

            for file in os.listdir(DLFOLDER):
                ending = file.rsplit(".")[-1]
                if ending == "opdownload":
                    continue
                elif ending == "mp4":
                    folgen_arr_counter = 0
                    for folge in folgen_array:
                        if folge[3] == file:
                            try:
                                os.rename(os.path.join(DLFOLDER, file),
                                          os.path.join(DLFOLDER, folge[1] + ".mp4"))
                                self.write_log("INFO: Renamed \"" + file + "\" to \"" + folge[1] + "\"")
                                folgen_array[folgen_arr_counter][3] = folge[1] + ".mp4"
                                tl_counter = 0
                                for dings in title_list:
                                    if dings == file:
                                        title_list[tl_counter] = folge[1] + ".mp4"
                                        break
                                    tl_counter += 1
                                break
                            except:
                                pass
                        folgen_arr_counter += 1

            self.write_log("INFO: List of series: ")
            self.write_log(folgen_array)
            self.write_log("INFO: List of downloaded series: ")
            self.write_log(title_list)

        downloading = True
        meldung = False
        while downloading:
            downloading = False
            for file in os.listdir(DLFOLDER):
                if file.rsplit(".")[-1] == "opdownload":
                    downloading = True
                else:
                    try:
                        os.rename(os.path.join(DLFOLDER, file), os.path.join(DLFOLDER, file))
                    except:
                        downloading = True
            if downloading:
                if not meldung:
                    self.write_log(
                        "WARNING: At least one file is still downloading, The Program will wait before moving the files...")
                    meldung = True

        sleep(1)

        for file in os.listdir(DLFOLDER):
            ending = file.rsplit(".")[-1]
            if ending == "opdownload":
                continue
            elif ending == "mp4":
                folgen_arr_counter = 0
                for folge in folgen_array:
                    if folge[3] == file:
                        os.rename(os.path.join(DLFOLDER, file),
                                  os.path.join(DLFOLDER, folge[1] + ".mp4"))
                        self.write_log("INFO: Renamed \"" + file + "\" to \"" + folge[1] + "\"")
                        folgen_array[folgen_arr_counter][3] = folge[1] + ".mp4"
                        tl_counter = 0
                        for dings in title_list:
                            if dings == file:
                                title_list[tl_counter] = folge[1] + ".mp4"
                                break
                            tl_counter += 1
                        break
                    folgen_arr_counter += 1

        sleep(1)

        self.write_log("INFO: Moving files to the destination.")

        for file in os.listdir(DLFOLDER):
            for folge in folgen_array:
                if folge[3] == file:
                    # new_name = folge[1] + "_" + folge[2] + ".mp4"
                    new_name = folge[1].split(".")
                    new_name = int(new_name[0])
                    new_name = str(new_name) + ".mp4"
                    os.rename(os.path.join(DLFOLDER, file), os.path.join(DLFOLDER, new_name))
                    self.write_log("INFO: Renamed \"" + file + "\" to \"" + new_name + "\"")

        for file in os.listdir(DLFOLDER):
            shutil.move(os.path.join(DLFOLDER, file), os.path.join(SAVEDIR, file))

        driver.quit()

        self.write_log("INFO: Successfully moved all files. Scraping Finished.")


        msg = QMessageBox()
        msg.setWindowTitle("Info")
        msg.setIcon(QMessageBox.Information)
        msg.setText("Successfully moved all files. Scraping Finished..")
        x = msg.exec_()

    def ffmpeg_download(self, cmd):
        self.write_log("Starting FFMPEG Download via \"" + str(cmd) + "\"")
        os.system(cmd)


class ConfigWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.config_grid_layout = QGridLayout()
        self.setWindowTitle("Config")
        self.setLayout(self.config_grid_layout)

        # Opera Download

        try:
            with open('config.json') as json_file:
                data = json.load(json_file)
        except:
            pass

        try:
            self.cfg_dlfolder = data['dlfolder']
            print(self.cfg_dlfolder)
        except:
            self.cfg_dlfolder = ""

        try:
            self.cfg_profile = data['profile']
            print(self.cfg_profile)
        except:
            self.cfg_profile = ""

        try:
            self.cfg_bin = data['bin']
            print(self.cfg_bin)
        except:
            self.cfg_bin = ""
            pass

        try:
            self.cfg_ffmpeg = data['ffmpeg']
            print(self.cfg_ffmpeg)
        except:
            self.cfg_ffmpeg = ""
            pass

        try:
            self.cfg_save_folder_deutsch = data['save_deutsch']
            print(self.cfg_save_folder_deutsch)
        except:
            self.cfg_save_folder_deutsch = ""
            pass

        try:
            self.cfg_save_folder_english = data['save_english']
            print(self.cfg_save_folder_english)
        except:
            self.cfg_save_folder_english = ""
            pass

        try:
            self.cfg_save_folder_deutsch_sub = data['save_deutsch_sub']
            print(self.cfg_save_folder_deutsch_sub)
        except:
            self.cfg_save_folder_deutsch_sub = ""
            pass

        self.label_opera_download_folder = QLabel(self)
        self.label_opera_download_folder.setText("Opera Download Folder: ")
        self.config_grid_layout.addWidget(self.label_opera_download_folder, 0, 0)

        self.button_opera_download_folder = QPushButton(self)
        if self.cfg_dlfolder != "":
            self.button_opera_download_folder.setText(self.cfg_dlfolder)
        else:
            self.button_opera_download_folder.setText("Browse...")
            self.cfg_dlfolder = ""
            self.button_opera_download_folder.setStyleSheet('QPushButton {color: red;}')
        self.button_opera_download_folder.setToolTip("The Folder Opera Downloads it's files to.")
        self.config_grid_layout.addWidget(self.button_opera_download_folder, 0, 1)

        self.button_opera_download_folder.clicked.connect(self.button_opera_download_folder_clicked)

        # Opera Profile

        self.label_opera_profile_folder = QLabel(self)
        self.label_opera_profile_folder.setText("Opera Profile Folder: ")
        self.config_grid_layout.addWidget(self.label_opera_profile_folder, 1, 0)

        self.button_opera_profile_folder = QPushButton(self)
        if self.cfg_profile != "":
            self.button_opera_profile_folder.setText(self.cfg_profile)
        else:
            tmp_path = os.path.join(os.getenv('APPDATA'), "Opera Software\\Opera Stable")
            if os.path.exists(tmp_path):
                self.button_opera_profile_folder.setText(tmp_path)
                self.cfg_profile = tmp_path
            else:
                self.button_opera_profile_folder.setText(os.getenv('APPDATA'))
                self.cfg_profile = os.getenv('APPDATA')
                self.button_opera_profile_folder.setStyleSheet('QPushButton {color: red;}')
        self.button_opera_profile_folder.setToolTip("The Folder to your Opera Profile.")
        self.config_grid_layout.addWidget(self.button_opera_profile_folder, 1, 1)

        self.button_opera_profile_folder.clicked.connect(self.button_opera_profile_folder_clicked)

        # Opera Bin Exe

        self.label_opera_bin_exe = QLabel(self)
        self.label_opera_bin_exe.setText("Opera Bin Exe: ")
        self.config_grid_layout.addWidget(self.label_opera_bin_exe, 2, 0)

        self.button_opera_bin_exe = QPushButton(self)
        if self.cfg_bin != "":
            self.button_opera_bin_exe.setText(self.cfg_bin)
        else:
            tmp_path = os.path.join(os.getenv('LOCALAPPDATA'), "Programs\\Opera")
            if os.path.exists(tmp_path):
                highest = 0
                tmp_dir = ""
                for file in os.listdir(tmp_path):
                    if os.path.isdir(os.path.join(tmp_path, file)):
                        if file[0].isdigit():
                            print(file)
                            tmp_nbr = file.replace(".", "")
                            if int(tmp_nbr) > highest:
                                tmp_dir = os.path.join(tmp_path, file)
                self.button_opera_bin_exe.setText(os.path.join(tmp_dir, "opera.exe"))
                self.cfg_bin = os.path.join(tmp_dir, "opera.exe")
            else:
                self.button_opera_bin_exe.setText(os.getenv('LOCALAPPDATA'))
                self.cfg_bin = os.getenv('LOCALAPPDATA')
                self.button_opera_bin_exe.setStyleSheet('QPushButton {color: red;}')
        self.button_opera_bin_exe.setToolTip("The Folder to your opera binary .exe file.")
        self.config_grid_layout.addWidget(self.button_opera_bin_exe, 2, 1)

        self.button_opera_bin_exe.clicked.connect(self.button_opera_bin_exe_clicked)

        # FFMPEG

        self.label_ffmpeg = QLabel(self)
        self.label_ffmpeg.setText("FFMPEG: ")
        self.config_grid_layout.addWidget(self.label_ffmpeg, 3, 0)

        self.button_ffmpeg = QPushButton(self)
        self.button_ffmpeg.setText(self.cfg_ffmpeg)
        self.button_ffmpeg.setToolTip("The Path to your FFMPEG.exe.")
        self.config_grid_layout.addWidget(self.button_ffmpeg, 3, 1)
        self.button_ffmpeg.clicked.connect(self.button_ffmpeg_clicked)

        # Save Folder Deutsch

        self.label_save_folder_deutsch = QLabel(self)
        self.label_save_folder_deutsch.setText("Save Folder Deutsch: ")
        self.config_grid_layout.addWidget(self.label_save_folder_deutsch, 4, 0)

        self.button_save_folder_deutsch = QPushButton(self)
        self.button_save_folder_deutsch.setText(self.cfg_save_folder_deutsch)
        self.button_save_folder_deutsch.setToolTip("The Path to your German Series.")
        self.config_grid_layout.addWidget(self.button_save_folder_deutsch, 4, 1)
        self.button_save_folder_deutsch.clicked.connect(self.button_save_folder_deutsch_clicked)

        # Save Folder Deutsch SUB

        self.label_save_folder_deutsch_sub = QLabel(self)
        self.label_save_folder_deutsch_sub.setText("Save Folder Deutsch-SUB: ")
        self.config_grid_layout.addWidget(self.label_save_folder_deutsch_sub, 5, 0)

        self.button_save_folder_deutsch_sub = QPushButton(self)
        self.button_save_folder_deutsch_sub.setText(self.cfg_save_folder_deutsch_sub)
        self.button_save_folder_deutsch_sub.setToolTip("The Path to your German-SUB Series.")
        self.config_grid_layout.addWidget(self.button_save_folder_deutsch_sub, 5, 1)
        self.button_save_folder_deutsch_sub.clicked.connect(self.button_save_folder_deutsch_sub_clicked)

        # Save Folder English

        self.label_save_folder_english = QLabel(self)
        self.label_save_folder_english.setText("Save Folder English: ")
        self.config_grid_layout.addWidget(self.label_save_folder_english, 6, 0)

        self.button_save_folder_english = QPushButton(self)
        self.button_save_folder_english.setText(self.cfg_save_folder_english)
        self.button_save_folder_english.setToolTip("The Path to your English Series.")
        self.config_grid_layout.addWidget(self.button_save_folder_english, 6, 1)
        self.button_save_folder_english.clicked.connect(self.button_save_folder_english_clicked)

        data = {}

        if os.path.exists(self.cfg_dlfolder):
            data['dlfolder'] = self.cfg_dlfolder
        if os.path.exists(self.cfg_profile):
            data['profile'] = self.cfg_profile
        if os.path.exists(self.cfg_bin):
            data['bin'] = self.cfg_bin
        if os.path.exists(self.cfg_ffmpeg):
            data['ffmpeg'] = self.cfg_ffmpeg
        if os.path.exists(self.cfg_save_folder_deutsch):
            data['save_deutsch'] = self.cfg_save_folder_deutsch
        if os.path.exists(self.cfg_save_folder_deutsch_sub):
            data['save_deutsch_sub'] = self.cfg_save_folder_deutsch_sub
        if os.path.exists(self.cfg_save_folder_english):
            data['save_english'] = self.cfg_save_folder_english

        with open('config.json', 'w') as outfile:
            json.dump(data, outfile)

    @pyqtSlot()
    def button_opera_download_folder_clicked(self):
        print("Opera Download Folder Clicked")

        dialog = QFileDialog(self)
        dialog.setWindowTitle('Open Opera Download Folder')
        dialog.setDirectory(os.getenv('USERPROFILE'))
        dialog.setFileMode(QFileDialog.DirectoryOnly)
        if dialog.exec_() == QDialog.Accepted:
            file_full_path = str(dialog.selectedFiles()[0])
            file_full_path = file_full_path.replace("/", "\\")
            print(file_full_path)
            self.button_opera_download_folder.setText(file_full_path)

            try:
                with open('config.json') as json_file:
                    data = json.load(json_file)

                data['dlfolder'] = file_full_path

                with open('config.json', 'w') as outfile:
                    json.dump(data, outfile)
            except:
                pass
        else:
            return None

    @pyqtSlot()
    def button_opera_profile_folder_clicked(self):
        print("Opera Profile Folder Clicked")

        dialog = QFileDialog(self)
        dialog.setWindowTitle('Open Opera Profile Folder')
        dialog.setDirectory(os.getenv('APPDATA'))
        dialog.setFileMode(QFileDialog.DirectoryOnly)
        if dialog.exec_() == QDialog.Accepted:
            file_full_path = str(dialog.selectedFiles()[0])
            file_full_path = file_full_path.replace("/", "\\")
            print(file_full_path)
            self.button_opera_profile_folder.setText(file_full_path)

            try:
                with open('config.json') as json_file:
                    data = json.load(json_file)

                data['profile'] = file_full_path

                with open('config.json', 'w') as outfile:
                    json.dump(data, outfile)
            except:
                pass
        else:
            return None

    @pyqtSlot()
    def button_ffmpeg_clicked(self):
        print("FFMPEG Clicked")

        dialog = QFileDialog(self)
        dialog.setWindowTitle('Open FFMPEG .exe')
        dialog.setNameFilter('exe files (*.exe;)')
        dialog.setDirectory(os.getenv('LOCALAPPDATA'))
        dialog.setFileMode(QFileDialog.ExistingFile)
        if dialog.exec_() == QDialog.Accepted:
            file_full_path = str(dialog.selectedFiles()[0])
            file_full_path = file_full_path.replace("/", "\\")
            print(file_full_path)
            self.button_ffmpeg.setText(file_full_path)

            try:
                with open('config.json') as json_file:
                    data = json.load(json_file)

                data['ffmpeg'] = file_full_path

                with open('config.json', 'w') as outfile:
                    json.dump(data, outfile)
            except:
                pass
        else:
            return None

    @pyqtSlot()
    def button_save_folder_deutsch_clicked(self):
        print("Opera Save Folder Deutsch Clicked")

        dialog = QFileDialog(self)
        dialog.setWindowTitle('Open Save Folder Deutsch')
        dialog.setFileMode(QFileDialog.DirectoryOnly)
        if dialog.exec_() == QDialog.Accepted:
            file_full_path = str(dialog.selectedFiles()[0])
            file_full_path = file_full_path.replace("/", "\\")
            print(file_full_path)
            self.button_save_folder_deutsch.setText(file_full_path)

            try:
                with open('config.json') as json_file:
                    data = json.load(json_file)

                data['save_deutsch'] = file_full_path

                with open('config.json', 'w') as outfile:
                    json.dump(data, outfile)
            except:
                pass
        else:
            return None

    @pyqtSlot()
    def button_save_folder_deutsch_sub_clicked(self):
        print("Opera Save Folder Deutsch SUB Clicked")

        dialog = QFileDialog(self)
        dialog.setWindowTitle('Open Save Folder Deutsch SUB')
        dialog.setFileMode(QFileDialog.DirectoryOnly)
        if dialog.exec_() == QDialog.Accepted:
            file_full_path = str(dialog.selectedFiles()[0])
            file_full_path = file_full_path.replace("/", "\\")
            print(file_full_path)
            self.button_save_folder_deutsch_sub.setText(file_full_path)

            try:
                with open('config.json') as json_file:
                    data = json.load(json_file)

                data['save_deutsch_sub'] = file_full_path

                with open('config.json', 'w') as outfile:
                    json.dump(data, outfile)
            except:
                pass
        else:
            return None

    def button_save_folder_english_clicked(self):
        print("Opera Save Folder English Clicked")

        dialog = QFileDialog(self)
        dialog.setWindowTitle('Open Save Folder English')
        dialog.setFileMode(QFileDialog.DirectoryOnly)
        if dialog.exec_() == QDialog.Accepted:
            file_full_path = str(dialog.selectedFiles()[0])
            file_full_path = file_full_path.replace("/", "\\")
            print(file_full_path)
            self.button_save_folder_english.setText(file_full_path)

            try:
                with open('config.json') as json_file:
                    data = json.load(json_file)

                data['save_english'] = file_full_path

                with open('config.json', 'w') as outfile:
                    json.dump(data, outfile)
            except:
                pass
        else:
            return None

    @pyqtSlot()
    def button_opera_bin_exe_clicked(self):
        print("Opera Bin Exe Clicked")

        dialog = QFileDialog(self)
        dialog.setWindowTitle('Open Opera Bin .exe')
        dialog.setNameFilter('exe files (*.exe;)')
        dialog.setDirectory(os.getenv('LOCALAPPDATA'))
        dialog.setFileMode(QFileDialog.ExistingFile)
        if dialog.exec_() == QDialog.Accepted:
            file_full_path = str(dialog.selectedFiles()[0])
            file_full_path = file_full_path.replace("/", "\\")
            print(file_full_path)
            self.button_opera_bin_exe.setText(file_full_path)

            try:
                with open('config.json') as json_file:
                    data = json.load(json_file)

                data['bin'] = file_full_path

                with open('config.json', 'w') as outfile:
                    json.dump(data, outfile)
            except:
                pass
        else:
            return None


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
