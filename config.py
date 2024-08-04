# config.py

system_prompt = "You are tasked with acting as a resume parser to extract personal, academic, and employment information from candidate resumes. Your goal is to accurately identify and organize relevant details from the resumes provided. Your output should include clear categorization of the extracted information, ensuring that personal details, educational background, and employment history are properly structured for further processing."

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
        "DOB": "",
        "Mobile": [],
        "Email": [],
        "Nationality": "",
        "MaritalStatus": "",
        "PanNo": "",
        "PassportDetail": {
            "DateofExpiry": "",
            "DateOfIssue": "",
            "PassposrtNumber": "",
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
            "Orgnization": "",
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

OPENAI_API_KEY='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
