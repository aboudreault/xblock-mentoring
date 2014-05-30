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

import time

from mentoring.test_base import MentoringBaseTest


# Classes ###########################################################

class MCQBlockTest(MentoringBaseTest):

    def test_mcq_choices_rating(self):
        """
        Mentoring MCQ should display tips according to user choice
        """
        # Initial MCQ status
        mentoring = self.go_to_page('Mcq 1')
        mcq1 = mentoring.find_element_by_css_selector('fieldset.choices')
        mcq2 = mentoring.find_element_by_css_selector('fieldset.rating')
        messages = mentoring.find_elements_by_css_selector('.feedback')

        self.assertEqual(messages[0].text, '')
        self.assertEqual(messages[1].text, '')
        self.assertFalse(messages[0].find_elements_by_xpath('./*'))
        self.assertFalse(messages[1].find_elements_by_xpath('./*'))

        mcq1_legend = mcq1.find_element_by_css_selector('legend > p')
        mcq2_legend = mcq2.find_element_by_css_selector('legend')
        self.assertEqual(mcq1_legend.text, 'Do you like this MCQ?')
        self.assertEqual(mcq2_legend.text, 'How much do you rate this MCQ?')

        mcq1_choices = mcq1.find_elements_by_css_selector('.choices-list .choice label')
        mcq2_choices = mcq2.find_elements_by_css_selector('.choices-list .choice label')

        self.assertEqual(len(mcq1_choices), 3)
        self.assertEqual(len(mcq2_choices), 6)
        self.assertEqual(mcq1_choices[0].text, 'Yes')
        self.assertEqual(mcq1_choices[1].text, 'Maybe not')
        self.assertEqual(mcq1_choices[2].text, "I don't understand")
        self.assertEqual(mcq2_choices[0].text, '1')
        self.assertEqual(mcq2_choices[1].text, '2')
        self.assertEqual(mcq2_choices[2].text, '3')
        self.assertEqual(mcq2_choices[3].text, '4')
        self.assertEqual(mcq2_choices[4].text, '5')
        self.assertEqual(mcq2_choices[5].text, "I don't want to rate it")

        mcq1_choices_input = [
            mcq1_choices[0].find_element_by_css_selector('input'),
            mcq1_choices[1].find_element_by_css_selector('input'),
            mcq1_choices[2].find_element_by_css_selector('input'),
        ]
        mcq2_choices_input = [
            mcq2_choices[0].find_element_by_css_selector('input'),
            mcq2_choices[1].find_element_by_css_selector('input'),
            mcq2_choices[2].find_element_by_css_selector('input'),
            mcq2_choices[3].find_element_by_css_selector('input'),
            mcq2_choices[4].find_element_by_css_selector('input'),
            mcq2_choices[5].find_element_by_css_selector('input'),
        ]
        self.assertEqual(mcq1_choices_input[0].get_attribute('value'), 'yes')
        self.assertEqual(mcq1_choices_input[1].get_attribute('value'), 'maybenot')
        self.assertEqual(mcq1_choices_input[2].get_attribute('value'), 'understand')
        self.assertEqual(mcq2_choices_input[0].get_attribute('value'), '1')
        self.assertEqual(mcq2_choices_input[1].get_attribute('value'), '2')
        self.assertEqual(mcq2_choices_input[2].get_attribute('value'), '3')
        self.assertEqual(mcq2_choices_input[3].get_attribute('value'), '4')
        self.assertEqual(mcq2_choices_input[4].get_attribute('value'), '5')
        self.assertEqual(mcq2_choices_input[5].get_attribute('value'), 'notwant')

        submit = mentoring.find_element_by_css_selector('input.input-main')

        # submit shouldn't be enabled
        self.assertFalse(submit.is_enabled())

        # Select option in mcq1
        mcq1_choices_input[1].click()

        # mcq2 has no selection. submit shouldn't be enabled
        self.assertFalse(submit.is_enabled())

        # Select option in mcq2
        mcq2_choices_input[2].click()

        # submit should be enabled
        self.assertTrue(submit.is_enabled())

        submit.click()

        time.sleep(1)
        tips = [
            messages[0].find_element_by_css_selector('.tip > p'),
            messages[1].find_element_by_css_selector('.tip > p')
        ]
        self.assertEqual(len(tips), 2)
        self.assertEqual(tips[0].text, 'Ah, damn.')
        self.assertEqual(tips[1].text, 'Will do better next time...')

        # One with only display tip, one with reject tip - should not complete
        mcq1_choices_input[0].click()
        mcq2_choices_input[2].click()
        submit.click()

        time.sleep(1)
        tips = [
            messages[0].find_element_by_css_selector('.tip > p'),
            messages[1].find_element_by_css_selector('.tip > p')
        ]
        self.assertEqual(len(tips), 2)
        self.assertEqual(tips[0].text, 'Great!')
        self.assertEqual(tips[1].text, 'Will do better next time...')

        # Only display tips, to allow to complete
        mcq1_choices_input[0].click()
        mcq2_choices_input[3].click()
        submit.click()

        time.sleep(1)
        tips = [
            messages[0].find_element_by_css_selector('.tip > p'),
            messages[1].find_element_by_css_selector('.tip > p')
        ]
        self.assertEqual(len(tips), 2)
        self.assertEqual(tips[0].text, 'Great!')
        self.assertEqual(tips[1].text, 'I love good grades.')

        feedback = mentoring.find_element_by_css_selector('.message.completed p')
        self.assertEqual(feedback.text, 'Congratulations!')
