import pandas as pd
from django.shortcuts import render
from missing_data.models import Person
from django.db.models import Avg


def home(request):
    # Assuming 'age' is a field in your Person model
    age_distribution = {
        'under_18': Person.objects.filter(age__lt=18).count(),
        'age_18_24': Person.objects.filter(age__gte=18, age__lte=24).count(),
        'age_25_34': Person.objects.filter(age__gte=25, age__lte=34).count(),
        'age_35_44': Person.objects.filter(age__gte=35, age__lte=44).count(),
        'age_45_54': Person.objects.filter(age__gte=45, age__lte=54).count(),
        'age_55_64': Person.objects.filter(age__gte=55, age__lte=64).count(),
        'over_65': Person.objects.filter(age__gt=65).count(),
    }

    marital_status = {
        'single': Person.objects.filter(marital_status__iexact='Single').count(),
        'married': Person.objects.filter(marital_status__iexact='Married').count(),
    }

    education_level = {
        'high_school': Person.objects.filter(education__iexact='High School').count(),
        'bachelor': Person.objects.filter(education__iexact='Bachelor\'s').count(),
        'masters': Person.objects.filter(education__iexact='Master\'s').count(),
        'doctorate': Person.objects.filter(education__iexact='Doctorate').count(),
    }

    # Define a list of the occupations you're interested in
    occupations = [
        'Digital Marketing', 'Software Engineer', 'Finance', 'Sales',
        'Teacher', 'Operations', 'Marketing', 'Construction',
        'Data Analyst', 'Software Developer', 'HR', 'Engineer'
    ]

    # Initialize a dictionary to hold average ratings by occupation
    product_rating_by_occupation = {}

    # Calculate the average product rating for each occupation
    for occupation in occupations:
        average_rating = Person.objects.filter(
            occupation__iexact=occupation
        ).aggregate(
            Avg('product_rating')
        )['product_rating__avg']

        # Ensure occupation keys match the format in your JavaScript snippet
        occupation_key = occupation.lower().replace(" ", "_")
        product_rating_by_occupation[occupation_key] = average_rating or 0  # Use 0 or a suitable default if no rating

    return render(request, 'charts.html', {
        'age_distribution': age_distribution,
        'education_level': education_level,
        'product_rating_by_occupation': product_rating_by_occupation,
        'marital_status': marital_status
    })

def jupyter_notebook(request):
    return render(request, 'HongProject.html')


def median_substitute(request):
    # top 10 records
    persons = Person.objects.all()[:10]
    return render(request, 'median_substitute.html', {'persons': persons})


def mean_substitute(request):
    #top 10 records
    persons = Person.objects.all()[:10]
    return render(request, 'mean_substitute.html', {'persons': persons})


def mode_substitute(request):
    # top 10 records
    persons = Person.objects.all()[:10]
    return render(request, 'mode_substitute.html', {'persons': persons})


def ml_substitute(request):
    # top 10 records
    persons = Person.objects.all()[:10]
    return render(request, 'ml_substitute.html', {'persons': persons})


def dev(request):
    if request.method == "POST":
        file = request.FILES['csvfile']
        auth_code = request.POST.get('auth')

        # Ensure pandas reads the file correctly in the context of Django file upload
        df = pd.read_csv(file)

        # Expected columns
        expected_cols = ['CustomerID', 'Gender', 'Age', 'Education', 'Occupation', 'MaritalStatus', 'ProductRating']

        # Validate header
        if not all(col in df.columns for col in expected_cols):
            # If the headers do not match exactly what we expect, return an error
            print("Invalid column names")
            return render(request, 'development.html', {'error': 'Invalid column names'})

        # Lambda functions for each field
        convert_int = lambda x: None if pd.isna(x) or x == '' else int(x)
        convert_float = lambda x: None if pd.isna(x) or x == '' else float(x)
        convert_str = lambda x: None if pd.isna(x) or x == '' else x

        # If the file is valid, process each row
        for index, row in df.iterrows():
            person = Person(
                customer_id=convert_int(row['CustomerID']),
                gender=convert_str(row['Gender']),
                age=convert_int(row['Age']),
                education=convert_str(row['Education']),
                occupation=convert_str(row['Occupation']),
                marital_status=convert_str(row['MaritalStatus']),
                product_rating=convert_float(row['ProductRating'])
            )
            if auth_code == 'markcanada':
                person.save()



    else:
        print("No file found")

    persons = Person.objects.all()  # Fetch all Person objects from the database
    return render(request, 'development.html', {'persons': persons})
