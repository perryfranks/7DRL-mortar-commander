from graphics.titles import get_welcome_message


def test_get_welcome_message():
    """
        Simply runs to try to catch whether there will be any errors thrown.
        A bad test style but would have helped earlier in the project.
    """
    for i in range(1000):
        get_welcome_message()

