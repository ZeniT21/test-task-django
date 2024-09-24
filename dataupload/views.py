from django.shortcuts import render
import pandas as pd
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

data_frame = None


@csrf_exempt
def upload_file(request):
    global data_frame
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']
        if uploaded_file.name.endswith('.csv'):
            data_frame = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            data_frame = pd.read_excel(uploaded_file)
        else:
            return JsonResponse({"error": "Invalid file type."})
        return render(request, 'dataupload/display_data.html', {'data': data_frame.to_dict(orient='records')})

    return render(request, 'dataupload/upload.html')


def search_data(request):
    global data_frame
    query = request.GET.get('query', '')
    if data_frame is not None:
        result = data_frame[data_frame.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)]
        return JsonResponse({'data': result.to_dict(orient='records')})
    return JsonResponse({'data': []})