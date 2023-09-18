from stock_api import create_app, db

# checks if the run.py file has executed directly and not imported
if __name__ == '__main__':  
    
    app = create_app()
    
    # create database tables before app runs
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)

    
