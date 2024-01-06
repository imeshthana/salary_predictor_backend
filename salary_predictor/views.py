from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import connection
import pickle
import json 
import joblib
import numpy as np

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def ml(request):
    data = json.loads(request.body.decode('utf-8'))
    
    # Job Title
    jobTitle = categorize_job_title(data.get('jobTitle'))
    #jobTitle = data.get('jobTitle')
    Data_Scientist = Data_Engineer = Data_Analyst = ML_Engineer = AI_Engineer = BI_BA_Engineer = Cloud_Engineer = Deep_Learning_Engineer = Others =0
    if(jobTitle == 'Data Scientist'):
        Data_Scientist = 1
    elif(jobTitle == 'Data Engineer'):
        Data_Engineer = 1
    elif(jobTitle == 'Data Analyst'):
        Data_Analyst = 1
    elif(jobTitle == 'ML Engineer'):
        ML_Engineer = 1
    elif(jobTitle == 'AI Engineer'):
        AI_Engineer = 1
    elif(jobTitle == 'BI/BA Engineer'):
        BI_BA_Engineer = 1
    elif(jobTitle == 'Cloud Engineer'):
        Cloud_Engineer = 1
    elif(jobTitle == 'Deep Learning Engineer'):
        Deep_Learning_Engineer = 1
    elif(jobTitle == 'Others'):
        Others = 1
    
    
    # Work Year
    y2022 = y2021 = y2020 = 0
    workYear = data.get('workYear')
    if workYear == '2023':
        y2022 = 1
    elif workYear == '2022':
        y2021 = 1
    elif workYear == '2021':
        y2020 = 1
     
     
    # Experience Level
    experienceLevel = data.get('experienceLevel')
    if(experienceLevel == 'EN'):
        experienceLevel = 1
    elif(experienceLevel == 'MI'):
        experienceLevel = 2
    elif(experienceLevel == 'SE'):
        experienceLevel = 3
    elif(experienceLevel == 'EX'):
        experienceLevel = 4
    
    # Employment Type
    employmentType = data.get('employmentType')
    if(employmentType == 'FT'):
        employmentType = 3
    elif(employmentType == 'PT'):
        employmentType = 2
    elif(employmentType == 'CT'):
        employmentType = 4
    elif(employmentType == 'FL'):
        employmentType = 1
        
        
    # Working Type
    workingType = data.get('workingType')
    if(workingType == '0'):
        workingType = 1
    elif(workingType == '50'):
        workingType = 2
    elif(workingType == '100'):
        workingType = 3
    
    
    # Company Size
    companySize = data.get('companySize')
    if(companySize == 'S'):
        companySize = 1
    elif(companySize == 'M'):
        companySize = 2
    elif(companySize == 'L'):
        companySize = 3
        
    
    # Salary Currency
    USD = GBP = EUR = INR = CAD = AUD = Other_currency = 0
    salaryCurrency = data.get('salaryCurrency')
    if(salaryCurrency == 'USD'):
        USD = 1
    elif(salaryCurrency == 'GBP'):
        GBP = 1
    elif(salaryCurrency == 'EUR'):
        EUR = 1
    elif(salaryCurrency == 'INR'):
        INR = 1
    elif(salaryCurrency == 'CAD'):
        CAD = 1
    elif(salaryCurrency == 'AUD'):
        AUD = 1
    elif(salaryCurrency == 'Other'):
        Other_currency = 1
    
    # Country
    US = GB = CA = ES = DE = IN = FR = Other_country = 0
    country = data.get('country')
    if(country == 'US'):
        US = 1
    elif(country == 'GB'):
        GB = 1
    elif(country == 'CA'):
        CA = 1
    elif(country == 'ES'):
        ES = 1
    elif(country == 'DE'):
        DE = 1
    elif(country == 'IN'):
        IN = 1
    else:
        Other_country = 1

    model = joblib.load(open('model/model.joblib', 'rb'))
    # model = pickle.load(open('model/model.pickle', 'rb'))
    
    result = model.predict([[0,
                             experienceLevel, 
                             employmentType, 
                             workingType, 
                             companySize, 
                             y2020, 
                             y2021, 
                             y2022, 
                             AI_Engineer,
                             BI_BA_Engineer,
                             Cloud_Engineer,
                             Data_Analyst,
                             Data_Engineer,
                             Data_Scientist,
                             ML_Engineer,
                             Others,
                             AUD,
                             CAD,
                             EUR,
                             GBP,
                             INR,
                             Other_currency,
                             USD,
                             CA,
                             DE,
                             ES,
                             FR,
                             GB,
                             IN,
                             Other_country,
                             US]])
    
    #print(jobTitle)
    # result_list = result.tolist()
    predicted_salary = np.exp(result)

    result_list = predicted_salary.tolist()
    
    return JsonResponse({'prediction': result_list[0]})
    

def categorize_job_title(job_title):
    category_mapping = {
        'Data Scientist': 'Data Scientist',
        'Data Science' : 'Data Scientist',
        'Data Engineer': 'Data Engineer',
        'Data Architect': 'Data Engineer',
        'Big Data Architect': 'Data Engineer',
        'Data Analyst': 'Data Analyst',
        'Head of Data': 'Data Analyst',
        'Data Analytic': 'Data Analyst',
        'Data Specialist': 'Data Analyst',
        'ETL Developer': 'Data Analyst',
        'Machine Learning': 'ML Engineer',
        'ML' : 'ML Engineer',
        'NLP Engineer' : 'ML Engineer',
        'AI': 'AI Engineer',
        'Business': 'BI/BA Engineer',
        'BI': 'BI/BA Engineer',
        'BA': 'BI/BA Engineer',
        'Cloud': 'Cloud Engineer',
        'Deep Learning': 'Deep Learning Engineer'
    }

    for keyword, category in category_mapping.items():
        if keyword.lower() in job_title.lower():
            return category

    return 'Others'
    
    

    