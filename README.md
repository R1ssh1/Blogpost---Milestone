# Blogpost-Milestone
Repository for the blogpost website by the milestone club for VIT-AP

You can find the code for html pages on : 'blogpost/user/templates'

The user directory is an app for django

The html code for the navbar has been added as a base static file, as it is used by all the pages. So to code any page, you just need to use:

{% extends 'base.html' %}

{% block body%}

#the code for the main body content	
	
{% endblock %}

The style.css file is also loaded in with the base static file. If you want to have a further look at it, it is located in : 'blogpost/user/templates/base.html'

To run on your machine, open Command Prompt, make sure you are in the blogpost directory and type the following:

python manage.py runserver

Then open the localhost website using the link given in the Command Prompt window or use:

http://127.0.0.1:8000/

in your browser

Github: https://github.com/R1ssh1/Blogpost-Milestone
Doc links:
https://getbootstrap.com/docs/5.3/getting-started/introduction/
https://docs.djangoproject.com/en/5.0/



