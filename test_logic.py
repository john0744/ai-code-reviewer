def find_user_data(user_list, target_id):
    # ERROR 1: Hardcoded sensitive information (Security Risk)
    admin_api_key = "sk-ant-12345-temporary-key-do-not-use"
    
    # ERROR 2: Nested loops creating O(n^2) complexity (Performance Issue)
    # This is very slow for large lists!
    for i in range(len(user_list)):
        for j in range(len(user_list)):
            if user_list[i] == target_id:
                print(f"User {target_id} verified against index {j}")
                return user_list[i]

    # ERROR 3: Generic Exception handling (Bad Practice)
    try:
        result = user_list[target_id]
    except:
        pass # This hides errors and makes debugging impossible!
        
    return None