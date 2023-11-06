from flask import Flask, render_template, redirect, request, url_for, Blueprint, abort, jsonify # importing libraries from framework

# registering blueprint 
web_tool = Blueprint('web_tool', __name__)

# Define a class to represent API endpoints
class APIEndpoint:
    def __init__(self, route, methods, description=""):
        self.route = route
        self.methods = methods
        self.description = description

# Function to extract comments from the provided code
def extract_comments(api_code):
    comments = []
    lines = api_code.split('\n')
    is_inside_comment = False
    current_comment = ""

    for line in lines:
        line = line.strip()
        if line.startswith('"""') or line.startswith("'''"):
            if is_inside_comment:
                comments.append(current_comment)
                current_comment = ""
                is_inside_comment = False
            else:
                current_comment = line
                is_inside_comment = True
        elif is_inside_comment:
            current_comment += "\n" + line

    # Append the last comment if it exists
    if is_inside_comment:
        comments.append(current_comment)

    return comments

# Function to extract API information from comments
def extract_api_info(comments):
    endpoints = []
    current_endpoint = None

    for comment in comments:
        comment_lines = comment.strip().split('\n')
        if len(comment_lines) > 1 and comment_lines[0].strip() == '"""API':
            if current_endpoint:
                endpoints.append(current_endpoint)
            current_endpoint = APIEndpoint("", [])
            current_endpoint.description = " ".join(comment_lines[1:]).strip()
        elif current_endpoint and len(comment_lines) > 0:
            if comment_lines[0].strip().lower() == "@route":
                current_endpoint.route = comment_lines[1].strip()
            elif comment_lines[0].strip().lower() == "@methods":
                current_endpoint.methods = [method.strip() for method in comment_lines[1:]]

    if current_endpoint:
        endpoints.append(current_endpoint)

    return endpoints

@web_tool.route('/')
def home():
    return render_template("home.html")

# Route to handle the form submission
@web_tool.route('/generate', methods=['POST'])
def generate():
    api_code = request.form['api_code']
    comments = extract_comments(api_code)
    endpoints = extract_api_info(comments)
    
    # Example: Printing the extracted API information
    for endpoint in endpoints:
        print("Route:", endpoint.route)
        print("Methods:", endpoint.methods)
        print("Description:", endpoint.description)
        print()

    # You can now process the extracted API information to generate documentation

    # Example: Returning the API information as JSON
    api_info = [{"route": endpoint.route, "methods": endpoint.methods, "description": endpoint.description} for endpoint in endpoints]
    return jsonify(api_info)


# Route to handle documentation customization
@web_tool.route('/customize', methods=['POST'])
def customize():
    route = request.form['route']
    description = request.form['description']
    request_parameters = request.form['request_parameters']
    response_structure = request.form['response_structure']

    # Update the documentation information for the specified endpoint
    for endpoint in endpoints:
        if endpoint.route == route:
            endpoint.description = description
            endpoint.request_parameters = request_parameters
            endpoint.response_structure = response_structure
            break

    # Redirect the user back to the documentation
    return render_template('custom.html', endpoints=endpoints)

