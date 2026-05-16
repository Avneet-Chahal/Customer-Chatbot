from backend.api.app import app

if __name__ == "__main__":
    print("Website: http://localhost:5001/")
    app.run(debug=True, port=5001)
