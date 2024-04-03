import pandas as pd
from django.shortcuts import render
from missing_data.models import Person


def home(request):
    return render(request, 'charts.html')

def jupyter_notebook(request):
    return render(request, 'HongProject.html')


def median_substitute(request):
    return render(request, 'median_substitute.html')


def mean_substitute(request):
    #top 10 records
    persons = Person.objects.all()[:10]
    return render(request, 'mean_substitute.html', {'persons': persons})


def mode_substitute(request):
    return render(request, 'mode_substitute.html')


def ml_substitute(request):
    return render(request, 'ml_substitute.html')


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
