import geocoder

def get_current_location():
    g = geocoder.ip("me")  # Get location from IP address
    if g.latlng:
        return tuple(g.latlng)
    else:
        print("Error: Location not found")
        return None

# Get user location
current_location = get_current_location()
print(f"Your current location: {current_location}")
