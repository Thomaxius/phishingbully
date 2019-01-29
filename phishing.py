import requests
from bs4 import BeautifulSoup
import random
import json
import string
import time
import datetime

firstnames_file = open("firstnames.txt")
finnish_words_file = open("finnish_words.txt")
common_passwords_file = open("common_passwords.txt")
output_file = open("output_file.txt", "a")
common_english_words_file = open("english_words.txt")

alphabet = string.ascii_lowercase
firstnames_list = firstnames_file.read().splitlines()
finnish_words_file = finnish_words_file.read().splitlines()
common_passwords_list = common_passwords_file.read().splitlines()
common_english_words_list = common_english_words_file.read().splitlines()

def phising_1(userid, email, password):
    print("Sending a form with the following info: userid %s, email %s, password %s" % (userid, email, password))
    url = 'https://haaga-hel1a-helpdesk.weebly.com/ajax/apps/formSubmitAjax.php'
    data = {"_u697771171613901263": userid, "_u770510225617309293": email, "_u347286333246038102": password,
            "ucfid": 407087612984639270}
    r = requests.post(url, data=data)
    html_response = r.text
    soup = BeautifulSoup(html_response)
    response_json = json.loads(soup.find(id="response").text)
    if not response_json:
        print("No response div found")
        return
    if response_json.get('success'):
        print('Succesfully sent fake form data')
    else:
        print('Failed to send form data: ', response_json)

def phising_2(userid, email, password):
    print("Sending a form with the following info: userid %s, email %s, password %s" % (userid, email, password))
    url = 'https://my-haga-helia-fi.weebly.com/ajax/apps/formSubmitAjax.php'
    data = {"_u697771171613901263": userid, "_u770510225617309293": email, "_u347286333246038102": password, "ucfid":361303802676750299}
    r = requests.post(url, data=data)
    html_response = r.text
    soup = BeautifulSoup(html_response)
    response_json = json.loads(soup.find(id="response").text)
    if not response_json:
        print("No response div found")
        return
    if response_json.get('success'):
        print('Succesfully sent fake form data')
        output_file.write("%s   %s  %s  %s\n" % (userid, email, password, datetime.datetime.now()))
    else:
        print('Failed to send form data: ', response_json)


def handle_name(firstname):
    firstname = firstname.lower()
    firstname = firstname.replace('ö','o').replace('ä','a').replace('å','o')
    if random.randrange(0,10) == 1:
        return firstname.title()
    else:
        return firstname.upper()


def get_password():
    random_number = random.randrange(0,15)
    random_symbols = ["!","?","@", "§", "$"]
    if random_number == 1:
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(random.randrange(8,20))) # Generates a password with random letters, varying between 9 and 19 characters in length
    if random_number in [2,3]: #Generates a password that is firstname with first letter capitalized + random sequence of 2 digits + a random symbol
        firstname = get_firstname()
        return firstname.title() + str(random.randrange(10,20)) + random.choice(random_symbols)
    if random_number in [4,5]: # chooses a random password from the most common passwords list
        return random.choice(finnish_words_file).title() + random.choice(random_symbols)
    if random_number in [6,7]: # Chooses a password from the common passwords -list
        if random_number == 7: #first letter will be capitalized and a symbol will be added to the end
            return random.choice(common_passwords_list).title() + random.choice(random_symbols)
        else:
            return random.choice(common_passwords_list) # Only a random word from the common passwords list will be chosen
    if random_number == 8: # A combination of firstname with first letter capitalized + two digits
        firstname = get_firstname()
        return random.choice(common_passwords_list) + firstname.title() + str(random.randrange(10,20))
    if random_number == 9: # A random finnish word + 2 to 3 digits
        return random.choice(finnish_words_file) + str(random.randrange(10,200))
    if random_number == 10: # A random english word with first letter capitalized + 2 or 3 digits
        return random.choice(common_english_words_list).title() + str(random.randrange(10,200))
    if random_number == 11: # A random english word without first letter capitalized + 2 or 3 digits
        return random.choice(common_english_words_list) + str(random.randrange(10,200))
    else: # A random finnish word with first letter capitalized + 2 or 3 digits
        return random.choice(finnish_words_file).title() + str(random.randrange(10,200))

def get_username():
    first_letter = random.choice(["a","A"])
    return first_letter + "1" + random.choice(["6","7"]) + str(random.randrange(10000,20000))

def get_firstname():
    random_firstname = random.choice(firstnames_list)
    return handle_name(random_firstname)

def get_domain():
    return random.choices(population=['myy.haaga-helia.fi', 'haaga-helia.fi', 'haag-helia.fi', 'haagahelia.fi',
                                      'myyhaaga-helia.fi', 'haaga-helia.net', 'myy.haaga-helia.net', 'gmail.com', 'live.fi'], weights=[60, 20, 5, 5, 5, 5, 10,10,5],k=1)[0]


def main():
    password = get_password()
    random_domain = get_domain()
    username = get_username()
    email = ("%s@%s" % (username, random_domain))
    phising_2(username, email, password)
    time.sleep(0.05)

while True:
    main()

