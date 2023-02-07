import pandas as pd
import pyautogui
from random import randint
import time

pd.options.mode.chained_assignment = None

def running(df):
    # get the event(log in or sign up)
    event = pyautogui.confirm("Log in or Sign up?","Start", ["Log in", "Sign up"])

    high_scores = list(df.high_score)
    passwords = list(df.password)
    names = list(df.name)
    succeed = 0
    stimes = []
    can_play = False


    # option for random password
    def random_password():
        r_password = randint(1000, 100000)
        while r_password in passwords:
            r_password = randint(1000, 100000)

        else:
            return r_password


    def get_time(password, event):
        seconds = time.time()
        current_time = time.ctime(seconds) # get the current time

        # updating the date
        if event == 'Log in':
            index = df.loc[df['password'] == password].index
            df['recent'].iloc[index] = current_time


        else:
            stimes.append(current_time)



    if event == "Log in":
        name = pyautogui.prompt("What is your name?", "Name") # get the user name
        password = pyautogui.password("Enter your password: ", "Password") # get the user password
        password = int(password) # change the password to int

        try:
            # check if the name and the password compatible with the users data
            if df.loc[df['password']==password, 'name'].iloc[0] == name:
                get_time(password, event)
                can_play = True


        except IndexError:
            pyautogui.alert("You were wrong with the password")

    else:
        name = pyautogui.prompt("What is your name?", "Name")

        # check if the name is taken
        while name in names:
            name = pyautogui.prompt("Your name already taken, Choose different name: ", "Name")
        else:
            names.append(name)
            succeed += 1

        #get whether he want to chose password by himself or receive random password
        option = pyautogui.confirm("Want to choose your password or random password?","Password", ["choose by myself", "random"])

        if option =="choose by myself":
            password = pyautogui.password("Choose your password:", "Password")
            password = int(password)
            # check if the password is taken or it too short
            while (password in passwords) or (len(str(password)) < 4):
                if password in passwords:
                    password = pyautogui.password(
                        "Your password already taken, Choose different password: (at least 4 numbers)", "Password")

                if len(str(password)) < 4:
                    password = pyautogui.password(
                        "Your password too short, Choose different password: (at least 4 numbers)", "Password")

                password = int(password)

            else:
                passwords.append(password)
                succeed += 1

        elif option == "random":
            password = random_password()
            passwords.append(password)
            pyautogui.alert(f"Your password is: {password}")
            succeed += 1


    # check if he put coorect name and password when he sign up
    if succeed == 2:
        high_scores.append(999) # append to high_score 999
        get_time(password, event)
        can_play = True


    times = [df["recent"].loc[i] for i, v in enumerate(df['recent'])]
    times.extend(stimes)

    # export the new data
    df = pd.DataFrame({'password':passwords, 'name':names, 'recent':times, 'high_score':high_scores})
    df.to_csv("UsersData.csv", index=False)

    if can_play:
        return event, name, password

    else:
        return 0,0,0


