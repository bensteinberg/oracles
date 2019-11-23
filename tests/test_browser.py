import pytest
import subprocess
from itertools import repeat


@pytest.mark.skipif(subprocess.run(['which', 'geckodriver']).returncode != 0,
                    reason='No geckodriver')
@pytest.mark.firefox_arguments('-headless')
@pytest.mark.usefixtures('live_server')
def test_example(selenium, app):
    text = 'diminishment of faerieland kills civilization'
    reversal = 'diminishment of civilization kills faerieland'

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
        tup[0].click()
        p = tup[1].find_element_by_id('text')
        return p.text

    texts = [t for t in map(random_text, repeat((rand, selenium), 100))]
    # not necessarily true, but pretty likely
    assert not all(t == texts[0] for t in texts)

    for button in selenium.find_elements_by_class_name('oracle'):
        o = button.get_attribute('id')
        button.click()
        h1 = selenium.find_element_by_id('oracle')
        assert h1.text == o
