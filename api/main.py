from database import create_database, insert_examples, database_exists

if __name__ == "__main__":
    cli_response = None
    while cli_response not in ['y', 'n']:
        cli_response = input("Would you want to delete the database (if exists)? (y/n): ")

    if not database_exists() or cli_response == 'y':
        create_database()
        insert_examples()
