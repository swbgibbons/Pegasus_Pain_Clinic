from tkinter import*
from tkinter import ttk
from datetime import datetime
from tkinter import messagebox
from Models import*
import re
import mysql.connector
from mysql.connector import Error


class Hospital_Mgmt_System:
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Management System")
        self.root.geometry("1540x800+0+0")
        self.Medication_Name = StringVar()
        self.Issue_Date = StringVar()
        self.Exp_Date = StringVar()
        self.Daily_Dose = StringVar()
        self.Side_FX = StringVar()
        self.Patient_Name = StringVar()
        self.DOB = StringVar()
        self.Original_Patient_Name = ""
        self.Original_Medication_Name = ""

        
        self.Hospital = Hospital("Pegasus Pain Clinic")
        self.Build_GUI()
        self.Fetch_Data()
        self.Medication_Doses = {
            "Morphine": 20,
            "Fentanyl": .002,
            "Acetaminophen": 750,
            "Vicodin": 10,
            "Percocet": 10,
            "Oxycodone": 10
        }


    def Build_GUI(self):

        Lbl_Title = Label(self.root, bd = 20, relief = RIDGE, text = self.Hospital.Name, fg = "Blue", bg = "white", font = ("Times New Roman", 50, "bold"))
        Lbl_Title.pack(side = TOP, fill = X)

        # =================================================================== Data frame============================================================================

        DataFrame = Frame(self.root, bd = 20, relief = RIDGE)
        DataFrame.place(x = 0, y = 130, width = 1530, height = 400)
        
        DataFrameLeft = LabelFrame(DataFrame, bd = 10, relief = RIDGE, padx = 10, font = ("Times New Roman", 12, "bold"), text = "Patient Information")
        DataFrameLeft.place(x = 0, y =5, width = 980, height = 350)
        DataFrameRight = LabelFrame(DataFrame, bd = 10, relief = RIDGE, padx = 10, font = ("Times New Roman", 12, "bold"), text = "Prescription")
        DataFrameRight.place(x = 990, y =5, width = 460, height = 350)
        # =================================================================== Buttons ============================================================================

        # Button frame not working for some
        ButtonFrame = Frame(self.root, bd = 20, relief = RIDGE)
        ButtonFrame.place(x = 0, y = 530, width = 1530, height = 70)

        # =================================================================== Details ============================================================================
        
        DetailsFrame = Frame(self.root, bd = 20, relief = RIDGE)
        DetailsFrame.place(x = 0, y = 600, width = 1530, height = 190)

        # =================================================================== DataFrame Left ============================================================================

        LblMedication = Label(DataFrameLeft, text = "Medication Name", font = ("Times New Roman", 12, "bold"), padx = 2, pady = 6)
        LblMedication.grid(row = 0, column = 0, sticky=W)

        ComNameMedication = ttk.Combobox(DataFrameLeft, textvariable = self.Medication_Name, state = "readonly", font = ("Times New Roman", 12, "bold"), width = 33)
        ComNameMedication['values'] = ("Morphine", "Fentanyl", "Acetaminophen", "Vicodin", "Percocet", "Oxycodone")
        ComNameMedication.current(0)
        ComNameMedication.grid(row = 0, column = 1)

        LblIssue_Date = Label(DataFrameLeft, font = ("arial", 12, "bold"), text = "Issue Date: ", padx = 2, pady = 6)
        LblIssue_Date.grid(row = 1, column = 0, sticky = W)
        TxtIssue_Date = Entry(DataFrameLeft, font = ("arial", 13, "bold"), width = 35, textvariable = self.Issue_Date)
        TxtIssue_Date.grid(row = 1, column = 1)

        LblExp_Date = Label(DataFrameLeft, font = ("arial", 12, "bold"), text = "Expiration Date: ", padx = 2, pady = 6)
        LblExp_Date.grid(row = 2, column = 0, sticky = W)
        TxtExp_Date = Entry(DataFrameLeft, font = ("arial", 13, "bold"), width = 35, textvariable = self.Exp_Date)
        TxtExp_Date.grid(row = 2, column = 1)

        LblDaily_Dose = Label(DataFrameLeft, font = ("arial", 12, "bold"), text = "Daily Dose: ", padx = 2, pady = 4)
        LblDaily_Dose.grid(row = 3, column = 0, sticky = W)
        TxtDaily_Dose = Entry(DataFrameLeft, font = ("arial", 13, "bold"), width = 35, textvariable = self.Daily_Dose)  # Fixed: was self.Side_FX
        TxtDaily_Dose.grid(row = 3, column = 1)

        # Added missing Side Effects field
        LblSide_FX = Label(DataFrameLeft, font = ("arial", 12, "bold"), text = "Side Effects: ", padx = 2, pady = 4)
        LblSide_FX.grid(row = 4, column = 0, sticky = W)
        TxtSide_FX = Entry(DataFrameLeft, font = ("arial", 13, "bold"), width = 35, textvariable = self.Side_FX)
        TxtSide_FX.grid(row = 4, column = 1)

        LblPatient_Name = Label(DataFrameLeft, font = ("arial", 12, "bold"), text = "Patient Name: ", padx = 2)
        LblPatient_Name.grid(row = 1, column = 2, sticky = W)
        TxtPatient_Name = Entry(DataFrameLeft, font = ("arial", 12, "bold"), width = 25, textvariable = self.Patient_Name)
        TxtPatient_Name.grid(row = 1, column = 3)

        LblDOB = Label(DataFrameLeft, font = ("arial", 12, "bold"), text = "Date of Birth: ", padx = 2, pady = 6)
        LblDOB.grid(row = 2, column = 2, sticky = W)
        TxtDOB = Entry(DataFrameLeft, font = ("arial", 12, "bold"), width = 25, textvariable = self.DOB)
        TxtDOB.grid(row = 2, column = 3)

        # ===========================================DataFrameRight ======================================================

        self.txtPrescription = Text(DataFrameRight, font = ("arial", 12, "bold"), width = 45)
        self.txtPrescription.grid(row = 0, column = 0)

        # ===========================================Buttons ======================================================

        # Fixed: Added command parameters to buttons
        Button_Prescription = Button(ButtonFrame, text = "Prescription", fg = "white", bg = "green", font = ("arial", 12, "bold"), width = 20, command = self.iPrescription)
        Button_Prescription.grid(row = 0, column = 0, padx = 5, pady = 5)

        Button_Prescription_Data = Button(ButtonFrame, text = "Prescription Entry ", bg = "green", fg = "white", font = ("arial", 12, "bold"), width = 20, command = self.iPrescription_Data)
        Button_Prescription_Data.grid(row = 0, column = 1, padx = 5, pady = 5)

        Button_Update = Button(ButtonFrame, text = "Update", bg = "green", fg = "white", font = ("arial", 12, "bold"), width = 20, command = self.Update_Data)
        Button_Update.grid(row = 0, column = 2, padx = 5, pady = 5)

        Button_Delete = Button(ButtonFrame, text = "Delete", bg = "green", fg = "white", font = ("arial", 12, "bold"), width = 20, command = self.Delete_Data)
        Button_Delete.grid(row = 0, column = 3, padx = 5, pady = 5)

        Button_Clear = Button(ButtonFrame, text = "Clear", bg = "green", fg = "white", font = ("arial", 12, "bold"), width = 20, command = self.Clear_Data)
        Button_Clear.grid(row = 0, column = 4, padx = 5, pady = 5)

        Button_Exit = Button(ButtonFrame, text = "Exit", bg = "green", fg = "white", font = ("arial", 12, "bold"), width = 20, command = self.Exit_App)
        Button_Exit.grid(row = 0, column = 5, padx = 5, pady = 5)

        # ===========================================Table ======================================================

        # ===========================================Scroll =======================================================
        scroll_x = ttk.Scrollbar(DetailsFrame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(DetailsFrame, orient=VERTICAL)
        self.hospital_table = ttk.Treeview(DetailsFrame, column = ("Medication Name", "Issue Date",
                                                                    "Expiration Date", "Daily Dose", "Side Effects", "Patient Name", 
                                                                    "DOB"), xscrollcommand = scroll_x.set, yscrollcommand = scroll_y.set) 
        scroll_x.pack(side = BOTTOM, fill = X)
        scroll_y.pack(side = RIGHT, fill = Y)
        scroll_x = ttk.Scrollbar(command=self.hospital_table.xview)
        scroll_y = ttk.Scrollbar(command=self.hospital_table.yview)


        # ===========================================Headings ======================================================

        self.hospital_table.heading("Medication Name", text = "Medication Name")
        self.hospital_table.heading("Issue Date", text = "Issue Date")
        self.hospital_table.heading("Expiration Date", text = "Exp. Date")
        self.hospital_table.heading("Daily Dose", text = "Daily Dosage")
        self.hospital_table.heading("Side Effects", text = "Side Effects")
        self.hospital_table.heading("Patient Name", text = "Patient Name")
        self.hospital_table.heading("DOB", text = "Date of Birth")

        self.hospital_table["show"] = "headings"
  
        self.hospital_table.column("Medication Name", width = 100)
        self.hospital_table.column("Issue Date", width = 100)
        self.hospital_table.column("Expiration Date", width = 100)
        self.hospital_table.column("Daily Dose", width = 100)
        self.hospital_table.column("Side Effects", width = 100)
        self.hospital_table.column("Patient Name", width = 100)
        self.hospital_table.column("DOB", width = 100)

        self.hospital_table.pack(fill = BOTH, expand = 1)
        # after some reasear
        self.hospital_table.bind("<ButtonRelease-1>", self.Get_Cursor)

        # ===========================================Functionality ======================================================
    def Validate_Date_Format(self, Date_Str):
        # data format put in try catch block to avoid complete crash
        # first if within try block returns none for empty strings

        try:
            if not Date_Str.strip():
                return None
            #returns valid (mm-dd-yyyy) format
            Valid_Date = datetime.strptime(Date_Str, "%m-%d-%Y")
            return Valid_Date
        # deleted the "as e" bc f string wasn't being used
        except ValueError:
            messagebox.showerror("Invalid date format. Please try again!")
        # deleted the if not block bc the first try block already catches the issue
        # deleted the extra try block bc it was redundant!

    def Valid_Exp_Date(self, Exp_Date_String):
        if not Exp_Date_String.strip():
            # went from True to none since string is empty
            return None
        Exp_Date_Obj = self.Validate_Date_Format(Exp_Date_String)
        if Exp_Date_Obj is None:
            messagebox.showerror("Invalid Date", "Must be in MM-DD-YYYY format")
            return False
    
        Exp_Date = Exp_Date_Obj.date()
        Today = datetime.today().date()

        if Exp_Date < Today:
            messagebox.showerror("Expired Medication. Cannot prescribe this medicaiton!")
            return False
        return True

    def Validate_Dose(self, Dose_String, Medication):
        # Dose validator works with the specific dosages that are listed in mg. 
        # Note fent is in micrograms, but converted to .002mg to make things simpler
        if not Dose_String.strip():
            messagebox.showerror("Dose is required!")
            return False
        # how does dose pattern work using this regex expression??
        #first d is for the number in front of decimal point
        # \. is for the decimal check, if there is one
        # third is for the value after the decimal
        Dose_Pattern = r'(\d+\.?\d*)'
        Match = re.search(Dose_Pattern, Dose_String.lower())
        if not Match:
            messagebox.showerror("Invalid Dose Format: Please enter a valid dose number")
            return False
        try:
            Dose_Value = float(Match.group(1))
        except ValueError:
            messagebox.showerror("Invalid Dose", "Please enter a valid numeric dose")
            return False
        # float('inf') will consider that the dose will be valid if med isn't listed
        Max_Dose = self.Medication_Doses.get(Medication, float('inf'))

        if Dose_Value > Max_Dose:
            messagebox.showerror("Dose too high", 
                                 f"Daily dose of {Dose_Value}mg exceeds the maximum safe dose"
                                 f"of {Max_Dose} for {Medication}")
            return False
        return True

    def Get_Database_Connection(self):
        # created a fxn to call the connection. decided to implement a more specific host since im using wsl terminal

        try:
            Conn = mysql.connector.connect(user = "root", host = "127.0.0.1", 
                                           database = "ppc", password = "HoneyMuffinz93", connection_timeout = 5)
            return Conn
        except Error as e:
            messagebox.showerror("Database Error",  f"Error connecting to database: {str(e)}")

    
    def Convert_Date_Format(self, date_str):
        """Convert mm-dd-yyy to yyyy-mm-dd for MySQL"""
        if not date_str.strip():
            return None
        try:
            # this is meant to properly display the value for mysql
            # this is necessary to input values into mysql..
            date_obj = datetime.strptime(date_str, "%m-%d-%Y")
            return date_obj.strftime("%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Date Error", f"Invalid date format: {date_str}. Use MM-DD-YYYY format")
            return None
        

    def Convert_Date_Display(self, mysql_date):
        """Convert YYY-MM-DD to MM-DD-YYYY for display"""
        if not mysql_date:
            return ""
        try:
            #isinstance is a method call to refer mysql_date object as a string
            if isinstance(mysql_date, str):
                date_obj = datetime.strptime(mysql_date, "%Y-%m-%d")
            else:
                date_obj =  mysql_date
            return date_obj.strftime("%m-%d-%Y")
        except (ValueError, AttributeError):
            return str(mysql_date)
                    
                # strips the traditional date format and returns mm-dd-yyyy format
                # returns as string
			

    def iPrescription_Data(self):
        if self.Medication_Name.get() == "" or self.Exp_Date.get() == "":
            messagebox.showerror("Error", "Fill out required fields")

        else:
            try:
                # how come this convert date format isnt registering?
                MySQL_Issue_Date = self.Convert_Date_Format(self.Issue_Date.get())
                MySQL_Exp_Date = self.Convert_Date_Format(self.Exp_Date.get())
                MySQL_DOB = self.Convert_Date_Format(self.DOB.get())
                
                if MySQL_Issue_Date is None or MySQL_Exp_Date is None or MySQL_DOB is None:
                    return 

                # validates the data
                if not self.Valid_Exp_Date(self.Exp_Date.get()):
                    return
                if not self.Validate_Dose(self.Daily_Dose.get(), self.Medication_Name.get()):
                    return
                Conn = self.Get_Database_Connection()
                if Conn is None:
                    return

                Cursor = Conn.cursor()

                # convert the str to date values before putting them into insert query
                # this was already accomplished when i created them within the intial try block

                Insert_Query = """INSERT INTO hospital_table (Medication_Name, Issue_Date, Exp_Date, Daily_Dose, Side_FX, Patient_Name, DOB)
                                VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                Data = (
                    self.Medication_Name.get(), 
                    MySQL_Issue_Date, 
                    MySQL_Exp_Date, 
                    self.Daily_Dose.get(), 
                    self.Side_FX.get(), 
                    self.Patient_Name.get(), 
                    MySQL_DOB
                    )

                Cursor.execute(Insert_Query, Data)
                Conn.commit()

                messagebox.showinfo("Success", "Record has been inserted successfully")
                self.Fetch_Data()  # Refresh the table after inserting
                self.Clear_Data()  # Clear the form after successful insert
            except Error as e:
                messagebox.showerror("Error", f"Error occurred: {str(e)}")


    def iPrescription(self):
        # Generate prescription text
        self.txtPrescription.delete(1.0, END)
        self.txtPrescription.insert(END, "Patient Name:\t\t" + self.Patient_Name.get() + "\n")
        self.txtPrescription.insert(END, "Date of Birth:\t\t" + self.DOB.get() + "\n")
        self.txtPrescription.insert(END, "Medication Name:\t\t" + self.Medication_Name.get() + "\n")
        self.txtPrescription.insert(END, "Issue Date:\t\t" + self.Issue_Date.get() + "\n")
        self.txtPrescription.insert(END, "Expiration Date:\t\t" + self.Exp_Date.get() + "\n")
        self.txtPrescription.insert(END, "Daily Dose:\t\t" + self.Daily_Dose.get() + "\n")
        self.txtPrescription.insert(END, "Side Effects:\t\t" + self.Side_FX.get() + "\n")

    def Fetch_Data(self):
        # fetch data with execute method to get all data to work with later
        try:
            Conn = self.Get_Database_Connection()
            if Conn is None:
                return
            Cursor = Conn.cursor()
            Cursor.execute("SELECT Medication_Name, Issue_Date, Exp_Date, Daily_Dose, Side_FX, Patient_Name, DOB FROM hospital_table")
            Rows = Cursor.fetchall()
            self.hospital_table.delete(*self.hospital_table.get_children())
            for r in Rows:
                Medication_name = r[0]
                Issue_Date = self.Convert_Date_Display(r[1])
                Exp_Date = self.Convert_Date_Display(r[2])
                Daily_Dose = r[3]
                Side_FX = r[4]
                Patient_Name = r[5]
                DOB = self.Convert_Date_Display(r[6])

                self.hospital_table.insert('', END, values = (Medication_name, Issue_Date, Exp_Date, 
                                                              Daily_Dose, Side_FX, Patient_Name, DOB))


        except Error as e:
            messagebox.showerror("Database Error", f"Error fetching data: {str(e)}")
        finally:
            if Conn and Conn.is_connected():
                Cursor.close()
                Conn.close()

    def Get_Cursor(self, event):
        Cursor_Row = self.hospital_table.focus()
        Content = self.hospital_table.item(Cursor_Row)
        Row = Content['values']
        if Row:

            self.Original_Patient_Name = Row[5]
            self.Original_Medication_Name = Row[0]

            self.Medication_Name.set(Row[0])
            self.Issue_Date.set(Row[1])
            self.Exp_Date.set(Row[2])
            self.Daily_Dose.set(Row[3])
            self.Side_FX.set(Row[4])
            self.Patient_Name.set(Row[5])
            self.DOB.set(Row[6])

    def Clear_Data(self):
        self.Medication_Name.set("")
        self.Issue_Date.set("")
        self.Exp_Date.set("")
        self.Daily_Dose.set("")
        self.Side_FX.set("")
        self.Patient_Name.set("")
        self.DOB.set("")
        self.txtPrescription.delete(1.0, END)

        self.Original_Patient_Name = ""
        self.Original_Medication_Name = ""

    def Update_Data(self):
        if self.Medication_Name.get() == "" or self.Exp_Date.get() == "":
            messagebox.showerror("Error", "Must fill out all required fields")
            return
        if not self.Original_Medication_Name or not self.Original_Patient_Name:
            return
        if not self.Valid_Exp_Date(self.Exp_Date.get()):
            return
        if not self.Validate_Dose(self.Daily_Dose.get(), self.Medication_Name.get()):
            return

        try:
            MySQL_Issue_Date = self.Convert_Date_Format(self.Issue_Date.get())
            MySQL_Exp_Date = self.Convert_Date_Format(self.Exp_Date.get())
            MySQL_DOB = self.Convert_Date_Format(self.DOB.get())

            if MySQL_Issue_Date is None or MySQL_Exp_Date is None or MySQL_DOB is None:
                return

            Conn = self.Get_Database_Connection()
            if Conn is None:
                return
            Cursor = Conn.cursor()

            Update_Query = """UPDATE hospital_table SET Medication_Name = %s, Issue_Date = %s, Exp_Date = %s, Daily_Dose = %s, Side_FX = %s, DOB = %s
                            WHERE Patient_Name = %s AND Medication_Name = %s"""
            Data = (self.Medication_Name.get(), MySQL_Issue_Date, MySQL_Exp_Date, self.Daily_Dose.get(), self.Side_FX.get(), MySQL_DOB, self.Patient_Name.get(), self.Medication_Name.get())
            Cursor.execute(Update_Query, Data)
            Conn.commit()

            if Cursor.rowcount > 0:
                messagebox.showinfo("Success", "Record updated successfully!")
                self.Original_Patient_Name = self.Patient_Name.get()
                self.Original_Medication_Name = self.Medication_Name.get()
                self.Fetch_Data()
                self.Clear_Data()
            else:
                messagebox.showwarning("Warning!", "No record found to delete.")
        except Error as e:
            messagebox.showerror("Database Error", f"Error updating data: {str(e)}")
        finally:
            if Conn and Conn.is_connected():
                Cursor.close()
                Conn.close()

    def Delete_Data(self):
        if self.Medication_Name.get() == "" or self.Exp_Date.get() == "":
            messagebox.showerror("Error", "Must fill out all required fields")
            return
        Result = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the record for {self.Patient_Name.get()}?")
        if not Result:
            return
        try:
            Conn = self.Get_Database_Connection()
            if Conn is None:
                return
            Cursor = Conn.cursor()
            Delete_Query = "DELETE FROM hospital_table WHERE patient_name = %s AND medication_name = %s"
            Cursor.execute(Delete_Query, (self.Patient_Name.get(), self.Medication_Name.get()))
            Conn.commit()

            if Cursor.rowcount > 0:
                messagebox.showinfo("Success", "Record deleted successfully")
                self.Fetch_Data()
                self.Clear_Data()
            else:
                messagebox.showwarning("Warning", "No record found to delete")
        except Error as e:
            messagebox.showerror("Database Error", f"Error deleting data: {str(e)}")
        finally:
            if Conn and Conn.is_connected():
                Cursor.close()
                Conn.close()

    def Exit_App(self):
        Result = messagebox.askyesno("Exit", "Are you sure you want to exit?")
        if Result:
            self.root.destroy()
if __name__ == "__main__":
    root = Tk()
    ob = Hospital_Mgmt_System(root)
    root.mainloop()
    