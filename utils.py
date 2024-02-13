from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from db_schema import Base
from insert_data import load_data_from_json, insert_data

if __name__ == '__main__':
    try:
        engine = create_engine('sqlite:///library_db.db', echo=True)

        Base.metadata.create_all(engine)

        session = Session(engine)

        file_path = 'library_data.json'
        data = load_data_from_json(file_path)

        insert_data(session, data)

        session.commit()

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if session:
            session.close()
