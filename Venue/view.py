class ViewVenue:
    def show_venues(self, venues):
        print("Venues:")
        for venue in venues:
            print(
                f"ID: {venue[0]}, Name: {venue[1]}, Address: {venue[2]}, City: {venue[3]}, Capacity: {venue[4]} ")
            
    def get_venue_input(self):
        name = input("Input name: ")
        address = input("Input address: ")
        city = input("Input city: ")
        capacity = int(input("Input capacity: "))
        return name, address, city, capacity
    
    def get_venue_id(self):
        return int(input("Input venue ID: "))
    
    def show_venue_message(self, message):
        print(message)