import pytest
import subprocess


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

    # why does the flip button work here?
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

    # and the random button doesn't?
    # rand = selenium.find_element_by_id('random')
    # assert rand.is_displayed()
    # assert rand.text == 'RANDOM'
    # rand.click()
    # p = selenium.find_element_by_id('text')
    # # not a good test, but:
    # assert text not in p.text
