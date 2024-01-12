from pytest import raises
import project

def test_path():
    assert project.path(0) == 0
    assert project.path(1) == 1
    assert project.path(2) == 2
    assert project.path(3) == 3

    with raises(ValueError):
        assert project.path(4)
        assert project.path(-1)

def test_yx_values():
    assert project.yx_values(78, 102, 0, 'house') == (39, 48)
    assert project.yx_values(75, 132, 0, 'start') == (37, 63)
    assert project.yx_values(1, 5, 0, 'mall') == (0, 0)
    assert project.yx_values(12, 16, 13, 'house') == (19, 5)

def test_validate():
    assert project.validate('mario', 'mario(1985)')
    assert project.validate('zelda', 'zelda(1986)')
    assert not project.validate('mario(1985)', 'mario(1985)')
    assert not project.validate('mario', 'mario')
    assert project.validate('pokemon', 'pokemon(198)')