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


def try_login(usr, pwd):
    return True    # TODO: REMOVE THIS DEBUG
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
