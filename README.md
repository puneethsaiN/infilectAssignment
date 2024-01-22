1. Clone the gitHub repository
2. Activate the virtual enviroment using "/fastapienv/Scripts/activate.bat"
3. Activate the server using "uvicorn main:app --reload"
4. Open another command line in the same directory and perform a POST request <br>
   Example: curl -X POST "http://127.0.0.1:8000/largest-rectangle" -H "Content-Type: application/json" -d "[[1, 0, 1, 0, 1, -9], [1, 1, 1, 1, 2, -9], [1, 1, 1, 1, 2, -9], [1, 0, 0, 0, 5, -9], [5, 0, 0, 0, 5]]"
6. To view log requests in the second terminal open sqlite command line by doing "sqlite3 logs.db"
7. Then enter "SELECT * FROM logs;" to view all the log details
