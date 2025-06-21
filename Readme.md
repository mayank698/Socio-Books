# Socio Books

Socio Books is a social media web application built with Django. It allows users to sign up, sign in, create profiles, upload posts with images, and interact with other users. The project includes a modern frontend with custom styles and JavaScript for enhanced user experience.

## Features

- User authentication (sign up, sign in)
- User profiles with profile images
- Post creation with image uploads
- User suggestions and search
- Settings page for user preferences
- Responsive design with custom CSS and Tailwind
- UI components powered by UIKit and custom JavaScript
- Calendar integration with FullCalendar
- Icon support with Remixicon and custom icon sets

## Project Structure

- **core/**: Main Django app with models, views, URLs, and admin configuration.
- **media/**: Uploaded user content (profile and post images).
- **social_book/**: Django project settings and configuration.
- **static/**: Static files (CSS, JS, images, fonts, icons, third-party libraries).
- **templates/**: HTML templates for the frontend.

## Setup Instructions

1. **Clone the repository**
    ```sh
    git clone https://github.com/mayank698/Socio-Books.git
    cd Social\ Media
    ```

2. **Install dependencies**
    ```sh
    pip install -r requirements.txt
    ```

3. **Apply migrations**
    ```sh
    python manage.py migrate
    ```

4. **Create a superuser (optional)**
    ```sh
    python manage.py createsuperuser
    ```

5. **Run the development server**
    ```sh
    python manage.py runserver
    ```

6. **Access the app**
    - Open your browser and go to `http://127.0.0.1:8000/`

## Static & Media Files

- Static files are located in the `static/` directory.
- User-uploaded media files are stored in the `media/` directory.

## License

This project is for educational purposes.
