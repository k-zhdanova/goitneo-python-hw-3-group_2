AVAILABLE_COMMANDS = {
    "autotest": {
        "preview": "autotest",
        "description": "Run the autotest",
    },
    "hello": {
        "preview": "hello",
        "description": "Greet the bot",
    },
    "all": {
        "preview": "all",
        "description": "Get all contacts",
    },
    "add": {
        "preview": "add <name> <phone>",
        "description": "Add a new contact",
    },
    "find": {
        "preview": "find <name>",
        "description": "Find a contact",
    },
    "change": {
        "preview": "change <name> <old_phone> <new_phone>",
        "description": "Change an existing contact",
    },
    "delete": {
        "preview": "delete <name>",
        "description": "Delete an existing contact",
    },
    "add-phone": {
        "preview": "add-phone <name> <phone>",
        "description": "Add a new phone to a contact",
    },
    "find-phone": {
        "preview": "find-phone <name>",
        "description": "Get the phone number of a contact",
    },
    "delete-phone": {
        "preview": "delete-phone <name> <phone>",
        "description": "Delete a phone from a contact",
    },
    "add-birthday": {
        "preview": "add-birthday <name> <birthday>",
        "description": "Add a birthday to a contact",
    },
    "show-birthday": {
        "preview": "show-birthday <name>",
        "description": "Show the birthday of a contact",
    },
    "birthdays": {
        "preview": "birthdays",
        "description": "Show the birthdays of the next week",
    },
    "help": {
        "preview": "help",
        "description": "Print this message",
    },
    "exit": {
        "preview": "exit",
        "description": "Exit the assistant bot",
    },
    "close": {
        "preview": "close",
        "description": "Exit the assistant bot",
    },
    "bye": {
        "preview": "bye",
        "description": "Exit the assistant bot",
    },
}

TEST_RECORDS = {
    "John": {
        "phones": ["0123456789", "9876543210"],
        "birthday": "17.12.1990"
    },
    "Jane": {
        "phones": ["1234567890"],
        "birthday": None
    },
    "Kate": {
        "phones": ["2345678901"],
        "birthday": "19.12.1990"
    },
    "Alex": {
        "phones": ["3456789012"],
        "birthday": "17.10.1994"
    }
}
    
MOCKED_INPUTS = [
    "hello",
    "all",
    "add",
    "add Mike", # should fail
    "add Mike mike", # should fail
    "add Mike 01234567891234567", # should fail
    "add Mike 01", # should fail
    "add Mike 0123456789",
    "add Mike 9876543210 0123456789", # should fail
    "all",
    "find Mike",
    "find Mike1234", # should fail
    "change Mike", # should fail
    "change Mike 01234564567", # should fail
    "change Mike 0123456789 9876543210",
    "change Mike 0123456789 9876543210", # should fail
    "all",
    "add-phone Mike 1111111111",
    "add-phone Mike mmm", # should fail
    "all",
    "find-phone Mike",
    "find-phone Mike1234", # should fail
    "all",
    "show-birthday Mike", # should fail
    "add-birthday Mike 1990.17.12", # should fail
    "add-birthday Mike 17.12.1990",
    "show-birthday Mike",
    "birthdays",
    "all",
    "delete-phone Mike 01234564567", # should fail
    "delete-phone Mike 1111111111",
    "delete Mike1234", # should fail
    "delete Mike",
    "all",
]
