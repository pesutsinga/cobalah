from splinter import Browser
from bs4 import BeautifulSoup
import time

class ChopeBrowser:
    def __init__(self, headless=False):
        self.chrome = Browser('chrome', headless=headless)

    def time_delay(self, time):
        self.chrome.is_element_present_by_name('!@#$%^&*())(*&^%$#@!', wait_time=time)

    def login(self, usr, pwd, domain='STUDENT'):
        url = 'https://ntupcb.ntu.edu.sg'
        url += '/fbscbs/Account/SignIn?ReturnUrl=%2ffbscbs'
        self.chrome.visit(url)
        dropdown = self.chrome.find_by_tag('option')

        for option in dropdown:
            if option.text == domain:
                option.click()

        self.chrome.fill('Username', usr)
        self.chrome.fill('Password', pwd + '\n')


# PC BOOKING STARTS HERE
    def pc_setup(self, Type):
        button = self.chrome.find_by_id('tdPcBook')
        button.click()
        time.sleep(1)
        with self.chrome.get_iframe('frmAdminViewControls') as iframe:
            iframe.find_by_id('pnlInsLoc3').click()
        self.type_number(Type)
        data = self.scrape_pc()
        print(data[0])
        print(data[1], data[2])
        print(self.book_pc(data[1], data[2]))

    def type_number(self, Types):
        for i in range(0, 5):
            with self.chrome.get_iframe('frmAdminViewControls') as iframe:
                page = iframe.find_by_id('pnlInsPcGrp'+str(i))
                if page != []:
                    page = page.html
                    page = BeautifulSoup(page, "lxml")
                    page = page.find("span", {"style": "display:inline-block;height:20px;width:80px;"})
                    page = page.get_text()
                    if page == Types:
                        page = iframe.find_by_id('pnlInsPcGrp'+str(i)).click()
                    return 0

    def scrape_pc(self):
        with self.chrome.get_iframe('frmSeating') as iframe:
            for i in range(0, 6):
                for j in range(1, 11):
                    idd = 'grdSeating_tblCol' + str(j) + '_' + str(i)
                    parse = iframe.find_by_id(idd)
                    if parse == []:
                        return 'no pc', 100, 100
                        break
                    if parse != []:
                        warna = self.color(parse.html)
                    if (warna == '#FFFFFF'):
                        return self.name_pc(parse.html), j, i
        no_pc = 'no pc'
        j = 100
        i = 100
        return no_pc, j, i

    def name_pc(self, codes):
        soup = BeautifulSoup(codes, "lxml")
        mydivs = soup.findAll("span", {"class": "lblPcName"})
        return mydivs[0].get_text()

    def color(self, code):
        soup = BeautifulSoup(code, "lxml")
        tag = soup.findAll('td', {"style": "background-color: #FFFFFF"})
        if tag != []:
            return '#FFFFFF'
        else:
            return 'blabla'

    def book_pc(self, col, row):
        with self.chrome.get_iframe('frmSeating') as iframe:
            if (col != 100) and (row != 100):
                try:
                    time.sleep(1)
                    print('a')
                    butt = iframe.find_by_id("grdSeating_divOuterCol" + str(col)+"_" + str(row))
                    if butt != []:
                        butt.click()
                    print('a')
                    time.sleep(2)
                    sub = iframe.find_by_name("btnsumit")
                    print('a')
                    sub.click()
                    print('a')
                    return "booked"
                except:
                    time.sleep(0.5)
                    self.chrome.fill('\n')
                    return "cannot book"
        return "cannot book"

    def first_setup(self):
        button = self.chrome.find_by_id('tdFacilityBook')
        button.click()
        self.chrome.click_link_by_href('#8')
        self.chrome.click_link_by_href('#-1')
        self.chrome.click_link_by_href('/fbscbs/Booking/Create?resourceId=69')
        self.chrome.click_link_by_id('book')
        self.chrome.click_link_by_id('changeResource')
        self.chrome.click_link_by_href('#-1')
        self.chrome.click_link_by_id('book')

    def is_registered(event):
        if event.has_class('noShowWhite'):
            return False
        if event.has_class('currentEvent'):
            return False
        return True

    def check_facility(self, evFacilities):
        columnWeek = self.chrome.find_by_css('.wc-event-column')
        evWeek = []
        for columnDay in columnWeek:
            evToday = []
            evList = columnDay.find_by_css('.ui-corner-all')
            for event in evList:
                if not event.has_class('noShowWhite'):
                    if not event.has_class('currentEvent'):
                        event = event.text
                        if not event.find('—') == -1:
                            if event == '':
                                continue
                            evToday.append(event.split('—'))
            evWeek.append(evToday)
        evFacilities.append(evWeek)

    def click_next(self, counter, evFacilities):
        # Kerja rekursif dengan check_facility.
        # Milih option facility berdasarkan counter.
        dropdown = self.chrome.find_by_id('ResourceId')
        options = dropdown.find_by_tag('option')
        if counter < len(options):
            nextOption = options[counter]
            nextOption.click()
            self.check_facility(counter, evFacilities)
        else:
            return evFacilities

    def scrape_seats(self, usr, pwd):
        self.login(usr, pwd)
        self.first_setup()
        evFacilities = []
        dropdown = self.chrome.find_by_id('ResourceId')
        options = dropdown.find_by_tag('option')
        optRange = range(len(options))
        for i in optRange:
            opt = options[i]
            nextOption = opt
            nextOption.click()
            self.time_delay(0.05)
            # while loadingTitle.visible:
            #     pass
            evFacilities.append(opt.text)
            self.check_facility(evFacilities)
        self.quit()
        return evFacilities

    def quit(self):
        self.chrome.quit()

def try_login(usr, pwd):
    # return True    # TODO: REMOVE THIS DEBUG
    instances = ChopeBrowser()
    url = 'https://ntupcb.ntu.edu.sg'
    url += '/fbscbs/Account/SignIn?ReturnUrl=%2ffbscbs'
    instances.chrome.visit(url)
    instances.chrome.fill('Username', usr)
    instances.chrome.fill('Password', pwd + '\n')
    loginCheck = instances.chrome.find_by_id('login')
    instances.quit()
    return loginCheck == []


def main():
    bro = ChopeBrowser()
    # usr = input("usr")
    # pwd = input("pwd")
    sol = ChopeBrowser()
    sol.login('echristo001', "Sayaanakrajin!2")
    sol.pc_setup(" (1) Single Monitors")
    print(sol)


if __name__ == '__main__':
    main()
