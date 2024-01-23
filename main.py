from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, func
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy.ext.declarative import DeclarativeMeta
from databases import Database
from sqlalchemy.orm import sessionmaker
import time

def isValid(matrix, maxSizeRect, row, col):
    wid = maxSizeRect[row][col][0]
    hgt = maxSizeRect[row][col][1]

    top_left_x = row - hgt + 1
    top_left_y = col - wid + 1

    st = set()
    for i in range(top_left_x, row + 1):
        for j in range(top_left_y, col + 1):
            st.add(matrix[i][j])
    return len(st)==1


def largest_rectangle(matrix: list[list[int]]) -> tuple:
    """
    :param matrix: A 2D matrix of integers (1 <= len(matrix),
    len(matrix[0]) <= 100)
    :return: The area of the largest rectangle formed by similar numbers
    """
    # Your code here
    maxSizeRect = []
    for i in range(len(matrix)):
        n = len(matrix[i])
        temp_list = [[1 for col in range(2)] for row in range(n)]
        maxSizeRect.append(temp_list)

    
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if j != 0 and matrix[i][j] == matrix[i][j-1]:
                maxSizeRect[i][j][0] = maxSizeRect[i][j-1][0] + 1
            if i != 0 and j < len(matrix[i-1]) and matrix[i][j] == matrix[i-1][j]:
                maxSizeRect[i][j][1] = maxSizeRect[i-1][j][1] + 1

    maxArea = -float('inf')            
    resNum = -1
    for row in range(len(matrix)):
        for col in range(len(matrix[row])):
            if maxSizeRect[row][col][0] == maxSizeRect[row][col][1]:
                continue
            currArea = maxSizeRect[row][col][0] * maxSizeRect[row][col][1]
            if currArea > maxArea and isValid(matrix, maxSizeRect, row, col):
                maxArea = currArea
                resNum = matrix[row][col]           
                
    print(resNum, maxArea)
    return (resNum, maxArea)


DATABASE_URL = "sqlite:///./logs.db"
Base = declarative_base()
metadata = Base.metadata

class LogEntry(Base):
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True, index=True)
    method = Column(String, index=True)
    path = Column(String, index=True)
    status_code = Column(Integer)
    request_body = Column(String)
    response_body = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    turnaround_time = Column(Float)

# Create SQLite database tables
engine = create_engine(DATABASE_URL)
metadata.create_all(bind=engine)

app = FastAPI()

Session = sessionmaker(bind=engine)

async def background_task(matrix: list[list[int]], start_time: float) -> None:
    result = largest_rectangle(matrix)
    turnaround_time = time.time() - start_time
    print(f"Turnaround Time: {turnaround_time} seconds")

    # Log entry with timestamp and turnaround time
    log_entry = LogEntry(
        method="POST",
        path="/largest-rectangle",
        status_code=200,  # Assuming success for simplicity
        request_body=str(matrix),
        response_body=str(result),
        timestamp=func.now(),
        turnaround_time=turnaround_time,
    )

    # Create a session
    session = Session()

    # Add the log entry to the session
    session.add(log_entry)

    # Commit the changes to the database
    session.commit()

    # Close the session
    session.close()



@app.post("/largest-rectangle", response_model=tuple[int, int])
async def get_largest_rectangle(request: Request, background_tasks: BackgroundTasks) -> tuple[int, int]:
    try:
        matrix = await request.json()
        start_time = time.time()
        background_tasks.add_task(background_task, matrix, start_time)
        return largest_rectangle(matrix)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    


if __name__ == "__main__":
    # Create SQLite database tables
    Base.metadata.create_all()

    # Run FastAPI server
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)



'''
    curl -X POST "http://127.0.0.1:8000/largest-rectangle" -H "Content-Type: application/json" -d "[[1, 0, 1, 0, 1, -9], [1, 1, 1, 1, 2, -9], [1, 1, 1, 1, 2, -9], [1, 0, 0, 0, 5, -9], [5, 0, 0, 0, 5]]"

'''





