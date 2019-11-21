from click.testing import CliRunner


def test_cli():
    from oracles import main

    text = 'diminishment of faerieland kills civilization'

    # no options
    runner = CliRunner()
    result = runner.invoke(main, [])
    assert result.exit_code == 0

    # specify the oracle
    result = runner.invoke(main, '-o angst')
    assert result.exit_code == 0

    # oracle substring
    result = runner.invoke(main, '-o ngst')
    assert result.exit_code == 0

    # specify roll but not oracle
    result = runner.invoke(main, '-d 1 1 1 1 1 1')
    assert result.exit_code == 0

    # specify everything
    result = runner.invoke(main, '-o angst -d 1 1 1 1 1 1')
    assert result.exit_code == 0
    assert result.output == '%s\n' % text

    # specify everything, verbose output
    result = runner.invoke(main, '-o angst -d 1 1 1 1 1 1 -v')
    assert result.exit_code == 0
    assert result.output == ("<Oracle 'angst' (1, 1, 1, 1, 1, 1) "
                             "'%s'>\n") % text

    # invalid dice roll
    result = runner.invoke(main, '-o angst -d 1 1 1 1 1 7')
    assert result.exit_code == 2
    assert 'is not in the valid range of 1 to 6.' in result.output

    # invalid oracle
    result = runner.invoke(main, '-o x')
    assert result.exit_code == 2
    assert 'not a valid' in result.output

    # ambiguous oracle
    result = runner.invoke(main, '-o an')
    assert result.exit_code == 2
    assert 'ambiguous' in result.output
