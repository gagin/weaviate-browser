from flask import Flask, render_template, request
import weaviate
from weaviate.classes.query import Filter

app = Flask(__name__)

# Connect to Weaviate
client = weaviate.connect_to_local()  # For local connection - modify as needed

@app.route("/")
def index():
    """Displays available collections and their object counts."""
    # Get all collection names
    collections = [collection for collection in client.collections.list_all()]

    if not collections:
        return "No collections found. Check if Weaviate is running and has data."

    class_counts = {}
    for class_name in collections:
        collection = client.collections.get(class_name)
        result = collection.aggregate.over_all()
        class_counts[class_name] = result.total_count

    return render_template("index.html", schema=collections, class_counts=class_counts)

@app.route("/browse/<class_name>")
def browse(class_name):
    """Browses objects of a specific class."""
    limit = int(request.args.get("limit", 10))  # Default limit of 10
    filters_text = request.args.get("filters", "")
    
    collection = client.collections.get(class_name)
    
    # Get property names from collection schema properly
    properties = []
    try:
        # Get the collection properties from its schema
        collection_schema = collection.properties.get()
        properties = [prop["name"] for prop in collection_schema]
    except Exception as e:
        print(f"Failed to get properties: {e}")
        # Fallback - we'll discover properties from the results
        properties = []
    
    query_obj = collection.query
    
    # Apply filters if provided
    if filters_text:
        try:
            # Simple filter parsing - format: property:value
            parts = filters_text.split(':')
            if len(parts) == 2:
                property_name, value = parts[0].strip(), parts[1].strip()
                # Create a filter for the property
                filter_obj = Filter.by_property(property_name).equal(value)
                query_obj = query_obj.with_where(filter_obj)
        except Exception as e:
            # If filter parsing fails, continue without filters
            print(f"Filter error: {e}")
            
    objects = query_obj.near_text(query="", limit=limit).objects
    
    # If properties list is empty, extract them from first object
    if not properties and objects:
        # Filter out special properties that start with _
        properties = [prop for prop in objects[0].properties.keys() if not prop.startswith('_')]

    # Create a list of dictionaries for each object with its properties
    formatted_objects = []
    for obj in objects:
        formatted_obj = {}
        # Assuming you want to access properties:
        for prop_name, prop_value in obj.properties.items():
            formatted_obj[prop_name] = prop_value
        formatted_objects.append(formatted_obj)

    return render_template("browse.html", 
                           class_name=class_name, 
                           properties=properties, 
                           objects=formatted_objects, 
                           limit=limit,
                           filters=filters_text)

if __name__ == "__main__":
    app.run(debug=True)