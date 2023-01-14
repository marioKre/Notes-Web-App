from website import create_app

app = create_app()

# Allows executing code when the file runs as a script directly, but not when it’s imported as a Module
if __name__ == '__main__':
    
    # debug=True automatically re-runs web server when change is made  
    app.run(debug=True)
    