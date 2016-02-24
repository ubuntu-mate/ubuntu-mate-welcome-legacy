#! /usr/bin/python3
# -*- coding:utf-8 -*-

def get_country_codes():

    """ Read country codes /usr/share/i18n/SUPPORTED

    Returns:
        a list containing the country codes, or None if an error occured reading the codes
    """

    codes = []
    codefile = open("/usr/share/i18n/SUPPORTED")
    for code in codefile:

        thiscode = None

        iscomment = code.startswith('#')
        if not iscomment:

            # check for a two character country code
            if (code[2] == " ") or (code[2] == "."):
                thiscode = code[0:]
            elif code[2] == "_":
                thiscode = code[0:5]
            elif code[3] == "_":
                thiscode = code[0:6]

            if thiscode is not None:
                thiscode = thiscode.split()[0]
                thiscode = thiscode.split(".")[0]

            if not thiscode in codes:
                codes.append(thiscode)

    return codes
