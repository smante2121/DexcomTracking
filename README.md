# DexcomTracking

## Overview
DexcomTracking is a comprehensive web application designed for continuous glucose monitoring via Dexcom devices. This project aims to provide a robust dashboard for healthcare professionals to monitor and analyze patient glucose levels, enhancing patient care and management. Leveraging the Dexcom API, this application supports live tracking and data visualization for both v1 and v2 APIs, ensuring compatibility with a wide range of Dexcom devices.

The code is designed to improve user experience and will become a valuable tool for healthcare professionals to view patients' glucose levels, analyze their condition, and improve patient care. The project will be deployed to numerous offices via Triage Logics Services once completed.

## Features
- **Real-Time Glucose Monitoring**: View live glucose data from Dexcom devices.
- **API Integration**: Seamless integration with Dexcom's v1 and v2 APIs.
- **User-Friendly Dashboard**: An intuitive interface for healthcare professionals to monitor patient data.
- **OAuth2 Security**: Secure authentication and data protection using OAuth2.
- **Switchable API**: Easily switch between v1 and v2 APIs to support a wider range of Dexcom devices.


## Project Structure
- **app.py**: The main application file that runs the code.
- **v1/**: Contains Python files for each v1 API endpoint.
- **v2/**: Contains Python files for each v2 API endpoint.
- **auth.py**: Handles OAuth2 authentication.
- **data.py**: Responsible for retrieving and formatting data for OAuth and endpoint usage.
- **templates/**: HTML templates for the application, organized into v1 and v2 subdirectories.
- **static/**: Contains CSS, JavaScript, and other static files for page viewing and functionality.

## Usage
- To switch between v1 and v2 APIs, uncomment the respective code sections in app.py


## Future Work
- **Expanded Dashboard**: Develop a comprehensive dashboard for healthcare providers to select and view individual patient data.
- **Alert System**: Integrate an alert system to notify healthcare providers of irregular glucose levels.



## Demo
To view a demo of this application in action, click the link below:
[YouTube Demo](https://youtu.be/epw2IpoW-VU)
