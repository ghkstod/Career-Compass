import importlib.metadata

def update_requirements_txt(file_path):

    # Open file_path and read each lines
    with open(file_path, 'r') as file:
        lines = file.readlines()

    #List to store the results
    results = []

    # Flag tio check if all packages are installed. If not False.
    all_installed = True


    for line in lines:
        if '==' in line:
            package_name = line.split('==')[0]
        else:
            package_name = line.strip()
        
        try:
            # check version of each package
            version = importlib.metadata.version(package_name)
            results.append(f'{package_name}=={version}\n')
            print(f'{package_name}=={version}')
        except importlib.metadata.PackageNotFoundError:
            all_installed = False
            print(f'Not installed: {package_name}')
    
    if all_installed == True:
        with open(file_path, 'w') as file:
            file.writelines(results)
        print('Updated Succesfully')
    else:
        print('Some packages are not installed. Therefore results are not updated.')

update_requirements_txt('./requirements.txt')