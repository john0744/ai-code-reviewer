def check_user(user_list, target_user):
    # Intentional O(n) search inside a loop = O(n^2)
    # Gemini should suggest using a Set or Dictionary here!
    for user in user_list:
        if user == target_user:
            print("Found user!")
            
    # Intentional Security Risk
    api_key = "12345-ABCDE-SECRET-KEY" 
    print(f"Connecting with {api_key}")