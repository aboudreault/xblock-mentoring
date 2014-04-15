# -*- coding: utf-8 -*-
#
# Copyright (C) 2014 Harvard
#
# Authors:
#          Xavier Antoviaque <xavier@antoviaque.org>
#
# This software's license gives you freedom; you can copy, convey,
# propagate, redistribute and/or modify this program under the terms of
# the GNU Affero General Public License (AGPL) as published by the Free
# Software Foundation (FSF), either version 3 of the License, or (at your
# option) any later version of the AGPL published by the FSF.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero
# General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program in a file in the toplevel directory called
# "AGPLv3".  If not, see <http://www.gnu.org/licenses/>.
#

# Imports ###########################################################

from selenium.webdriver.support.ui import WebDriverWait

from mentoring.test_base import MentoringBaseTest


# Classes ###########################################################

class AnswerBlockTest(MentoringBaseTest):

    def test_answer_edit(self):
        """
        Answers of same name should share value accross blocks
        """
        # Answer should initially be blank on all instances with the same answer name
        mentoring = self.go_to_page('Answer Edit 2')
        answer1_bis = mentoring.find_element_by_css_selector('.xblock textarea')
        answer1_readonly = mentoring.find_element_by_css_selector('blockquote.answer.read_only')
        self.assertEqual(answer1_bis.get_attribute('value'), '')
        self.assertEqual(answer1_readonly.text, '')

        # Another answer with the same name
        mentoring = self.go_to_page('Answer Edit 1')
        header1 = self.browser.find_element_by_css_selector('h1')
        self.assertEqual(header1.text, 'XBlock: Answer Edit 1')

        # Check <html> child
        p = mentoring.find_element_by_css_selector('div.xblock-light-child p')
        self.assertEqual(p.text, 'This should be displayed in the answer_edit scenario')

        # TODO, move that to main test_base to have a generic function that check completion
        # This is temporary and will be modified soon
        def check_data_completion(browser):
            data = browser.execute_script("return $('.xblock-light-child[data-type=\"AnswerBlock\"]').data();")
            return data['completed'] if 'completed' in data else False

        # Initial unsubmitted text
        answer1 = mentoring.find_element_by_css_selector('textarea')
        self.assertEqual(answer1.text, '')
        self.assertFalse(check_data_completion(self.browser))

        # Submit without answer
        submit = mentoring.find_element_by_css_selector('input.input-main')
        submit.click()
        self.assertEqual(answer1.get_attribute('value'), '')
        self.assertFalse(check_data_completion(self.browser))

        # Submit an answer
        answer1.send_keys('This is the answer')
        submit.click()

        self.assertEqual(answer1.get_attribute('value'), 'This is the answer')
        WebDriverWait(self.browser, 5).until(check_data_completion)
        self.assertTrue(check_data_completion(self.browser))

        # Answer content should show on a different instance with the same name
        mentoring = self.go_to_page('Answer Edit 2')
        answer1_bis = mentoring.find_element_by_css_selector('.xblock textarea')
        answer1_readonly = mentoring.find_element_by_css_selector('blockquote.answer.read_only')
        self.assertEqual(answer1_bis.get_attribute('value'), 'This is the answer')
        self.assertEqual(answer1_readonly.text, 'This is the answer')

    def test_answer_blank_read_only(self):
        """
        Read-only answers should not prevent completion when blank
        """
        # Check initial state
        mentoring = self.go_to_page('Answer Blank Read Only')
        answer = mentoring.find_element_by_css_selector('blockquote.answer.read_only')
        self.assertEqual(answer.text, '')
        # Submit should allow to complete
        submit = mentoring.find_element_by_css_selector('input.input-main')
        submit.click()

        # Wait and Check data completion
        # TODO, move that to main test_base to have a generic function that check completion
        # This is temporary and will be modified soon
        def check_data_completion(browser):
            data = browser.execute_script("return $('.xblock-light-child[data-type=\"AnswerBlock\"]').data();")
            return 'completed' in data

        WebDriverWait(self.browser, 5).until(check_data_completion)

        javascript = "return $('.xblock-light-child[data-type=\"AnswerBlock\"]').data('completed');"
        completed = self.browser.execute_script(javascript)
        self.assertTrue(completed)
