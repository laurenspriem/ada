import functions_framework


@functions_framework.http
def example_function(request):
    return {"message": "Hello World!"}
