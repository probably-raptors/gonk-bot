def atoi(s):
    # convert object s to int without exception
    try:
        return int(s)
    except:
        return 0


def atof(s):
    # convert object s to float without exception
    try:
        return float(s)
    except:
        return 0


def atos(s):
    # convert object s to str without exception
    try:
        return str(s)
    except:
        return ""
