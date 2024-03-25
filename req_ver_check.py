import importlib.metadata

def update_requirements_txt(file_path):
    """
    주어진 경로의 requirements.txt 파일을 읽어 각 패키지의 현재 설치된 버전으로 업데이트합니다.

    requirements.txt 파일의 각 줄을 읽어 해당 패키지가 시스템에 설치되어 있는 경우,
    해당 패키지의 현재 버전으로 업데이트합니다. 만약 파일 내 일부 패키지가 설치되어 있지 않은 경우,
    업데이트는 수행되지 않으며 사용자에게 어떤 패키지가 누락되었는지 알립니다.

    매개변수:
        file_path (str): 업데이트할 requirements.txt 파일의 경로.

    노트:
        모든 패키지가 설치되어 있고, 버전 정보가 성공적으로 업데이트된 경우 파일이 새로운 내용으로 덮어씌워집니다.
        일부 패키지가 설치되어 있지 않은 경우, 파일은 업데이트되지 않으며, 사용자에게 설치되지 않은 패키지 목록이 출력됩니다.
    """

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