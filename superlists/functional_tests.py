from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_list_retrieve_later(self):
        self.browser.get('http://localhost:8000')
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!')

# fictional user 'edith' visits website

# she notices that the word 'to-do' in the title

# she is invited to enter a to-do item straight away.

# she types 'Buy peacock feathers' into a text box

# she hits Enter, the page updates, and now the page lists
# '1: Buy peacock feathers' as an item in a to-do list.

# there is still a text box inviting her to add another item.
# she enters 'Use peacock feathers to make a fly'

# the page updates again, and now shows both items on her list.

# she sees that the site has generated a unique URL for her.

# she visits that URL - her to-do list is still there.

# she closes the page

if __name__ == '__main__':
    unittest.main(warnings='ignore')
