import re


def extract_backend_dependency_install(output):
    """
    Returns output for dependency install
    :param output:
    :returns:
    """
    start_index = 0
    for index, line in enumerate(output):
        if "Collecting stone-grading@" in line:
            start_index = index
            break

    end_index = 0
    for index, line in enumerate(output[start_index:]):
        if "Requirement already" in line:
            end_index = index

    index_count = 0
    for index, line in enumerate(output[end_index:]):
        if "Successfully installed" in line:
            index_count = index

    end_index += index_count

    return output[start_index : end_index + 1]


def extract_frontend_build_output(output):
    """
    Returns output for the frontend build
    :param output:
    :returns:
    """
    start_index = 0
    for index, line in enumerate(output):
        match = re.search(r"^> [A-Za-z]+@[0-9]+.[0-9]+.[0-9]+ build$", line)
        if match is not None:
            start_index = index
            break

    end_index = 0
    for index, line in enumerate(output):
        if "Find out more about deployment here:" in line:
            end_index = index + 2
            break

    return output[start_index : end_index + 1]


def extract_eslint_output(output):
    """
    Returns output for frontend linting
    :param output:
    :returns:
    """
    start_index = 0
    for index, line in enumerate(output):
        match = re.search(r"^> [A-Za-z]+@[0-9]+.[0-9]+.[0-9]+ lint$", line)
        if match is not None:
            start_index = index
            break

    end_index = 0
    for index, line in enumerate(output):
        if "All matched files use Prettier code style!" in line:
            end_index = index
            break


def extract_black_linting_output(output):
    """
    Returns output for black linting
    :param output:
    :returns:
    """


def extract_django_unittests_output(output):
    """
    Returns output for django unittests
    :param output:
    :returns:
    """
    start_index = 0
    for index, line in enumerate(output):
        if "django: settings: " in line:
            start_index = index - 2
            break

    end_index = 0
    for index, line in enumerate(output):
        match = re.search(
            r"^(=)* [0-9]+ failed, [0-9]+ passed, [0-9]+ errors in [0-9]+.[0-9]+s \(\d+.\d+.\d+\) (=)*",
            line,
        )
        if match is not None:
            end_index = index

    return output[start_index : end_index + 1]


def extract_selenium_tests_output(output):
    """
    Returns output for selenium tests
    :param output:
    :returns:
    """
