To install this application and run it, you must first git clone the repository from github or if you have a zip file extract it to a folder
Then open this in VSCode ensuring you have the python language installed version 3.6 and above.
Then in a terminal in the folder with the code run pip install bcrypt, pip install maskpass, and pip install pyopenssl if ssl is not already installed in your device

To run the application open a terminal in the folder the code is stored in and enter the text between speech marks into the terminal and click enter "python chat_server.py --name=server --port=9988" to run the server. The text after the --name= part doesnt matter.

And open a new terminals and enter the text inbetween the speech marks "python chat_client.py --name=client2 --port=9988" (the name field can contain anything) and press enter to run the chat clients. 

You should now see the Register or Quit options Register a new user by typing in a username consisting of any characters with a minimum length of 1 character and click enter, then type in a password consisting of any characters of a length of at least 1 character. You can click the left control button on your keyboard to make it visible. Then repeat the process for another chat client and you can begin chatting. During the login, register or chatting procedures you can type 'Q' into the text fields to exit and log out. The chat application is limited to 2 chat clients/users at any one time.