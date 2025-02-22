class User:
    def __init__(self, ID, Name, Email, Mobile_Number, City, State, Pincode, Password, Is_Active=True):
        self.ID = ID
        self.Name = Name
        self.Email = Email
        self.Mobile_Number = Mobile_Number
        self.City = City
        self.State = State
        self.Pincode = Pincode
        self.Password = Password
        self.Is_Active = Is_Active
