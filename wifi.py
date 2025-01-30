import subprocess

def get_wifi_profiles():
    # Run the command to get Wi-Fi profiles
    profiles_data = subprocess.run(['netsh', 'wlan', 'show', 'profiles'], capture_output=True, text=True).stdout

    # Extract profile names
    profiles = []
    for line in profiles_data.split('\n'):
        if "All User Profile" in line:
            profile_name = line.split(":")[1].strip()
            profiles.append(profile_name)
    
    return profiles

def get_wifi_password(profile):
    # Run the command to get Wi-Fi details including the key
    profile_data = subprocess.run(
        ['netsh', 'wlan', 'show', 'profile', profile, 'key=clear'],
        capture_output=True, text=True
    ).stdout

    # Extract the password
    for line in profile_data.split('\n'):
        if "Key Content" in line:
            return line.split(":")[1].strip()
    
    return "No password found"

def main():
    # Get all Wi-Fi profiles
    profiles = get_wifi_profiles()
    if not profiles:
        print("No Wi-Fi profiles found.")
        return

    # Display the profiles and passwords
    print("Wi-Fi Profiles and Passwords:")
    for profile in profiles:
        password = get_wifi_password(profile)
        print(f"Profile: {profile}, Password: {password}")

if __name__ == "__main__":
    main()
