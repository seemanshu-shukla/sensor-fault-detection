from setuptools import find_packages,setup
#find_packages: searches for package in the local dir for looking for __init__.py file
#setup: used to basically setup the package or defined the intended package

from typing import List

HYPEN_E_DOT='-e .'

def get_requirements(file_path:str)->List[str]:
    """
    This function will return list of requirements
    """
    requirement_list:List[str] = []

    """
    Write a code to read requirements.txt file and append each requirements in requirement_list variable.
    """
    with open(file_path) as file_obj:
        requirement_list=file_obj.readlines()
        requirement_list=[req.replace("\n","") for req in requirement_list]

        if HYPEN_E_DOT in requirement_list:
            requirement_list.remove(HYPEN_E_DOT)
    
    return requirement_list

setup(
    name="sensor", #Name that we want to give to our package
    version="0.0.1",
    author="Seemanshu Shukla",
    author_email="seemanshu.shukla11@gmail.com",
    packages = find_packages(),
    install_requires=get_requirements("requirements.txt"),#["pymongo==4.2.0"],
)

