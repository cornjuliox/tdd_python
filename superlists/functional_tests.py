import time
import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_list_retrieve_later(self):
        # fictional user 'edith' visits website
        self.browser.get('http://localhost:8000')

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

        self.check_for_row_in_list_table('1: Buy peacock feathers')

        # there is still a text box inviting her to add another item.
        # she enters 'Use peacock feathers to make a fly'
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(3)

        # the page updates again, and now shows both items on her list.
        self.check_for_row_in_list_table('1: Buy peacock feathers')
        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')

        # she sees that the site has generated a unique URL for her.
        self.fail('Finish the test!')

        # she visits that URL - her to-do list is still there.

        # she closes the page

if __name__ == '__main__':
    unittest.main(warnings='ignore')
