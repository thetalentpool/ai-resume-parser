# config.py

system_prompt = """
You are tasked with extracting and organizing personal, academic, and employment information from candidate resumes. Your goal is to identify relevant details and categorize them into sections such as personal information, educational background, skills, and employment history.
Give all dates in dd/MM/yyyy format, especially the StartDate and EndDate fields of Academics and WorkExperience.
In dates, if just year is mentioned then consider it to be the last day of the year in EndDate and first day of the year in StartDate.
In dates, if year and month is mentioned then consider it to be the last day of that month in EndDate and first day of that month in StartDate.
Stick to the given json template only.
Provide the output as valid JSON. Do not include any markdown formatting, such as triple backticks or other extra characters. Respond with only the JSON content.
"""

# Ensure the output is structured clearly, suitable for further processing in recruitment workflows, and always include the WorkedPeriod calculation, ensuring accuracy.
# """

# system_prompt = """
# You are tasked with extracting and organizing personal, academic, and employment information from candidate resumes. Your goal is to identify relevant details and categorize them into sections such as personal information, educational background, skills, and employment history.
# Give all dates in dd/MM/yyyy format
# Stick to the given json template only.
# Provide the output as valid JSON. Do not include any markdown formatting, such as triple backticks or other extra characters. Respond with only the JSON content.
# """

user_prompt = "User is requesting to extract the following details from the resume text:"

json_template_old = {
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

json_template = {
    "City": "",
    "PersonalDetails": {
        "Name": {"FirstName": "", "LastName": "", "MiddleName": "", "FullName": "", "TitleName": ""},
        "DateOfBirth": "",
        "Mobile": [],
        "Email": [],
        "Nationality": ""
    },
    "Academics": [
        {
            "Degree": "",
            "Branch": "",
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
            "Designation": ""
        }
    ]
}

OPENAI_API_KEY='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
IMAGE_API_KEY='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

