import mechanicalsoup
URL = 'https://www.publix.com/savings/coupons/digital-coupons'


def run_script(username, password):
    ('Username: {} Password: {}'.format(username, password))
    browser = mechanicalsoup.StatefulBrowser()
    browser.open(URL)
    browser.follow_link("login")

    print(browser.get_url())
    # print(browser.get_current_page())
    browser.select_form('form[id="loginForm"]')
    # print(browser.get_current_form().print_summary())
    # print(browser.get_current_form())

    browser["UserName"]= username
    browser["Password"]= password

    print(browser.get_current_form().print_summary())
    

    #test in acutal browser
    # browser.launch_browser()
    # response= browser.submit_selected()
    # print(response.text)

def main():
    run_script('test', 'test')


if __name__ == "__main__":
    main()
