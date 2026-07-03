import os
from app import create_app
from models import db
from sqlalchemy import text

app = create_app()

with app.app_context():
    # Get all table names
    tables = db.engine.table_names() if hasattr(db.engine, 'table_names') else db.metadata.tables.keys()
    
    for table_name in tables:
        try:
            # PostgreSQL specific query to sync sequence
            # pg_get_serial_sequence('table_name', 'id') gets the sequence name
            # setval(sequence_name, max_id) sets the sequence
            
            # First, check if the table has an 'id' column
            columns_query = text(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}';")
            columns = [row[0] for row in db.session.execute(columns_query).fetchall()]
            
            if 'id' in columns:
                query = text(f"""
                    SELECT setval(
                        pg_get_serial_sequence('{table_name}', 'id'), 
                        COALESCE((SELECT MAX(id) FROM {table_name}), 1)
                    );
                """)
                db.session.execute(query)
                print(f"Successfully synced sequence for table: {table_name}")
            else:
                print(f"Skipped table (no 'id' column): {table_name}")
                
        except Exception as e:
            print(f"Error syncing {table_name}: {e}")

    db.session.commit()
    print("All sequences synchronized successfully.")
