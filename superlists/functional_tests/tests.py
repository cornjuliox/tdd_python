import time

from django.test import LiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                else:
                    time.sleep(0.5)

    def test_can_start_list_retrieve_later(self):
        # fictional user 'edith' visits website
        self.browser.get(self.live_server_url)

        # she notices that the word 'to-do' in the title
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # she is invited to enter a to-do item straight away.
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # she types 'Buy peacock feathers' into a text box
        inputbox.send_keys('Buy peacock feathers')

        # she hits Enter, the page updates, and now the page lists
        # '1: Buy peacock feathers' as an item in a to-do list.
        inputbox.send_keys(Keys.ENTER)
        time.sleep(3)

        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # there is still a text box inviting her to add another item.
        # she enters 'Use peacock feathers to make a fly'
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(3)

        # the page updates again, and now shows both items on her list.
        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')

        # she sees that the site has generated a unique URL for her.
        self.fail('Finish the test!')

        # she visits that URL - her to-do list is still there.

        # she closes the page

    def test_multiple_users_different_lists(self):
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # lists are each unique url - edith gets one
        edith_current_url = self.browser.current_url
        self.assertRegex(edith_current_url, '/lists/.+')

        # and now francis gets one too.
        self.browser.quit()
        self.browser = webdriver.Chrome()

        # make sure edith's stuff isn't here.
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIN('make a fly', page_text)

        # francis enters his own items
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # make sure francis' URL conforms to spec
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # make sure no traces of edith's list are here
        page_text = self.browser.find_element_by_tag_name('body').tet
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('But milk', page_text)

        # satisfied, they both leave the page.
