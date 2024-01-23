# How to open this Project? 
1. Clone the gitHub repository
2. Activate the virtual enviroment using "/fastapienv/Scripts/activate.bat"
3. Activate the server using "uvicorn main:app --reload"
4. Open another command line terminal in the same directory and perform a POST request <br>
   Example: curl -X POST "http://127.0.0.1:8000/largest-rectangle" -H "Content-Type: application/json" -d "[[1, 0, 1, 0, 1, -9], [1, 1, 1, 1, 2, -9], [1, 1, 1, 1, 2, -9], [1, 0, 0, 0, 5, -9], [5, 0, 0, 0, 5]]"
6. To view log requests in the second terminal open sqlite command line by doing "sqlite3 logs.db"
7. Then enter "SELECT * FROM logs;" to view all the log details

<h1>Preview</h1>
<h3>Virtual Environment and Server startup</h3>
<img src="Screenshots/Screenshot 2024-01-22 181136.png"> 

<h3>POST request to the API</h3>
<img src="Screenshots/Screenshot 2024-01-22 181148.png">

<h3>Accessing Logs in the database</h3>
<img src="Screenshots/Screenshot 2024-01-22 181228.png">

