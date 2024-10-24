To install this application and run it, you must first git clone the repository from github or if you have a zip file extract it to a folder.
Then open the folder containg the code in VSCode ensuring you have the python language installed version 3.6 and above.
Then in a terminal in the folder with the code run pip install bcrypt, pip install maskpass, and pip install pyopenssl if ssl is not already installed in your device.

To run the application open a new terminal in the folder the code is stored in and enter the text between speech marks into the terminal and click enter "python chat_server.py --name=server --port=9988" to run the server. 

Then open a new terminals and enter the text inbetween the speech marks "python chat_client.py --name=client1 --port=9988"  and press enter to run the chat client. 

You should now see the Register or Quit options Register a new user by typing in a username consisting of any characters with a minimum length of 1 character and click enter, then type in a password consisting of any characters of a length of at least 1 character. You can click the left control button on your keyboard to make it visible. 
Then enter the text in between the speech marks to create a new client "python chat_client.py --name=client2 --port=9988" into a new terminal opened in the folder the code is in, 
and go through the login/register process and you can begin chatting with the previously made client. During the login, register or chatting procedures you can type 'Q' into the text fields to exit and log out.
The chat application is limited to 2 chat clients/users at any one time.

Generating a new certificate is done by entering this text in speech marks into the terminal opened in the folder with the code and hitting enter, it is completely optional. 
"openssl req -new -x509 -days 365 -nodes -out cert.pem -keyout cert.pem"
