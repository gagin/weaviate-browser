from flask import Flask, render_template, request
import weaviate
from weaviate.classes.query import Filter
from weaviate.classes.config import Property, DataType
from weaviate.classes.data import DataObject

app = Flask(__name__)

# Connect to Weaviate (adjust as needed)
client = weaviate.connect_to_local()

def get_collection_properties(collection):
    """Gets properties and their data types from a collection's schema."""
    try:
        collection_schema = collection.config.get()
        properties = {}
        for prop in collection_schema.properties:
            properties[prop.name] = prop.data_type
        return properties
    except Exception as e:
        print(f"Error getting properties for {collection.name}: {e}")
        return {}


def build_weaviate_filter(filters_text, properties_with_types):
    """Builds a Weaviate Filter object from a string and property types."""
    if not filters_text:
        return None

    filter_list = []
    filter_parts = filters_text.split(',')

    for part in filter_parts:
        try:
            prop_name, value_str = part.strip().split(':', 1)
            prop_name = prop_name.strip()
            value_str = value_str.strip()

            if prop_name not in properties_with_types:
                print(f"Warning: Property '{prop_name}' not found in schema.")
                continue

            data_type = properties_with_types[prop_name]

            if data_type == DataType.TEXT:
                value = value_str
            elif data_type == DataType.INT:
                value = int(value_str)
            elif data_type == DataType.NUMBER:
                value = float(value_str)
            elif data_type == DataType.BOOL:
                value = value_str.lower() == 'true'
            elif data_type == DataType.DATE:
                value = value_str
            else:
                print(f"Warning: Unsupported data type {data_type} for {prop_name}.")
                continue

            filter_list.append(Filter.by_property(prop_name).equal(value))

        except (ValueError, TypeError) as e:
            print(f"Invalid filter part '{part}': {e}")
            continue

    if not filter_list:
        return None
    elif len(filter_list) == 1:
        return filter_list[0]
    else:
        return Filter.and_(*filter_list)

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
    limit = int(request.args.get("limit", 10))
    filters_text = request.args.get("filters", "")

    collection = client.collections.get(class_name)
    properties_with_types = get_collection_properties(collection)
    properties = list(properties_with_types.keys())

    weaviate_filter = build_weaviate_filter(filters_text, properties_with_types)

    # Corrected query building and execution
    if weaviate_filter:
        result = collection.query.fetch_objects(
            limit=limit, filters=weaviate_filter, include_vector=False
        )
    else:
        result = collection.query.fetch_objects(limit=limit, include_vector=False)


    # Correctly extract objects from the QueryReturn object
    objects = []
    if result.objects: # Check if there are any objects in the result
        for obj in result.objects:  # Iterate through the .objects attribute
            formatted_obj = {}
            for prop_name in properties:
                formatted_obj[prop_name] = obj.properties.get(prop_name, "N/A")
            objects.append(formatted_obj)

    return render_template(
        "browse.html",
        class_name=class_name,
        properties=properties,
        objects=objects,
        limit=limit,
        filters=filters_text,
    )

if __name__ == "__main__":
    app.run(debug=True)