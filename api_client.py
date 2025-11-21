# ============================================
# api_client.py
# ============================================

import requests

API_BASE = "http://127.0.0.1:8000"  # Make sure API is running

def call_square_root():
    try:
        value = int(input("Enter an integer: "))
        response = requests.get(f"{API_BASE}/sqrt", params={"value": value})
        result = response.json()   # Convert API response to dict automatically
        print("\nResponse:", result)
        print("\nResponse input:", result['input'])
        print("\nResponse square_root:", result['square_root'])
    except Exception as e:
        print("Error:", e)

def call_range_sum():
    try:
        from_param = int(input("Enter from_param: "))
        to_param = int(input("Enter to_param: "))
        response = requests.get(f"{API_BASE}/range_sum", params={"from_param": from_param, "to_param": to_param})
        result = response.json()
        print("\nResponse:", result)
        print("\nResponse from:", result['from'])
        print("\nResponse to:", result['to'])
        print("\nResponse sum:", result['sum'])
    except Exception as e:
        print("Error:", e)

def call_process_dict1():
    try:
        data = {}
        data["name"] = input("Enter your name: ")
        data["age"] = input("Enter your age: ")
        
        payload = {"data": data}
        response = requests.post(f"{API_BASE}/process_dict1", json=payload)
        result = response.json()
        
        print("\nResponse:", result)
        print("\nResponse name:", result['received_data']['data']['name'])
        print("\nResponse age:", result['received_data']['data']['age'])
    except Exception as e:
        print("Error:", e)

def call_process_dict2():
    try:
        data = {}
        data["name"] = input("Enter your name: ")
        data["age"] = input("Enter your age: ")
        
        payload = {"data": data}
        response = requests.post(f"{API_BASE}/process_dict2", json=payload)
        result = response.json()
        
        print("\nResponse:", result)
        print("\nResponse name:", result['received_data']['name'])
        print("\nResponse age:", result['received_data']['age'])
    except Exception as e:
        print("Error:", e)

def call_user_info():
    try:
        user_id = int(input("Enter user ID : "))
        response = requests.get(f"{API_BASE}/user", params={"user_id": user_id})
        result = response.json()
        print("\nResponse:", result)
    except Exception as e:
        print("Error:", e)

def menu():
    print("\n==============================")
    print("   API FUNCTION CONSOLE MENU  ")
    print("==============================")
    print("1. Get Square Root")
    print("2. Get Range Sum")
    print("3. Process Dictionary1")
    print("4. Process Dictionary2")
    print("5. Get User Info")
    print("6. Exit")
    print("==============================")

def main():
    while True:
        menu()
        choice = input("Enter your choice (1-6): ").strip()
        
        if choice == "1":
            call_square_root()
        elif choice == "2":
            call_range_sum()
        elif choice == "3":
            call_process_dict1()
        elif choice == "4":
            call_process_dict2()
        elif choice == "5":
            call_user_info()
        elif choice == "6":
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid option. Please choose between 1 and 6.")

if __name__ == "__main__":
    main()
