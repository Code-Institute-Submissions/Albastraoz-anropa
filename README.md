## Anropa development website.

This project idea came to life after I got in touch with a client who was in need of a website for their startup job agency.
The goal was to create a good looking website with easy to use tools for admin and user to create a more automated database online.
Before I decided to accept this project I already created a logo and business card for the client.
This gave me the advantage of that I already knew the colors and layout to use in the website.

To get admin access to the website use the following login:
email: admin@anropa.com
password: anropaadmin

Hosted on [Heroku](https://anropa-developmentsite.herokuapp.com/)
Repository on [GitHub](https://github.com/Albastraoz/anropa)

## UX

![Responsive Views of website](/static/images/responsive.jpg)

### Users 
Expected users of the website are people looking for a job and companies looking for new staff.
Also the employees of the job agencie will use the website a lot to post, edit and delete vacancies plus look for user information.

### User Stories
1. Companie looking for new staff
2. Jobless person waiting for their new job adventure
3. Owner of website to make the user database automated
4. Owner of website to create new vacancies

### Design
![Website Logo - Anropa](/static/images/logo.png)
- Colour scheme is blue with grey which was the clients own choice
    - Main blue colour:   ![#1A76BC](https://placehold.it/15/#1A76BC/000000?text=+) `#1A76BC`
    - Other grey colours have been used to create visible difference
    - Black and white for balance
- [Custom designed logo](/static/images/logo.png) created using the following font: 
    - font-family: 'Nyala', sans-serif;
    - font-family: 'Myriad Pro', sans-serif;
- Roboto and Krona One font used throughout the website
    - font-family: 'Roboto', sans-serif;
    - font-family: 'Krona One', sans-serif;

### Mockups
The website consists of several pages each with a unique section of information:
- [Homepage](https://www.figma.com/file/4DeBoEp0PPx3HwVNjZ0jzB/Anropa?node-id=1%3A37)  
- [Database](https://www.figma.com/file/4DeBoEp0PPx3HwVNjZ0jzB/Anropa?node-id=0%3A1)  

## Features

Features planned, implemented and outlined for later development 

### Planned Features
- Documentation - ReadMe File & Mockups
- Website content
- Contact form functionality
- Apply button to apply for job
- Colour Scheme
- Custom Logo
- MongoDB database
    - CRUD for vacancies
    - CRUD for users
- Bootstrap - HTML, CSS Framework
    - Grid System - Columns and Rows
    - Icons
- User register/login database
- Vacancy database
- Email verification when registering
- Password reset functionality
- Multiple file uploads
- Search function for user database (admin only)
- CMS system for content (admin)
- Search function for vacancies
- Responsive design - Mobile First
- UX elements
    - User Flow
    - Animations
    - Transitions
- Accesibility
- Git - Version Control System
- GitHub - Remote Repository
- Deployed - Hosted on Heroku

### Existing Features
- Documentation - ReadMe File & Mockups
- Website content
- Contact form functionality
- Apply button to apply for job
- Colour Scheme
- Custom Logo
- MongoDB database
    - CRUD for vacancies
    - CRUD for users
- Bootstrap - HTML, CSS Framework
    - Grid System - Columns and Rows
    - Icons
- User register/login database
- Vacancy database
- Email verification when registering
- Password reset functionality
- Multiple file uploads
- Search function for user database (admin only)
- Responsive design - Mobile First
- UX elements
    - User Flow
    - Animations
    - Transitions
- Accesibility
- Git - Version Control System
- GitHub - Remote Repository
- Deployed - Hosted on Heroku

### Features Left to Implement
- CMS system for content (admin)
- Search function for vacancies


## Technologies Used

This project makes use of:
- [HTML](https://developer.mozilla.org/en-US/docs/Web/HTML)
    - HTML for basic strucutre
- [CSS](https://developer.mozilla.org/en-US/docs/Web/CSS)
    - CSS for Styling
- [Bootstrap](https://getbootstrap.com/)
    - HTML and CSS Framework from **Bootstrap**
- [Javascript](https://www.w3schools.com/jsref/)
    - JavaScript for game application
- [jQuery](https://jquery.com/)
    - The project uses JQuery to simplify DOM manipulation
- [Visual Studio Code](https://code.visualstudio.com/)
    - Changed to local workspace where I used VS Code as editor
- [Python](https://www.python.org/)
    - Project runs on Python
- [Flask](http://flask.palletsprojects.com/en/1.1.x/)
    - Flask plugin is used for website functionality
- [AtlasMongoDB](https://www.mongodb.com/cloud/atlas)
    - A MongoDB database is used to store information
- [Google Chrome](https://www.google.com/chrome/)
    - Used for browser and dev tools
- [Mozilla Firefox](https://www.mozilla.org/en-US/firefox/new)
    - Used for browser and dev tools
- [Google](https://www.google.com/)
    - **Google** was used for research.
- [Git](https://git-scm.com/)
    - **Git** used for Version Control
- [GitHub](https://github.com/)
    - Repository hosted on **GitHub**
- [Heroku](https://www.heroku.com)
    - Website hosted on **Heroku**
- [Am I Responsive](http://ami.responsivedesign.is)
    - Testing responsiveness of the website

## Testing

The website was tested by users, Chrome/Firefox dev tools and for errors on W3.

### User experience testing 
Preview was send regularly to people within my social circle and asked for testing.

1. Sending website location to specific users over messaging.
2. Write down feedback.
3. Search for possible fixes.
4. If possible implement solution to error or improve product.

### Dev tools
- Everything has been tested and works correctly except for some minor bugs.
- Know bugs and will be addressed:
    - Still need a max upload size for all files together.
    - Search function for users as of right now only works my searching for a specific email address.

### Coding error testing
After complete product start to addres coding errors:

1. Go to W3's validation websites [HTML](https://validator.w3.org) or [CSS](https://jigsaw.w3.org/css-validator/).
2. Fill in URL of every specific page and look for errors.
3. Locate errors and solve accordingly.
4. After all errors are solved go back to step 1 and continue untill no errors are shown.

## Deployment

The project is hosted on [Heroku](https://anropa-developmentsite.herokuapp.com/)
 
To deploy your own version of the website:
- Have git installed
- Visit the [repository]([GitHub](https://github.com/Albastraoz/anropa))
- Click 'Clone or download' and copy the code for http
- Open your chosen IDE (Cloud9, VS Code, etc.)
- Open a terminal in your root directory
- Type 'git clone ' followed by the code taken from github repository
    - ```git clone https://github.com/Albastraoz/anropa.git```
- Install all dependencies from the requirements.txt file
- When this completes you have your own version of the website
    - Feel free to make any changes to it
- The website can be run by opening one of the HTML files within a web browser
- Visit the link provided
- Your website with any made changes will appear
- Saved changes to the website will appear here after refreshing the page

The benefits of hosting your website on Heroku through Github is that any pushed changes to your project will automatically update the website. Development branches can be created and merged to the master when complete.

It may take a moment for changes to appear on the hosted website.

## Credits

### Content
The text on the website has been written myself or copied and edited from:  
- [Wikipedia](https://www.wikipedia.org/)

All icons are imported from Fontawesome:
- [Fontawesome](http://www.fontawesome.com/)

Fonts are imported from Google fonts:
- [Google Fonts](https://fonts.google.com/)

### Media
The images for the website are copyright free and taken from:
- [Pxhere](https://pxhere.com/)
- [Flickr](https://www.flickr.com/)

All images direct location:
- [jumbotron-image.jpg](https://pxhere.com/en/photo/1194115)
- [female-portrait.jpg](https://www.flickr.com/photos/hendrikwieduwilt/39072939820)
- [male-portrait.jpg](https://www.flickr.com/photos/hendrikwieduwilt/27012448648)
- [employees-image.jpg](https://pxhere.com/en/photo/747034)
- [employers-image.jpg](https://www.flickr.com/photos/byrawpixel/45789233761)
- [contact-image.jpg](https://www.flickr.com/photos/ervins_strauhmanis/14562090039)

### Acknowledgements
Thank you to the following for inspiration, motivation and the direction I needed:

- Seun Owonikoko    @seun_mentor
- Yung-Chin Huang
- Code Institute
- Google - your best friend
