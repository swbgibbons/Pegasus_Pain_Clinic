class Hospital:
    def __init__(self, Name = "Pegasus Pain Clinic"):
        self.Name = Name
    
class Patient:
    def __init__(self, Name, DOB):
        self.Name = Name
        self.DOB = DOB

class Prescription:
    def __init__(self, Medication_Name, Issue_Date, Exp_Date, Daily_Dose, Side_FX):
        self.Medication_Name = Medication_Name
        self.Issue_Date = Issue_Date
        self.Exp_Date = Exp_Date
        self.Daily_Dose = Daily_Dose
        self.Side_FX = Side_FX
