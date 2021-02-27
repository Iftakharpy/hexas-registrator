from bot import Bot
import threading

default_delimeter = ','


def make_creedential_tuples(user_names, passwords, delimeter=','):
    # parse usernames
    user_names = user_names.split(delimeter)
    user_names = map(lambda user_name: user_name.strip().upper(),
                    user_names)
    # parse passwords
    passwords = passwords.split(delimeter)
    passwords = map(lambda password: password.strip().upper(),
                    passwords)
    return zip(user_names, passwords)

def register_for_exam(*args, **kwargs):
    bot = Bot(*args, **kwargs)

def main(credential_iterator, start_time='10:00 AM', end_time='05:00 PM', priority='middle', register_for='speaking'):
    threads = []
    # preparing threads
    for creed in credential_iterator:
        thread = threading.Thread(target=register_for_exam, args=(*creed, start_time, end_time, priority, register_for), daemon=True)
        threads.append(thread)
    
    # starting threads
    for th in threads:
        th.start()
    
    # waiting for threads to finish
    for th in threads:
        th.join()


if __name__ == "__main__":
    delimeter = input(f"Enter separator delimeter(defalut='{default_delimeter}'): ").strip()
    if not delimeter:
        delimeter = default_delimeter
    user_names = input(f"Enter the Hexas IDs(delimeter={delimeter}): ").strip()
    passwords = input(f"Enter the Passwords(delimeter={delimeter}): ").strip()
    start_time = input("Enter the starting time(HH:MM AM/PM): ").strip()
    end_time = input("Enter the ending time(HH:MM AM/PM): ").strip()
    priority = input("Enter the priority(start|middle|end): ").strip().lower()
    register_for = input("Enter the module(listening|speaking|reading|writing) you want to register for: ").strip().lower()

    credentials = make_creedential_tuples(user_names, passwords)
    main(credentials, start_time, end_time, priority, register_for)
    

"""
Delimeter: ,
IDs: HZ15626, HZ15365, HZ15698, HZ15625, HZ15629
Passwords: AS26, AS65, AS98, AS25, AS29
Start: 09:00 AM
End: 05:00 PM
Priority: middle
Register for: speaking

,
HZ15626, HZ15365, HZ15698, HZ15625, HZ15629
AS26, AS65, AS98, AS25, AS29
09:00 AM
05:00 PM
middle
speaking

,
HZ15626, HZ15365
AS26, AS65
09:00 AM
05:00 PM
middle
speaking
"""
