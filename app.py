from app import create_app

# Main WSGI application instance for Vercel and local dev
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
