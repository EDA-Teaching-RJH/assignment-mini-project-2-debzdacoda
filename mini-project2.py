import re
import csv
import unittest 

#Reading Files(file I/O)
def import_passwords_csv(filepath):
    passwords = set()
    try:
        with open(filepath, 'r') as file:
            reader= csv.read(file)
    except FileNotFoundError:
        print(f"CSV file{filepath} not found.")
    return passwords

#Writing and saving feedback in file
def upload_feedback(feedback, filepath): 
    try:
        with open(filepath, 'w') as file:
            for suggestion in feedback:
                file.write(suggestion + "\n")
        print(f"Saving feedback to{filepath}")  
    except Exception as e:
        print(f"Error found when saving feedback: {e}")


#To Analyse the composition of the password and check its validity
class PasswordEvaluater:

    def __init__(self, password_file):
        self.passwords = import_passwords_csv(password_file)

    def evaluate_password_strength(self,password):

        pasword_grading = 0
        feedback = []

        #check for special characters
        if re.search(r'[!@#£&*()"%:.,€$¥_^{}|<>]',password):
            password_grading += 1
        else:
            feedback.append("Password must include at least one special character")
        
        #check for variability in case of the letters
        if re.search(r'[A-Z]',password):
            password_grading += 1
        else:
            feedback.append("Password must have at least 1 uppercase")
        if re.search(r'[a-z]',password):
            password_grading += 1
        else:
            feedback.append("Password must have at least 1 lowercase letter")
        
        #Length check
        if len(password) >= 8:
            password_grading += 1
        else:
            feedback.append("Password character count should be a minimum of 8 characters")

        if password in self.passwords:
            feedback.append("Alert!Do not use weak passwords")
        else:
            password_grading += 1

        grade = {5: "Very Strong", 4: "Strong", 3: "Moderate", 2: "Weak", 1:"Very Weak"}
        return grade.get(password_grading,"Invalid"), feedback

    #test code 

    class test_code_for_password_evaluater(unittest.Testcase):
        def setUp(self):
            self.evaluate = PasswordEvaluater("password.csv")

        def test_strong_password(self):
            self.assertEqual(self.evaluate.evaluate_strength("Million£123"),("Very Strong",[]))

        def test_short_password(self):
            grade,feedback = self.evaluate.evaluate_strength("Abc#123")
            self.assertEqual(grade, "Weak")
            self.assertIn("Password charcter count should be a minimum of 8 characters", feedback)

        def test_missing_uppercase(self):
            grade,feedback = self.evaluate.evaluate_strength("lowercase@1")
            self.assertEqual(grade, "Moderate")
            self.assertIn("Password must have at least 1 uppercase")

    #main function
    if __name__ == "__main__":

        password_file = passwords.csv
        evaluate = PasswordEvaluater("passwords_file")

        new_user_password = input("Create new password:  ")
        grade, feedback = evaluate.evaluate_password_strength(new_user_password)

        print(f"Password Strength grade: {grade}")
        if feedback:
            print("Suggestions:")
            for suggestion in feedback:
                print(f"- {suggestion}")

            upload_feedback(feedback, "new_password_feedback.txt")

        unittest.main()

