# From: Zero to AI Agent, Chapter 6, Section 6.4
# File: 05_reraise_chain.py


# Re-raising
def process_with_logging(data):
    try:
        result = risky_operation(data)
        return result
    except Exception as e:
        log_error(e)  # Log it
        raise  # Re-raise the same exception

# Exception chaining
def get_user_from_db(user_id):
    try:
        users = load_users()
        return users[user_id]
    except KeyError as e:
        # Provide better context
        raise ValueError(f"User {user_id} not found") from e
