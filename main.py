if __name__ == "__main__":
    user_name = input("Enter the Hexas ID: ").strip()
    password = input("Enter the Password: ").strip()
    start_time = input("Enter the starting time(HH:MM AM/PM): ").strip()
    end_time = input("Enter the ending time(HH:MM AM/PM): ").strip()
    priority = input("Enter the priority(start|middle|end): ").strip().lower()
    
    # To avoid showing debuging message while entering above inputs 
    # import statements are moved down here.
    from bot import login
    from bot import register_for_listening
    from bot import register_for_speaking
    from bot import register_for_reading
    from bot import register_for_writing

    login(user_name, password)
    #comment out the unnecessary registration
    register_for_listening(start_time, end_time, priority, password)
    register_for_speaking(start_time, end_time, priority, password)
    register_for_reading(start_time, end_time, priority, password)
    register_for_writing(start_time, end_time, priority, password)


"""
HZ15365
AS65
01:00 AM
01:00 PM
end
"""
