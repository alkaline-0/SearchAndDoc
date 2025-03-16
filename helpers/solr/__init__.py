import pysolr

import pysolr
import requests

def create_core_from_server_id(
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
    Creates a Solr core and defines its schema based on provided parameters.

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
        bool: True if the core and schema were created successfully, False otherwise.
    """
    solr_url = "http://localhost:8983/solr"  # Assuming Solr is running locally

    schema_fields = [
        {"name": "message_id", "type": "pint", "stored": True, "indexed": True},
        {"name": "discord_message_id", "type": "pint", "stored": True, "indexed": True},
        {"name": "discord_message_content", "type": "string", "stored": True, "indexed": True},
        {"name": "discord_channel_id", "type": "pint", "stored": True, "indexed": True},
        {"name": "discord_category_id", "type": "pint", "stored": True, "indexed": True},
        {"name": "discord_author_id", "type": "pint", "stored": True, "indexed": True},
        {"name": "discord_author_name", "type": "string", "stored": True, "indexed": True},
        {"name": "discord_server_id", "type":"pint", "stored": True, "indexed": True}, #added discord server ID to the schema.
    ]

    try:
        # Create the core
        create_core_url = f"{solr_url}/admin/cores?action=CREATE&name={server_id}&instanceDir={server_id}&configSet=_default"
        response = requests.get(create_core_url)
        response.raise_for_status()
        print(f"Core '{server_id}' created successfully.")

        # Connect to the new core
        solr = pysolr.Solr(f"{solr_url}/{server_id}", always_commit=True)

        # Define the schema fields
        for field in schema_fields:
            add_field_url = f"{solr_url}/{server_id}/schema"
            payload = {"add-field": field}
            response = requests.post(add_field_url, json=payload)
            response.raise_for_status()
            print(f"Field '{field['name']}' added successfully.")

        print(f"Schema for core '{server_id}' defined successfully.")

        #Add the initial document.
        document = {
            "message_id": message_id,
            "discord_message_id": discord_message_id,
            "discord_message_content": discord_message_content,
            "discord_channel_id": discord_channel_id,
            "discord_category_id": discord_category_id,
            "discord_author_id": discord_author_id,
            "discord_author_name": discord_author_name,
            "discord_server_id": discord_server_id,
        }
        solr.add([document])
        print("Initial document added")

        return True

    except requests.exceptions.RequestException as e:
        print(f"Error creating core or schema: {e}")
        return False
    except pysolr.SolrError as e:
        print(f"Solr error: {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False

def create_document(core, doc_id, doc_title):
    solr = pysolr.Solr('https://localhost:8983/solr/' + core, always_commit=True)

    document = {
        'id': doc_id,
        'title': doc_title,
    }

    solr.add(document)

    results = solr.search('title:local')
    for result in results:
        print(f"ID: {result['id']}, Title: {result['title']}")

if __name__ == "__main__":
    create_core_from_server_id("1", 1, 1, 1, "1", 1, 1, 1, "1")
