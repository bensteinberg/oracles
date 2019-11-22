import pytest


@pytest.fixture
def app():
    from server import app
    return app


@pytest.mark.firefox_arguments('-headless')
@pytest.mark.usefixtures('live_server')
def test_example(selenium, app):
    selenium.get('http://localhost:5000/oracles/angst/1/1/1/1/1/1')

    h1 = selenium.find_element_by_id('oracle')
    assert h1.text == 'angst'

    p = selenium.find_element_by_id('text')
    assert 'diminishment of faerieland kills civilization' in p.text

    flip = selenium.find_element_by_id('flip')

    flip.click()
    p = selenium.find_element_by_id('reversal')
    assert 'diminishment of civilization kills faerieland' in p.text

    flip.click()
    p = selenium.find_element_by_id('text')
    assert 'diminishment of faerieland kills civilization' in p.text

    rand = selenium.find_element_by_id('random')
    rand.click()
    h1 = selenium.find_element_by_id('oracle')
    assert h1.text in ['angst', 'rancor']