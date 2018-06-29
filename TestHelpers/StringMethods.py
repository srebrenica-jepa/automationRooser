#!/usr/bin/env python
import random
import string
import socket
import struct


def get_unique_string(prefix='random_', unicode=False):
    """
    Used for any name that needs to be unique and can contains Letter (lower and upper case) and Digits
    :param prefix:
    :param unicode:
    :return:
    """
    chars = string.letters + string.digits
    random_text = ''.join([random.choice(chars) for _ in xrange(5)])

    if unicode:
        return u'random_' + random_text

    return prefix + random_text


def get_unique_name(prefix='random_', unicode=False):
    """
    Used for Authentication names, as this unique name is only composed of Digits (Authentication names cannot
    contain Uppercase characters)
    :param prefix:
    :param unicode:
    :return:
    """
    chars = string.digits
    random_text = ''.join([random.choice(chars) for _ in xrange(5)])

    if unicode:
        return u'random_' + random_text

    return prefix + random_text


def get_unique_ipv4():
    address = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
    if '127' not in address:
        return address
    return get_unique_ipv4()


def get_unique_ipv6():
    return ':'.join(("%x" % random.randint(0, 16**4) for _ in range(8)))


def get_unique_ipv4_range():
    ip = ".".join(map(str, (random.randint(0, 255)
                            for _ in range(3)))) + "." + str(random.randint(0, 254))

    a, b, c, d = ip.split(".")
    if int(c) < 255:
        return ip + "-" + a + "." + b + "." + str(int(c)+1) + "." + d
    else:
        return ip + "-" + a + "." + b + "." + c + "." + str(int(d)+1)


def get_unique_ipv6_range():
    ip = ':'.join(("%x" % random.randint(0, 16**4) for _ in range(8)))
    a, b, c, d, e, f, g, h = ip.split(":")
    return ip + "-" + a + ":" + b + ":" + c + ":" + d + ":" + e + ":" + f + ":" + g + ":" + str(hex(int(h, 16)+1).lstrip("0x"))


def get_unique_email(prefix='random_', unicode=False):
    """
    Used for emails as this unique email is only composed of lowercase characters and has to have the format
    characters@characters.characters (Emails cannot contain Uppercase characters or digits)
    :param prefix:
    :param unicode:
    :return:
    """
    chars = string.lowercase
    random_user = ''.join([random.choice(chars) for _ in xrange(3)])
    random_provider = ''.join([random.choice(chars) for _ in xrange(5)])
    random_ending = ''.join([random.choice(chars) for _ in xrange(3)])

    if unicode:
        return u'random_' + random_user + '@' + random_provider + '.' + random_ending

    return prefix + random_user + '@' + random_provider + '.' + random_ending


def get_unique_password(prefix='random_', unicode=False):
    """
    Used for any password that needs to be unique and that has to contain at least one lowercase, uppercase, number
    and special character
    :param prefix:
    :param unicode:
    :return:
    """
    random_text_lowercase = ''.join([random.choice(string.lowercase) for _ in xrange(3)])
    random_text_uppercase = ''.join([random.choice(string.uppercase) for _ in xrange(3)])
    random_text_digits = ''.join([random.choice(string.digits) for _ in xrange(3)])
    random_text_character = ''.join([random.choice(string.punctuation) for _ in xrange(3)])

    if unicode:
        return u'random_' + random_text_lowercase + random_text_uppercase + random_text_digits + random_text_character

    return prefix + random_text_lowercase + random_text_uppercase + random_text_digits + random_text_character


def get_unique_number():
    """
    Used for any number that needs to be unique
    :return:
    """
    number = string.digits
    random_number = ''.join([random.choice(number) for _ in xrange(3)])

    return random_number


def get_unique_real_number_less_than_1():
    """
    Used for any unique real number less then 1
    :return:
    """
    number = string.digits
    random_number = ''.join([random.choice(number) for _ in xrange(1)])

    return '0' + '.' + random_number


def get_unique_phone_number():
    """
    Used for any phone number(11 digits and the 1st digit is 0) that needs to be unique
    :return:
    """
    number = string.digits
    random_number = ''.join([random.choice(number) for _ in xrange(10)])

    return '0' + random_number
