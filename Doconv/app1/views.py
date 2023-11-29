from django.shortcuts import render, redirect
from .forms import FileUploadForm
import pandas as pd
import os

def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()


            file_extension = instance.file.name.split('.')[-1].lower()
            if file_extension == 'csv':
                df = pd.read_csv(instance.file, delimiter=',')
            elif file_extension == 'json':
                df = pd.read_json(instance.file)
            elif file_extension == 'xlsx':
                df = pd.read_excel(instance.file)
            else:
                os.remove(instance.file.path)  
                return redirect('uploaded')

            column_names = df.columns.tolist()


            selected_column_name = request.POST.get('column_name')

            if selected_column_name is None:
                print("Column name not provided in the POST data.")
                return redirect('uploaded')  

            print(df[selected_column_name])

            context = {'column_names': column_names, 'selected_column_name': selected_column_name}

            return render(request, 'upload_file.html', context)  
    else:
        form = FileUploadForm()

    return render(request, 'upload_file.html', {'form': form})



def uploaded(request):
    return render(request, 'uploaded.html')