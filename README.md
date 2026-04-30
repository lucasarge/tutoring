# Clarity Tutoring
Created by Luca Sargent
## What is Clarity Tutoring?
It is a booking website for a tutoring business.

## How to Run Clarity Tutoring?
Insert these following commands at the **root** of the directory.

First create a virtual environment:
`
py -m venv .venv
`\
Next install the following frameworks & libraries:
> [!TIP]
> The "--upgrade pip" may not be necessary if already to date.
```
py -m pip install django
py -m pip install Pillow
py -m pip install --upgrade pip
```
Once those are installed use the connected command to run:
> [!Note]
> The "Set-ExecutionPolicy" is only there because powershell disables scripts by default. It will only give temporary access while launching.
```
Set-ExecutionPolicy RemoteSigned -Scope Process ; 
.venv/Scripts/activate ; 
cd clarity ; 
py manage.py runserver 6464
```
Now everything should be complete and you can go to the following link: 
[Local Host](https://localhost:6464)