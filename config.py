# config.py

system_prompt = """
You are tasked with extracting and organizing personal, academic, and employment information from candidate resumes. Your goal is to identify relevant details and categorize them into sections such as personal information, educational background, skills, and employment history.
Give all dates in dd/MM/yyyy format.
Stick to the given json template only.
Ensure the output is structured clearly, suitable for further processing in recruitment workflows, and always include the WorkedPeriod calculation, ensuring accuracy.
"""

user_prompt = "User is requesting to extract the following details from the resume text:"

json_template = {
    "Address": [
        {
            "City": "",
            "Country": "",
            "CountryCode": "",
            "State": "",
            "Street": "",
            "AddressType": "",
            "ZipCode": ""
        }
    ],
    "PersonalDetails": {
        "Name": {"FirstName": "", "LastName": "", "MiddleName": "", "FullName": "", "TitleName": ""},
        "FatherName": "",
        "MotherName": "",
        "DateOfBirth": "",
        "Mobile": [],
        "Email": [],
        "Nationality": "",
        "MaritalStatus": "",
        "PanNo": "",
        "PassportDetail": {
            "DateofExpiry": "",
            "DateOfIssue": "",
            "PassportNumber": "",
            "PlaceOfIssue": ""
        }
    },
    "LanguageKnown": [],
    "Academics": [
        {
            "Degree": "",
            "StartDate": "",
            "EndDate": "",
            "Institute": "",
            "Score": ""
        }
    ],
    "CurrentEmployer": "",
    "CurrentSalary": "",
    "ExpectedSalary": "",
    "WorkedPeriod": {"TotalExperienceInMonths": "", "TotalExperienceInYear": "",
                     "TotalExperienceRange": ""},
    "Skills": [],
    "WorkExperience": [
        {
            "Organization": "",
            "StartDate": "",
            "EndDate": "",
            "Designation": "",
            "Projects": [
                {
                    "Project Name": "",
                    "Project Start": "",
                    "Project End": "",
                    "Project Objective": "",
                    "Skills Involved": ""
                }
            ],
            "Last Salary": "",
            "Total Time Spent": ""
        }
    ],
    "Objective": ""
}

OPENAI_API_KEY='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

