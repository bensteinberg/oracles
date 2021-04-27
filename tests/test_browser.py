import pytest
import subprocess
from itertools import repeat
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.skipif(subprocess.run(['which', 'chromedriver']).returncode != 0,
                    reason='No chromedriver')
@pytest.mark.usefixtures('live_server')
def test_example(selenium, app, text, reversal, chrome_options):
    selenium.get('http://localhost:5000/oracles/angst/1/1/1/1/1/1')

    h1 = selenium.find_element_by_id('oracle')
    assert h1.text == 'angst'

    p = selenium.find_element_by_id('text')
    assert p.is_displayed()
    assert text in p.text

    flip = selenium.find_element_by_id('flip')
    assert flip.text == 'FLIP'

    flip.click()
    p = selenium.find_element_by_id('reversal')
    assert p.is_displayed()
    assert reversal in p.text
    assert flip.text == 'BACK'

    flip.click()
    p = selenium.find_element_by_id('text')
    assert p.is_displayed()
    assert text in p.text

    rand = selenium.find_element_by_id('random')
    assert rand.is_displayed()
    assert rand.text == 'RANDOM'

    def random_text(tup):
        """ this takes a function and the driver """
        tup[0].click()
        p = tup[1].find_element_by_id('text')
        return p.text

    # The following section tests two things: first, that clicking the
    # random button produces different big pictures, and second, that
    # clicking the browser's back button produces the same sequence of
    # big pictures in reverse. (That is, testing the popstate listener
    # in app/static/oracle.js.) This sequence is fragile; when n is 50
    # or 100, the latter assertion tends to fail; n of 10 mostly works.
    n = 10
    texts = list(map(random_text, repeat((rand, selenium), n)))

    # not necessarily true, but pretty likely -- how likely? with n == 10,
    # the assertion will fail once in 10 * 2 * 46,656 == 933,120 times,
    # almost one in a million, a probability of 0.000001072
    assert not all(t == texts[0] for t in texts)

    # now test the back button
    rev_texts = [texts[-1]]
    for _ in range(1, n):
        selenium.back()
        # the following awkward sequence is to get around what looks
        # like an inconsistent response of the driver to clicking on
        # the back button
        try:
            p = WebDriverWait(selenium, 10).until(
                EC.presence_of_element_located((By.ID, 'text')))
            rev_texts.append(p.text)
        except StaleElementReferenceException:
            selenium.get(selenium.current_url)
            p = WebDriverWait(selenium, 10).until(
                EC.presence_of_element_located((By.ID, 'text')))
            rev_texts.append(p.text)
    assert list(reversed(texts)) == rev_texts

    # check the oracle buttons
    for button in selenium.find_elements_by_class_name('oracle'):
        o = button.get_attribute('id')
        button.click()
        h1 = selenium.find_element_by_id('oracle')
        assert h1.text == o
