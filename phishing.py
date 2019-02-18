import requests
from bs4 import BeautifulSoup
import random
import json
import string
import time
import datetime

firstnames_file = open("firstnames.txt",encoding="utf8", errors='ignore')
finnish_words_file = open("finnish_words.txt",encoding="utf8", errors='ignore')
common_passwords_file = open("common_passwords.txt",encoding="utf8", errors='ignore')
output_file = open("output_file.txt", "a",encoding="utf8", errors='ignore')
common_english_words_file = open("english_words.txt",encoding="utf8", errors='ignore')
lastnames_file = open("lastnames.txt",encoding="utf8", errors='ignore')

alphabet = string.ascii_lowercase
firstnames_list = firstnames_file.read().splitlines()
lastnames_list = lastnames_file.read().splitlines()
finnish_words_file = finnish_words_file.read().splitlines()
common_passwords_list = common_passwords_file.read().splitlines()
common_english_words_list = common_english_words_file.read().splitlines()

def phising_1(userid, email, password):
    print("Sending a form with the following info: userid %s, email %s, password %s" % (userid, email, password))
    url = 'https://haaga-helia-desk.weebly.com//ajax/apps/formSubmitAjax.php'
    data = {"_u768032520541082005": email, "_u894627795127593335": userid, "_u125213772223352816": password,
            "ucfid": 123374606509319342}
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


def phising_3(firstname, lastname, userid, email, password):
    print("Sending a form with the following info: firstname %s, lastname %s, userid %s, email %s, password %s" % (firstname, lastname, userid, email, password))
    url = 'https://haaga-helia.weebly.com/ajax/apps/formSubmitAjax.php'
    data = {"_u581711145251090073[first]": firstname, "_u581711145251090073[last]": lastname, "u889022183156699632": email, "_u544484960623491938": password, "_u284261734227315756": password, "ucfid":361303802676750299}
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
    random_number = random.randrange(0,15)
    firstname = firstname.lower()
    firstname = firstname.replace('ö','o').replace('ä','a').replace('å','o')
    if random_number > 6:
        return firstname.title()
    else:
        return firstname


def get_password(name):
    random_number = random.randrange(0,19)
    random_symbols = ["!","?","@", "§", "$"]
    if random_number == 1:
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(random.randrange(8,20))) # Generates a password with random letters, varying between 9 and 19 characters in length
    elif random_number in [2,3]: #Generates a password that is firstname with first letter capitalized + random sequence of 2 digits + a random symbol
        return name.title() + str(random.randrange(10,20)) + random.choice(random_symbols)
    elif random_number in [4,5]: # chooses a random password from the most common passwords list
        return random.choice(finnish_words_file).title() + random.choice(random_symbols)
    elif random_number in [6,7]: # Chooses a password from the common passwords -list
        if random_number == 7: #first letter will be capitalized and a symbol will be added to the end
            return random.choice(common_passwords_list).title() + random.choice(random_symbols)
        else:
            return random.choice(common_passwords_list) # Only a random word from the common passwords list will be chosen
    elif random_number == 8: # A combination of firstname with first letter capitalized + two digits
        return random.choice(common_passwords_list) + name.title() + str(random.randrange(10,20))
    elif random_number == 9: # A random finnish word + 2 to 3 digits
        return random.choice(finnish_words_file) + random.choice(random_symbols) + str(random.randrange(10,200))
    elif random_number == 10: # A random english word with first letter capitalized + 2 or 3 digits
        return random.choice(common_english_words_list).title() + str(random.randrange(10,200)) + random.choice(random_symbols)
    elif random_number == 11: # name with one letter replaced + two to three random digits + a random symbol
        letter_to_replace = name[random.randrange(0, len(name))]
        return name.replace(letter_to_replace, letter_to_replace.upper()) + str(random.randrange(10,200)) + random.choice(random_symbols)
    elif random_number == 12: # A random english word without first letter capitalized + 2 or 3 digits
        return random.choice(common_english_words_list) + str(random.randrange(10,200))
    elif random_number == 13: # A random letter is replaced from name + capitalized + a random symbol is added + digits added to the end
        letter_to_replace = name[random.randrange(0, len(name))]
        return name.replace(letter_to_replace, letter_to_replace.upper() + random.choice(random_symbols)) + str(random.randrange(10,200))
    elif random_number == 14:  # A random letter in the name is replaced, two random symbols are added + a name is added to the end
        letter_to_replace = name[random.randrange(0, len(name))]
        return name.replace(letter_to_replace, random.choice(random_symbols) + random.choice(random_symbols)) + str(random.randrange(10, 200))
    elif random_number == 15:  # Two random words are joined together + a symbol is added
        return random.choice(common_english_words_list) + random.choice(common_english_words_list) + random.choice(random_symbols)
    elif random_number == 16:  # An english word is joined with a finnish word in Caps, a random symbol is added to the end
        return random.choice(common_english_words_list) + random.choice(finnish_words_file).upper() + random.choice(random_symbols)
    else: # A random finnish word with first letter capitalized + 2 or 3 digits
        return random.choice(finnish_words_file).title() + str(random.randrange(10,200))

def get_username():
    first_letter = random.choice(["a","A"])
    return first_letter + "1" + random.choice(["6","7"]) + "04" + str(random.randrange(100,999))

def get_firstname():
    random_firstname = random.choice(firstnames_list)
    return handle_name(random_firstname)

def get_lastname():
    random_lastname = random.choice(lastnames_list)
    return handle_name(random_lastname)

def get_domain():
    return random.choices(population=['myy.haaga-helia.fi', 'Myy.haaga-helia.fi', 'myy.Haaga-Helia.fi', 'haaga-helia.fi', 'haag-helia.fi', 'haagahelia.fi',
                                      'myyhaaga-helia.fi', 'haaga-helia.net', 'myy.haaga-helia.net', 'gmail.com', 'live.fi'], weights=[60, 50, 30, 20, 5, 5, 5, 5, 10,10,5],k=1)[0]

def get_email(username, domain):
    number = random.randrange(0,10)
    if number > 5:
        if username[0] == 'A':
            username = username.replace('A','a')
        else:
            username = username.replace('a', 'A')
    return ("%s@%s" % (username, domain))


def main():
    firstname, lastname = get_firstname(), get_lastname()
    password = get_password(random.choice([firstname, lastname]))
    random_domain = get_domain()
    username = get_username()
    email = get_email(username, random_domain)
    phising_1(username, email, password)
    time.sleep(0.1)

while True:
    main()

