from sqlalchemy.orm import Session


def fetch_data(db_func: Session, query: str):
    """Run SQL query and return JSON-serializable data."""
    try:
        cursor = db_func.cursor(dictionary=True)
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        db_func.rollback()
        return {"error": str(e)}
    

def post_data(db_func: Session, query: str, values: tuple):
    """Run an SQL query to insert/update/delete data and return success/failure."""
    try:
        cursor = db_func.cursor()
        cursor.execute(query, values)
        db_func.commit()
        return {"success": True, "message": "Data inserted successfully"}
    except Exception as e:
        db_func.rollback()
        return {"success": False, "error":{e}}
