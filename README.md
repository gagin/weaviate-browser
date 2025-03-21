# Weaviate Explorer

This is a simple, single-file Flask application that allows you to
browse the contents of a Weaviate database. It was created to provide a
quick and easy way to inspect data stored in Weaviate, especially during
development and experimentation with AI applications.

## Motivation

While working with Weaviate and AI platforms like Dify, I often needed a
visual way to see what data my applications were storing in the Weaviate
database. Rather than writing custom scripts each time, I built this
lightweight browser to provide a basic overview of collections, object
counts, and object properties.

## Features

-   **List Collections:** Displays a list of all collections in your
    Weaviate instance, along with the number of objects in each
    collection.
-   **Browse Collection Objects:** Allows you to view the objects within
    a specific collection, displaying their properties in a table.
-   **Filtering:** Includes a simple text filter to narrow down the list
    of displayed collections.
-   **Limit Results:** You can specify a limit on the number of objects
    displayed per collection, preventing the browser from being
    overwhelmed by very large collections.
-   **Simple Property:Value Filter**: Allows to filter by one or several
    properties in format `property:value,property2:value2`.
-   **Single File Application:** The entire application is contained
    within a single `main.py` file, making it easy to deploy and run.
-   **Uses Weaviate Python Client v4:** Built using the latest Weaviate
    Python client.

## Requirements

-   Python 3.7+
-   Weaviate (running locally or in the cloud)
-   Flask
-   weaviate-client (v4)

## Installation

1.  **Clone the repository (or just copy the \`\`main.py\`\` file):**

    ``` bash
    git clone <repository_url>  # Replace <repository_url>
    cd weaviate-browser
    ```

2.  **Install dependencies:**

    ``` bash
    pip install flask weaviate-client
    ```

## Usage

1.  **Ensure Weaviate is Running:** Make sure your Weaviate instance is
    running (either locally or in the cloud). If you are not running
    locally, modify the `client = weaviate.connect_to_local()` line in
    `main.py` to connect to your Weaviate instance (e.g., using
    `connect_to_weaviate_cloud` or `connect_to_custom`).

2.  **Run the application:**

    ``` bash
    python main.py
    ```

3.  **Open your web browser and go to:**

    ``` 
    http://127.0.0.1:5000/
    ```

You should see a list of your Weaviate collections. Click on a
collection name to browse its objects. You can use the \"Limit\" and
\"Filters\" inputs to control the displayed data.

## Project Structure

``` 
.
├── main.py  <- application code
├── templates
    ├── browse.html <- browse collection objects page
    └── index.html <- index page
```

## Weaviate Python Client v4 Reference

A function reference for the Weaviate Python client v4, which was used
to build this application, is available here:
<https://github.com/gagin/weaviate-v4-python-reference/>

## Contributing

Contributions are welcome! If you find any bugs or have suggestions for
improvements, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file
for details. (You should add a LICENSE file to your repository).
