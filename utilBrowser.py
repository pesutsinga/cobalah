from splinter import Browser


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
    def pc_setup(self, Library, Type):
        with self.chrome.get_iframe('frmAdminViewControls') as iframe:
            iframe.find_by_id('pnlInsLoc3').click()
        self.type_number(self, Type)
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
                    page = page.find("span", {"style": "display:inline-block;height\
                        :20px;width:80px;"})
                    page = page.get_text()
                    if page == Types:
                        page = iframe.find_by_id('pnlInsPcGrp'+str(i)).click()
                    return 0

    def scrape_pc(self):
        with self.chrome.get_iframe('frmSeating') as iframe:
            no_pc = 'no pc'
            for i in range(0, 6):
                for j in range(1, 11):
                    idd = 'grdSeating_tblCol' + str(j) + '_' + str(i)
                    parse = iframe.find_by_id(idd)
                    if parse == []:
                        return no_pc, 100, 100
                    if parse != []:
                        warna = self.color(parse.html)
                        if warna == '#FFFFFF':
                            return self.name_pc(parse.html), j, i
        return no_pc, 100, 100

    def name_pc(self, codes):
        soup = BeautifulSoup(codes, "lxml")
        mydivs = soup.findAll("span", {"class": "lblPcName"})
        return mydivs[0].get_text()

    def color(code):
        soup = BeautifulSoup(code, "lxml")
        tag = soup.findAll("span", {"class": "lblPcName"})
        if tag != []:
            return '#FFFFFF'
        else:
            return 'blabla'

    def book_pc(self, col, row):
        with self.chrome.get_iframe('frmSeating') as iframe:
            if (col < 99) and (row < 99):
                time.sleep(1)
                butt = iframe.find_by_id("grdSeating_divOuter\
                    Col" + str(col) + "_" + str(row))
                if butt != []:
                    butt.click()
                time.sleep(2)
                sub = iframe.find_by_name('btnsumit')
                try:
                    sub.click()
                except:
                    return "not booked"
                return "booked"
        return "not booked"

    # Initializes the clicks and selections to reach the booking page. Also changes facility type to 'All Facilities'.
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

    # Eliminates unnecessary booking slots that are still bookable
    def is_registered(event):
        if event.has_class('noShowWhite'):
            return False
        if event.has_class('currentEvent'):
            return False
        return True

    # Adds weekly booked slots for selected facility to list.
    # Each list of weekly bookings contain lists of daily bookings,
    # each containing lists booked slots, determined by start- and end-time of booking, for that day.
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

    # Does the whole scraping from logging in, initializing clicks and selections,
    # and scraping bookings from each facility
    def scrape_seats(self, usr, pwd):
        self.login(usr, pwd)
        self.first_setup()
        evFacilities = []
        dropdown = self.chrome.find_by_id('ResourceId')
        options = dropdown.find_by_tag('option')
        for opt in options:
            nextOption = opt
            nextOption.click()
            self.time_delay(0.1)
            # while loadingTitle.visible:
            #     pass
            evFacilities.append(opt.text)
            self.check_facility(evFacilities)
        return evFacilities

    def quit(self):
        self.chrome.quit()

# Checks if the user can successfully login
def try_login(usr, pwd):
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
    usr = input("usr")
    pwd = input("pwd")
    sol = bro.scrape_seats(usr, pwd)
    print(sol)


if __name__ == '__main__':
    main()
