# Clarity Tutoring

Created by Luca Sargent

## What is Clarity Tutoring?

Clarity Tutoring is a local learning service in Tauranga and online service for New Zealand that helps students build strong skills and boost their school confidence through clear, one-on-one lessons tailored to each child's unique needs.

## How to Setup Clarity Tutoring?
Insert these following commands at the **root** of the directory.

First create a virtual environment:
`
py -m venv .venv
`
Then it is key to run this virtual environment using commands below:
> [!Note]
> The "Set-ExecutionPolicy" is only there because powershell disables scripts by default through certain wifi. It will only give temporary access while launching.
```
Set-ExecutionPolicy RemoteSigned -Scope Process ; 
.venv/Scripts/activate
```
Next install the following frameworks & libraries:
> [!TIP]
> The "--upgrade pip" may not be necessary if already to date.
```
py -m pip install --upgrade pip
py -m pip install django
py -m pip install Pillow
```
Once those are installed use the commands to run it:
```
cd clarity  
py manage.py runserver 6464
```
Now everything should be complete and you can go to the following link: 
[Local Host](https://localhost:6464)

## How to Run Clarity Tutoring?
Once you have done the setup to relaunch it there is a different order.

Just paste in the connected command below:
```
Set-ExecutionPolicy RemoteSigned -Scope Process ; 
.venv/Scripts/activate ; 
cd clarity ;
py manage.py runserver 6464
```
Now everything should be complete and you can go to the following link: 
[Local Host](https://localhost:6464/admin)