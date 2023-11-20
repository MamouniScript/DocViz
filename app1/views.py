from django.shortcuts import render, redirect
from .forms import FileUploadForm
import pandas as pd
import os
import matplotlib.pyplot as plt
from django.conf import settings

def upload_file(request):
    global df
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

            # Stocker les données dans la session
            request.session['column_names'] = df.columns.tolist()

            request.session['selected_column_name'] = request.POST.get('column_name')
            column_names = df.columns.tolist()


            # Rediriger vers la vue uploaded avec les noms de colonnes
            return redirect('uploaded')
    else:
        form = FileUploadForm()

    return render(request, 'upload_file.html', {'form': form})

def uploaded(request):

    # Récupérer les noms de colonnes depuis la session
    column_names = request.session.get('column_names', [])

    # Récupérer le nom de la colonne sélectionnée
    selected_column_name = request.POST.get('column_name')

    if selected_column_name is not None:
        # Récupérer les données de la colonne sélectionnée à partir du DataFrame d'origine
        selected_column_data = df[selected_column_name].tolist()  # Assurez-vous que df est accessible ici

        # Créer une série Pandas à partir des données
        column_series = pd.Series(selected_column_data)

        # Vérifier si la série n'est pas vide
        if not column_series.empty:
            # Générer un graphique à barres avec Pandas et Matplotlib
            plt.figure(figsize=(20, 6))
            column_series.value_counts().plot(kind='bar', color='skyblue')
            plt.title(f'Graphique de la colonne {selected_column_name}')
            plt.xlabel(f'Valeurs de la colonne {selected_column_name}')
            plt.ylabel('Fréquence')
            plt.xticks(rotation=50)
            plt.tight_layout()

            

            
            static_directory = os.path.join(settings.BASE_DIR, 'static')
            os.makedirs(static_directory, exist_ok=True)

            
            graph_file_path = os.path.join(static_directory, 'graphique.png')
            plt.savefig(graph_file_path)
            plt.close()

            return render(request, 'uploaded.html', {'column_names': column_names, 'selected_column_name': selected_column_name, 'graph_file_path': graph_file_path})


     # Récupérer les données depuis la session
    column_names = request.session.get('column_names', [])
    selected_column_name = request.session.get('selected_column_name', None)

    return render(request, 'uploaded.html', {'column_names': column_names, 'selected_column_name': selected_column_name})