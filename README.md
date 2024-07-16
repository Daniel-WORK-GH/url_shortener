# url_shortener

### Description
This program will open a server on localhost using port 8000. It will allow the user to input a url and the server will return a new short one.

### Technical 
After inputing the url it will be sent to the server, the server will hash it save the Hex value as a string. If that HEX value isn't used in the database it will link it to the inputed url. Otherwise it will try to find an unused HEX value.

When the user clicks the created link it will take him to the server, the server will fetch the actual wanted url from the database and redirect the user there. 

### Exapmle
Shorten: https://github.com/Daniel-WORK-GH/url_shortener/edit/main/README.md

The output url was: 

![image](https://github.com/user-attachments/assets/838f47cc-023a-4265-8d79-75ac6b2fc61e)

When clicking on the output url i was taken back to the original one:

![image](https://github.com/user-attachments/assets/66d9a891-c81c-44d1-8772-08661046564d)

