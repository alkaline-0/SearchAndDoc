import pysolr
import requests
import random
import datetime

def create_collection_from_server_id(
    server_id,
    message_id,
    discord_server_id,
    discord_message_id,
    discord_message_content,
    discord_channel_id,
    discord_category_id,
    discord_author_id,
    discord_author_name
):
    """
    Creates a Solr collection and defines its schema based on provided parameters.
    Args:
        server_id (str): Internal Server ID (used as core name).
        message_id (int): Internal Message ID.
        discord_server_id (int): Discord Server ID.
        discord_message_id (int): Discord Message ID.
        discord_message_content (str): Discord Message Content.
        discord_channel_id (int): Discord Channel ID.
        discord_category_id (int): Discord Category ID.
        discord_author_id (int): Discord Author ID.
        discord_author_name (str): Discord Author Name.
    Returns:
        bool: True if the collection and schema were created successfully, False otherwise.
    """
    solr_url = "http://localhost:8983/solr"  # assuming Solr is running locally
    schema_fields = [
        {"name": "message_id", "type": "pint", "stored": True, "indexed": True},
        {"name": "discord_message_id", "type": "pint", "stored": True, "indexed": True},
        {"name": "discord_message_content", "type": "string", "stored": True, "indexed": True},
        {"name": "discord_channel_id", "type": "pint", "stored": True, "indexed": True},
        {"name": "discord_category_id", "type": "pint", "stored": True, "indexed": True},
        {"name": "discord_author_id", "type": "pint", "stored": True, "indexed": True},
        {"name": "discord_author_name", "type": "string", "stored": True, "indexed": True},
        {"name": "discord_server_id", "type": "pint", "stored": True, "indexed": True},
        {"name": "timestamp", "type": "pdate", "stored": True, "indexed": True}, #added timestamp
    ]
    try:
        # create the collection (TODO: make a collection config)
        create_core_url = f"{solr_url}/admin/collections?action=CREATE&name={server_id}&collection.configName=_default&numShards=1&replicationFactor=1"
        response = requests.get(create_core_url)
        response.raise_for_status()
        print(f"Collection '{server_id}' created successfully.")

        solr = pysolr.Solr(f"{solr_url}/{server_id}", always_commit=True)

        # define the schema fields
        for field in schema_fields:
            add_field_url = f"{solr_url}/{server_id}/schema"
            payload = {"add-field": field}
            response = requests.post(add_field_url, json=payload)
            response.raise_for_status()
            print(f"Field '{field['name']}' added successfully.")
        print(f"Schema for collection '{server_id}' defined successfully.")

        # initial document
        document = {
            "message_id": message_id,
            "discord_message_id": discord_message_id,
            "discord_message_content": discord_message_content,
            "discord_channel_id": discord_channel_id,
            "discord_category_id": discord_category_id,
            "discord_author_id": discord_author_id,
            "discord_author_name": discord_author_name,
            "discord_server_id": discord_server_id,
            "timestamp": datetime.datetime.now().isoformat(),
        }
        solr.add([document])
        print("Initial document added")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error creating collection or schema: {e}")
        return False
    except pysolr.SolrError as e:
        print(f"Solr error: {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False

def generate_realistic_dummy_document(server_id):
    """Generates a realistic dummy document for the given Solr core."""
    solr_url = f"http://localhost:8983/solr/{server_id}/update?commit=true"
    solr = pysolr.Solr(solr_url, always_commit=True)

    message_id = random.randint(1000, 9999)
    discord_server_id = random.randint(100000000000000000, 999999999999999999)
    discord_message_id = random.randint(100000000000000000, 999999999999999999)
    discord_channel_id = random.randint(100000000000000000, 999999999999999999)
    discord_category_id = random.randint(100000000000000000, 999999999999999999)
    discord_author_id = random.randint(100000000000000000, 999999999999999999)

    author_names = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Henry", "Ivy", "Jack"]
    discord_author_name = random.choice(author_names)

    message_contents = [
        "Hey everyone, how's it going?",
        "Just finished a great coding session!",
        "Anyone up for a game later?",
        "Check out this cool link: https://example.com",
        "Learning a lot about Solr today.",
        "This is a test message.",
        "What are your thoughts on this?",
        "I need help with a bug!",
        "Good morning, world!",
        "It's Friday!"
    ]
    discord_message_content = random.choice(message_contents)

    timestamp = datetime.datetime.now().isoformat()

    document = {
        "message_id": message_id,
        "discord_message_id": discord_message_id,
        "discord_message_content": discord_message_content,
        "discord_channel_id": discord_channel_id,
        "discord_category_id": discord_category_id,
        "discord_author_id": discord_author_id,
        "discord_author_name": discord_author_name,
        "discord_server_id": discord_server_id,
        "timestamp": timestamp,
    }

    try:
        #solr.add([document]) -- solr.add seems buggy, returns HTTP400
        response = requests.post(solr_url, json=[document])
        response.raise_for_status()
        print(f"Dummy document added to collection '{server_id}'.")
        return True
    except pysolr.SolrError as e:
        print(f"Error adding dummy document: {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False

if __name__ == "__main__":
    server_id = "test_server_1"
    #if create_collection_from_server_id(server_id, 1, 1, 1, "1", 1, 1, 1, "1"):
        #generate_realistic_dummy_document(server_id)
    generate_realistic_dummy_document(server_id) #add another for testing.
