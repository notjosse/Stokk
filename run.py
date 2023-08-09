from stock_api import app, db

# checks if the run.py file has executed directly and not imported
if __name__ == '__main__':  
    # create database tables before app runs
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)

    
