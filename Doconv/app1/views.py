from django.shortcuts import render, redirect
from .forms import FileUploadForm, VisualizationForm
import pandas as pd
import seaborn as sns
import os


def upload_file(request):
    column_names = request.session.get('column_names', [])

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

            print(column_names)
            request.session['column_names'] = df.columns.tolist()

            # Pass column choices to VisualizationForm
            form_visualization = VisualizationForm(column_choices=[(col, col) for col in column_names],
                                                   visualization_choices=[('histogram', 'Histogram'), ('bar', 'Bar Plot'), ('heatmap', 'Heatmap')])

            return render(request, 'uploaded.html', {'column_names': column_names, 'form_visualization': form_visualization})

    else:
        form = FileUploadForm()

    return render(request, 'upload_file.html', {'form': form})

def uploaded(request):
    column_names = request.session.get('column_names', [])

    if not column_names:
        return redirect('upload_file')

    if request.method == 'POST':
        print(request.POST)

    # Extract selected_column_name from the VisualizationForm
    selected_column_name = request.POST.get('selected_column_name', None)

    form_visualization = VisualizationForm(request.POST,
                                           column_choices=[(col, col) for col in column_names],
                                           visualization_choices=[('histogram', 'Histogram'), ('bar', 'Bar Plot'), ('heatmap', 'Heatmap')])

    if form_visualization.is_valid():
        visualization_type = form_visualization.cleaned_data['visualization_type']
        print("form passed")

        print(selected_column_name)
        print("¤¤**--")
        print(visualization_type)

        df_dict = request.session.get('uploaded_df', {})
        df = pd.DataFrame.from_dict(df_dict)

        temp_plot_path = generate_plot(df, selected_column_name, visualization_type)

        context = {'temp_plot_path': temp_plot_path, 'selected_column_name': selected_column_name, 'column_names': column_names}

        return render(request, 'visualization.html', context)

    context = {'column_names': column_names, 'form_visualization': form_visualization}
    return render(request, 'uploaded.html', context)



def generate_plot(df, column_name, visualization_type):
    plt.figure(figsize=(10, 6))
    
   # if visualization_type == 'line':
   #     sns.lineplot(x=df.index, y=df[column_name])
   #     plt.title(f'Line Plot for {column_name}')
   # elif visualization_type == 'scatter':
   #     sns.scatterplot(x=df.index, y=df[column_name])
   #     plt.title(f'Scatter Plot for {column_name}')
   # elif visualization_type == 'boxplot':
   #     sns.boxplot(x=df[column_name])
    #    plt.title(f'Boxplot for {column_name}')
    if visualization_type == 'histogram':
        sns.histplot(df[column_name], kde=False)
        plt.title(f'Histogram for {column_name}')
   # elif visualization_type == 'kde':
    #    sns.kdeplot(df[column_name], fill=True)
   #     plt.title(f'KDE Plot for {column_name}')
   # elif visualization_type == 'violin':
    #    sns.violinplot(x=df[column_name])
    #    plt.title(f'Violin Plot for {column_name}')
    elif visualization_type == 'bar':
        sns.barplot(x=df.index, y=df[column_name])
        plt.title(f'Bar Plot for {column_name}')
    elif visualization_type == 'heatmap':
        sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
        plt.title('Heatmap')
    else:
        raise ValueError(f'Unsupported visualization type: {visualization_type}')

    # Save the plot to a temporary file
    temp_plot_path = 'static/temp_plot.png'
    plt.savefig(temp_plot_path)
    plt.close()

    return temp_plot_path



def display_visualization(request):
    column_names = request.session.get('column_names', [])
    selected_column_name = request.session.get('selected_column_name', None)
    visualization_type = request.session.get('visualization_type', None)

    if not all([column_names, selected_column_name, visualization_type]):
        # Handle the case when some required data is missing
        return redirect('uploaded')

    # Process the DataFrame and generate the plot
    df = pd.DataFrame()  # Replace this with your actual DataFrame
    temp_plot_path = generate_plot(df, selected_column_name, visualization_type)

    # Pass the path to the generated plot to the template
    context = {'temp_plot_path': temp_plot_path}
    return render(request, 'visualization.html', context)

