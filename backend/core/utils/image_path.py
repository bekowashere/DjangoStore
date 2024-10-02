# ACCOUNT
def upload_person_portrait(instance, filename):
    filebase, extension = filename.rsplit(".")
    return f'account/user/person/portrait/{instance.number}.{extension}'

def upload_person_credentials(instance, filename):
    filebase, extension = filename.rsplit(".")
    return f'account/user/person/credentials/{instance.number}.{extension}'

# PRODUCT
def upload_category_background_image(instance, filename):
    filebase, extension = filename.rsplit(".")
    return f'product/categories/{instance.slug}.{extension}'
    
