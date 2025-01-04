class ViewFacility:
    def show_facility(self, facilities):
        print("Facilities:")
        for facility in facilities:
            print(
                f"Facility ID: {facility[0]},Venue ID: {facility[1]}, Name: {facility[2]}, Type: {facility[3]} ")
            
    def get_facility_input(self):
        facility_name = input("Input facility name: ")
        facility_type = input("Input facility type: ")
        venue_id = int(input("Input Venue ID: "))
        return facility_name, facility_type, venue_id
    
    def get_facility_id(self):
        return int(input("Input Facility ID: "))
    
    def show_facility_message(self, message):
        print(message)