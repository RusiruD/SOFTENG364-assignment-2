import pickle
import bcrypt
class userDetailsManager:

    def __init__(self, filename='user_details.pkl'):
        #Initialize the manager and automatically load the array from the file."""
        self.filename = filename
        self.array = self.load_array()  # Load the array on initialization
        
    def print_array(self):
        #Print the array.
        print(self.array)

    def add_user(self, username, password, login):
        #Add a username and password to the array as a sub-array and save it."""
        user_data = [username, password, login]  # Store both username and password as a list
        self.array.append(user_data)  # Append the sub-array to the main array
        self.save_array()  # Save immediately after adding the user
        print(f"Added user '{username}' to the file and saved.")
    def get_array_size(self):
        #Return the size of the array."""
        return len(self.array)
    
    def find_user(self, username, password):
        #Check if a username and password pair exists in the array."""
        self.array = self.load_array()  # Load the array on initialization

        for user_data in self.array:
            if user_data[0]==username:  # Check if the sub-array exists
                if bcrypt.checkpw(password, user_data[1]):
                    return True
        else:
            return False
    
    def is_logged_in(self, username):
        self.array = self.load_array()  # Load the array on initialization

        #Check if a user is logged in."""
        for user_data in self.array:
            if user_data[0] == username:
                return user_data[2]
        return False
    def set_login(self, username, login):
        #Set the login status of a user. 0 for not logged in, 1 for logged in.
        self.array = self.load_array()  # Load the array on initialization

        for user_data in self.array:
            if user_data[0] == username:
                user_data[2] = login
                
                self.save_array()
                return
            
        print(f"User '{username}' not found in the file.")

    def set_all_login(self, login):
        #Set the login status of all users."""
        self.array = self.load_array()
        for user_data in self.array:
            user_data[2] = login
        self.save_array()
        
    def find_username(self, username):
        self.array = self.load_array()  # Load the array on initialization

        #Check if a username exists in the array.
        for user_data in self.array:
            if user_data[0] == username:
                return True
        return False
    
    def save_array(self):
        #Pickle (save) the array to a file.
        with open(self.filename, 'wb') as f:
            pickle.dump(self.array, f)
        

    def load_array(self):
        #Load the array from the pickled file. If the file doesn't exist, return an empty list.
        try:
            with open(self.filename, 'rb') as f:
                array = pickle.load(f)
            return array
        except FileNotFoundError:
            return []

    def deletedata(self):
        #Clear the array and save the empty list.
        self.array.clear()
        self.save_array()
        print("Data deleted.")
    


  
