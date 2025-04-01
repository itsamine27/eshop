import requests

def CallNewProdApi(request, form, formset):
    base_url=request.get_host()
        
        # Construct the URL using the company_id parameter.
    url = f"{base_url}/api/company/products/"
    payload = {
        "product_name": form.cleaned_data['product_name'],
        "product_description": form.cleaned_data['product_description'],
        "product_quantity": form.cleaned_data['product_quantity'],
        "product_price": form.cleaned_data['product_price'],
        "product_discount": form.cleaned_data['product_discount'],
        
        "product_images": [
            {
            "product_image": "https://static.nike.com/a/images/c_limit,w_592,f_auto/t_product_v1/49545dac-67b5-4c49-b82f-83dcd07b375a/pegasus-41-electric-road-running-shoes-sLBdkL.png"
            }
        ],
        "product_rating": [
        ]
    }
        # Make the POST request; the JSON payload is automatically serialized.
    response = requests.post(url, json=payload)
        


