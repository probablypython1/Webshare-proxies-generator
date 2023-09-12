import requests
import random
import time
import capsolver
import colorama
from colorama import init, Fore
init(autoreset=True)
capsolver.api_key = "" # capsolver key here



def generate_random_email():
    random.seed(time.time())
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    email = "".join(random.choice(chars) for _ in range(8))
    print("[!]" + Fore.BLUE + " Successfully generated email")
    return f"{email}@outlook.fr"

def solve_captcha():
    try:
        while True:
            solution = capsolver.solve({
                "type": "ReCaptchaV2TaskProxyLess",
                "websiteURL": "https://proxy2.webshare.io/",
                "websiteKey": "6LeHZ6UUAAAAAKat_YS--O2tj_by3gv3r_l03j9d",
                "isInvisible": True,
            })
            captcha_solution = solution.get('gRecaptchaResponse')
            return captcha_solution
    except Exception as e:
        print(f"An error occurred: {e}")

def register():
    try:
        url = "https://proxy.webshare.io/api/v2/register/"

        
        email = generate_random_email()
        payload = {
            "email": email,
            "password": "=vi*'*?s#\"bV2r7",
            "tos_accepted": True,
            "recaptcha": solve_captcha(),
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Content-Type": "application/json",
            "Connection": "keep-alive",
            "Host": "proxy.webshare.io",
            "Origin": "https://proxy2.webshare.io",
            "Referer": "https://proxy2.webshare.io/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "TE": "trailers",
        }
        response = requests.post(url, json=payload, headers=headers)
        response_json = response.json()
        tokenn = response_json.get("token")
        if not tokenn:
            print(response_json)
            raise Exception("Failed to extract token from response")
        return tokenn
    except Exception as e:
        print(f"An error occurred: {e}")
        register()

def get_proxy(token):
    try:
        while True:
            url = "https://proxy.webshare.io/api/v2/proxy/config/"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0",
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate, br",
                "Authorization": f"Token {token}",
                "Origin": "https://proxy2.webshare.io",
                "Connection": "keep-alive",
                "Referer": "https://proxy2.webshare.io/",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-site",
                "Pragma": "no-cache",
                "Cache-Control": "no-cache",
                "TE": "trailers",
            }
            response = requests.get(url, headers=headers)
            response_json = response.json()
            proxiesdownload = response_json.get("proxy_list_download_token")
            mano = f"https://proxy.webshare.io/api/v2/proxy/list/download/{proxiesdownload}/-/any/username/direct/-/"
            sticky = requests.get(mano)
            stick = sticky.text
            username = response_json.get("username")
            password = response_json.get("password")
            rotating = f"{username}-rotate:{password}@p.webshare.io:80"

            with open("./sticky.txt", "a") as file:
                file.write(stick)  

            with open("./rotating.txt", "a") as file:
                file.write(rotating + "\n")

            print(f"[=]" + Fore.GREEN + f" Proxies successfully saved\n")

            return mano
    except Exception as e:
        print(f"An error occurred: {e}")
        register()

if __name__ == "__main__":
    try:
        for i in range(9999999):
            token = register()  # Register an account and get the token
            print(f"[!]" + Fore.BLUE + " Successfully got token .")
            print(f"[!]" + Fore.BLUE + " Getting proxies")

            get_proxy(token)
            i += 1  
    except Exception as e:
        print(f"An error occurred: {e}")
        token = register()  
