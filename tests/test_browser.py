import os
from playwright.sync_api import Page, expect


# https://stackoverflow.com/a/64504144/4074877
if os.uname().sysname == 'Darwin':
    import multiprocessing
    multiprocessing.set_start_method("fork")


def test_example(page: Page, text, reversal):
    page.goto('http://localhost:5000/oracles/angst/1/1/1/1/1/1')

    expect(page).to_have_title('Oracles')

    expect(page.get_by_role('heading')).to_have_text('angst')

    expect(page.get_by_text(text)).to_be_visible()
    expect(page.get_by_text(reversal)).not_to_be_visible()

    page.get_by_text('flip', exact=True).click()

    expect(page.get_by_text(reversal)).to_be_visible()
    expect(page.get_by_text(text)).not_to_be_visible()

    page.get_by_text('back', exact=True).click()

    expect(page.get_by_text(text)).to_be_visible()
    expect(page.get_by_text(reversal)).not_to_be_visible()


def test_random_and_back(page: Page):
    # The following section tests two things: first, that clicking the
    # random button produces different big pictures, and second, that
    # clicking the browser's back button produces the same sequence of
    # big pictures in reverse. (That is, testing the popstate listener
    # in app/static/oracle.js.) This sequence is fragile; when n is 50
    # or 100, the latter assertion tends to fail; n of 10 mostly works.
    page.goto('http://localhost:5000/oracles/angst/1/1/1/1/1/1')

    texts = []
    n = 10
    for _ in range(n):
        page.get_by_text('random', exact=True).click(delay=7)
        t = page.get_by_title('oracle').text_content()
        texts.append(t)

    # not necessarily true, but pretty likely -- how likely? with n == 10,
    # the assertion will fail once in 10 * 2 * 46,656 == 933,120 times,
    # almost one in a million, a probability of 0.000001072
    assert not all(t == texts[0] for t in texts)

    # why does this work often but not always?
    expect(page.get_by_title('oracle')).to_have_text(texts[-1])

    # now test the back button, also does not always work
    texts.reverse()
    for i in range(n):
        expect(page.get_by_title('oracle')).to_have_text(texts[i])
        page.go_back()


def test_oracle_buttons(page: Page, text, reversal):
    buttons = page.get_by_role('button')
    for i in range(buttons.count()):
        oracle = buttons.nth(i).text_content()
        if oracle not in ['random', 'flip']:
            buttons.nth(i).click()
            expect(page.get_by_role('heading')).to_have_text(oracle)
