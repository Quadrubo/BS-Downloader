import threading
from tkinter import *
import json
from pathlib import Path
from tkinter import filedialog
from selenium import webdriver
from seleniumrequests import Opera
from time import sleep
import os
import shutil


class Win1:
    def __init__(self, master):
        self.master = master

        self.set_geo()
        self.show_widgets()
        self.get_config()

    def set_geo(self):
        self.master.geometry("425x321")
        self.master.resizable(0, 0)

    def get_config(self):
        my_file = Path("./config.json")
        if my_file.is_file():
            print("INFO: Config File found.")
            # file exists

            with open("config.json") as json_data_file:

                try:
                    data = json.load(json_data_file)
                    self.dlfolder = data['dlfolder']
                    self.profilefolder = data['profile']
                    self.binfile = data['bin']

                    self.counter = 0
                    for file in os.listdir(self.dlfolder):
                        self.counter += 1

                    self.entry_already_var.set(self.counter)
                except:
                    print("ERROR: Invalid Config File. Please create a new one with the Program.")
                    self.new_window(Win2)



        else:
            print("WARNING: No Config File found.")

            self.new_window(Win2)

    def browse_savefolder(self):
        self.save_folder = filedialog.askdirectory()
        self.button_save_var.set(self.save_folder)
        print("INFO: Save Folder selected: " + self.save_folder)

    def show_widgets(self):
        self.frame = Frame(self.master)
        self.frame.grid(row=0, column=0)

        self.frame2 = Frame(self.master)
        self.frame2.grid(row=1, column=0)

        self.master.title("BS Downloader GUI v2.3.2")

        self.label_url = Label(self.frame, text="BS Url: ")
        self.label_url.grid(row=0, column=0)

        self.entry_url = Entry(self.frame, width=50)
        self.entry_url.grid(row=0, column=1, sticky=W)

        self.label_save = Label(self.frame, text="Save Folder: ")
        self.label_save.grid(row=1, column=0)

        self.button_save_var = StringVar()
        self.button_save = Button(self.frame, textvariable=self.button_save_var, command=self.browse_savefolder, width=42)
        self.button_save.grid(row=1, column=1, sticky=W)
        self.button_save_var.set("Browse...")

        self.button_already = Button(self.frame, text="Existing Downloads: ", command=self.open_dir)
        self.button_already.grid(row=2, column=0)

        self.entry_already_var = StringVar()
        self.entry_already = Entry(self.frame, textvariable=self.entry_already_var, width=10, justify="center")
        self.entry_already.grid(row=2, column=1, sticky=W)

        self.label_max = Label(self.frame, text="Limit: ")
        self.label_max.grid(row=3, column=0)

        self.entry_max_var = StringVar()
        self.entry_max = Entry(self.frame, textvariable=self.entry_max_var, width=10, justify="center")
        self.entry_max.grid(row=3, column=1, sticky=W)
        self.entry_max_var.set(0)

        self.label_pref = Label(self.frame, text="Preferred Platform: ")
        self.label_pref.grid(row=4, column=0)

        self.radio_pref_var = StringVar()

        self.radio_pref_vivo = Radiobutton(self.frame, text="vivo", variable=self.radio_pref_var, value="vivo")
        self.radio_pref_vivo.grid(row=4, column=1, sticky=W)
        self.radio_pref_streamtape = Radiobutton(self.frame, text="streamtape", variable=self.radio_pref_var, value="streamtape")
        self.radio_pref_streamtape.grid(row=5, column=1, sticky=W)
        self.radio_pref_voe = Radiobutton(self.frame, text="voe", variable=self.radio_pref_var, value="voe")
        self.radio_pref_voe.grid(row=6, column=1, sticky=W)
        self.radio_pref_vidoza = Radiobutton(self.frame, text="vidoza", variable=self.radio_pref_var, value="vidoza")
        self.radio_pref_vidoza.grid(row=7, column=1, sticky=W)
        self.radio_pref_mixdrop = Radiobutton(self.frame, text="mixdrop", variable=self.radio_pref_var, value="mixdrop")
        self.radio_pref_mixdrop.grid(row=8, column=1, sticky=W)
        self.radio_pref_playtube = Radiobutton(self.frame, text="playtube", variable=self.radio_pref_var, value="playtube")
        self.radio_pref_playtube.grid(row=9, column=1, sticky=W)
        self.radio_pref_upstream = Radiobutton(self.frame, text="upstream", variable=self.radio_pref_var, value="upstream")
        self.radio_pref_upstream.grid(row=10, column=1, sticky=W)
        self.radio_pref_vidlox = Radiobutton(self.frame, text="vidlox", variable=self.radio_pref_var, value="vidlox")
        self.radio_pref_vidlox.grid(row=11, column=1, sticky=W)
        self.radio_pref_vivo.select()

        self.button_start_var = StringVar()
        self.button_start = Button(self.frame, textvariable=self.button_start_var, command=self.start, width=42,bg="lightgreen")
        self.button_start.grid(row=12, column=1)
        self.button_start_var.set("Start!")

        self.button1 = Button(self.frame, text="Config", command=lambda: self.new_window(Win2), bg="orange")
        self.button1.grid(row=12, column=0)

    def open_dir(self):
        os.system("start " + self.dlfolder)

    def start(self):
        print("INFO: Starting the Webscraper...")

        execute = True

        # The profile where I enabled the VPN previously using the GUI.
        OPERA_DLFOLDER = self.dlfolder
        if OPERA_DLFOLDER == "" or OPERA_DLFOLDER == "Browse...":
            print("ERROR: Opera Download Folder was not specified: " + OPERA_DLFOLDER)
            execute = False
        else:
            print("INFO: Opera Download Folder: " + OPERA_DLFOLDER)
        OPERA_PROFILE = self.profilefolder
        if OPERA_PROFILE == "" or OPERA_PROFILE == "Browse...":
            print("ERROR: Opera Profile Folder was not specified: " + OPERA_PROFILE)
            execute = False
        else:
            print("INFO: Opera Profile Folder: " + OPERA_PROFILE)
        OPERA_BIN = self.binfile
        if OPERA_BIN == "" or OPERA_BIN == "Browse...":
            print("ERROR: Opera Binary EXE File was not specified: " + OPERA_BIN)
            execute = False
        else:
            print("INFO: Opera Binary EXE File: " + OPERA_BIN)
        website = self.entry_url.get()
        if website == "":
            print("ERROR: Website was not specified: " + website)
            execute = False
        else:
            print("INFO: Website: " + website)
        save_dir = self.button_save_var.get()
        if save_dir == "" or save_dir == "Browse...":
            print("ERROR: Save Folder was not specified: " + save_dir)
            execute = False
        else:
            print("INFO: Save Folder: " + OPERA_BIN)
        already_exist = self.entry_already_var.get()
        try:
            already_exist = int(self.entry_already_var.get())
        except:
            pass
        if already_exist == "":
            print("ERROR: It's not specified, how many files already exist: " + str(already_exist))
            execute = False
        elif type(already_exist) is not int:
            print("ERROR: You didn't enter a number: " + str(already_exist))
            execute = False
        else:
            print("INFO: Files that already exist: " + str(already_exist))
        try:
            maximum = int(self.entry_max_var.get())
        except:
            maximum = self.entry_max_var.get()
            pass
        if type(maximum) is not int:
            print("ERROR: You didn't enter a number: " + str(maximum))
            execute = False
        else:
            print("INFO: Limit: " + str(maximum))

        preferred_website = self.radio_pref_var.get()

        if execute:
            opera_profile = OPERA_PROFILE
            options = webdriver.ChromeOptions()
            options.add_argument('user-data-dir=' + opera_profile)
            options.add_argument("disable-blink-features=AutomationControlled")
            options._binary_location = OPERA_BIN
            driver = Opera(executable_path='./operadriver.exe', options=options)

            driver.get(website)

            loop = True
            while loop:
                try:
                    table = driver.find_element_by_xpath('//*[@id="root"]/section/table')
                    loop = False
                except:
                    pass

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

            title_list = []

            if maximum != 0:
                folgen_arr_temp = folgen_arr.copy()

                folgen_arr = []

                for i in range(0, maximum):
                    folgen_arr.append(folgen_arr_temp[i])

            folge_gesamt = 0
            for folge in folgen_arr:
                folge_gesamt += 1

            folge_counter = 0

            for folge in folgen_arr:
                if folge_counter < already_exist:
                    for file in os.listdir(OPERA_DLFOLDER):
                        if file in title_list:
                            continue
                        else:
                            folgen_arr[folge_counter][3] = file
                            title_list.append(file)
                            break
                    folge_counter += 1
                    continue

                driver.get(folge[0])

                str_services_ul = ""

                loop = True
                while loop:
                    try:
                        str_services_ul = driver.find_element_by_xpath('//*[@id="root"]/section/ul[1]')
                        loop = False
                    except:
                        pass

                str_services_list = str_services_ul.find_elements_by_tag_name('a')

                counter = 0
                for element in str_services_list:
                    str_services_list[counter] = element.text.lower()
                    counter += 1

                found = False

                counter = 0
                for element in str_services_list:
                    print(element.lower())
                    print(preferred_website)
                    if element.lower() == preferred_website:
                        found = True
                        counter += 1
                        break
                    counter += 1

                if found and counter != 1:
                    driver.find_element_by_xpath('//*[@id="root"]/section/ul[1]/li[' + str(counter) + ']/a').click()


                loop = True
                while loop:
                    try:
                        driver.find_element_by_xpath('//*[@id="root"]/section/div[8]/div[1]').click()
                        loop = False
                    except:
                        pass

                loop = True
                msg_send = False
                while loop:
                    try:
                        vscheck = driver.find_element_by_xpath("/html/body/div[4]")
                        if "visible" in vscheck.get_attribute("style"):
                            if not msg_send:
                                print("INFO: Captcha found, Human needed O.O")
                                msg_send = True
                        else:
                            print("INFO: Captcha solved. Good job Human :)")
                            loop = False
                    except:
                        pass

                video_mode = driver.find_element_by_xpath('//*[@id="root"]/section/ul[1]/li[1]/a').text.lower()

                print("\"" + video_mode + "\"")

                dnl_link = ""

                if video_mode == "vivo":
                    loop = True
                    while loop:
                        try:
                            driver.get(driver.find_element_by_xpath('//*[@id="root"]/section/div[8]/a').get_attribute('href'))
                            loop = False
                        except:
                            pass
                    dnl_link = driver.find_element_by_tag_name('source').get_attribute('src')
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

                filecounter = 0
                for file in os.listdir(OPERA_DLFOLDER):
                    filecounter += 1

                driver.get(dnl_link)

                filecounter_new = filecounter
                while filecounter >= filecounter_new:
                    filecounter_new = 0
                    for file in os.listdir(OPERA_DLFOLDER):
                        filecounter_new += 1

                print("INFO: New File found.")

                sleep(1)

                for file in os.listdir(OPERA_DLFOLDER):
                    ending = file.rsplit(".")[-1]
                    if ending == "opdownload":
                        file = file[0:-11]
                    if file in title_list:
                        continue
                    else:
                        folgen_arr[folge_counter][3] = file
                        title_list.append(file)
                        break

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
                                for dings in title_list:
                                    if dings == file:
                                        title_list[tl_counter] = folge[1] + ".mp4"
                                        break
                                    tl_counter += 1
                                break
                            folgen_arr_counter += 1

                print("INFO: List of series: ")
                print(folgen_arr)
                print("INFO: List of downloaded series: ")
                print(title_list)

            downloading = True
            meldung = False
            while downloading:
                downloading = False
                for file in os.listdir(OPERA_DLFOLDER):
                    if file.rsplit(".")[-1] == "opdownload":
                        downloading = True
                if downloading:
                    if not meldung:
                        print("WARNING: At least one file is still downloading, The Program will wait before moving the files...")
                        meldung = True

            sleep(1)

            for file in os.listdir(OPERA_DLFOLDER):
                ending = file.rsplit(".")[-1]
                if ending == "opdownload":
                    continue
                elif ending == "mp4":
                    folgen_arr_counter = 0
                    for folge in folgen_arr:
                        if folge[3] == file:
                            os.rename(os.path.join(OPERA_DLFOLDER, file),
                                      os.path.join(OPERA_DLFOLDER, folge[1] + ".mp4"))
                            folgen_arr[folgen_arr_counter][3] = folge[1] + ".mp4"
                            tl_counter = 0
                            for dings in title_list:
                                if dings == file:
                                    title_list[tl_counter] = folge[1] + ".mp4"
                                    break
                                tl_counter += 1
                            break
                        folgen_arr_counter += 1

            sleep(1)

            print("INFO: Moving files to the destination.")

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

            print("INFO: Successfully moved all files. Scraping Finished.")
            self.button_start_var.set("Success!")
        else:
            self.button_start_var.set("Something's wrong I can feel it!")

    def solve_captcha(self):
        pass

    def new_window(self, _class):
        self.win = Toplevel(self.master)
        _class(self.win)

    def close_window(self):
        self.master.destroy()


class Win2(Win1):

    def set_geo(self):
        self.master.geometry("638x105")
        self.master.resizable(0, 0)
        self.master.grab_set()

    def get_config(self):
        my_file = Path("./config.json")
        if my_file.is_file():
            print("INFO: Config File found.")
            # file exists

            try:
                with open("config.json") as json_data_file:

                    data = json.load(json_data_file)

                    self.dlfolder = data['dlfolder']
                    self.profilefolder = data['profile']
                    self.binfile = data['bin']

                    self.button1_save_var.set(self.dlfolder)
                    self.button2_save_var.set(self.profilefolder)
                    self.button3_save_var.set(self.binfile)
            except:
                print("ERROR: Invalid Config File. Please create a new one with the Program.")

    def save_config(self):
        data = {
            "dlfolder": self.dlfolder,
            "profile": self.profilefolder,
            "bin": self.binfile
        }

        with open("config.json", "w") as outfile:
            json.dump(data, outfile)

        self.master.destroy()

    def browse_dlfolder(self):
        self.dlfolder = filedialog.askdirectory()
        self.button1_save_var.set(self.dlfolder)
        print("INFO: Opera Download Folder selected: " + self.dlfolder)

    def browse_profilefolder(self):
        self.profilefolder = filedialog.askdirectory()
        self.button2_save_var.set(self.profilefolder)
        print("INFO: Opera Profile Folder selected: " + self.profilefolder)

    def browse_binfile(self):
        self.binfile = filedialog.askopenfile().name
        self.button3_save_var.set(self.binfile)
        print("INFO: Opera Binary EXE File selected: " + self.binfile)

    def show_widgets(self):
        # A frame with a button to quit the window
        self.frame1 = Frame(self.master)
        self.frame1.grid(row=0, column=0)

        self.label1 = Label(self.frame1, text="Opera Download Folder: ")
        self.label1.grid(row=0, column=0)

        self.button1_save_var = StringVar()
        self.button1 = Button(self.frame1, textvariable=self.button1_save_var, command=self.browse_dlfolder, width=70)
        self.button1.grid(row=0, column=1)
        self.button1_save_var.set("Browse...")

        self.label2 = Label(self.frame1, text="Opera Profile Folder: ")
        self.label2.grid(row=1, column=0)

        self.button2_save_var = StringVar()
        self.button2 = Button(self.frame1, textvariable=self.button2_save_var, command=self.browse_profilefolder,
                              width=70)
        self.button2.grid(row=1, column=1)
        self.button2_save_var.set("Browse...")

        self.label3 = Label(self.frame1, text="Opera Bin Exe: ")
        self.label3.grid(row=2, column=0)

        self.button3_save_var = StringVar()
        self.button3 = Button(self.frame1, textvariable=self.button3_save_var, command=self.browse_binfile, width=70)
        self.button3.grid(row=2, column=1)
        self.button3_save_var.set("Browse...")

        self.save_button = Button(self.frame1, text="Save & Exit", command=self.save_config, bg="lightgreen")
        self.save_button.grid(row=3, column=1)

        self.close_button = Button(self.frame1, text="Exit", command=self.close_window, bg="red")
        self.close_button.grid(row=3, column=0)


root = Tk()
app = Win1(root)
root.mainloop()
