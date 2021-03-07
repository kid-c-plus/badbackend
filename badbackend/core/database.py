class Database:
    """Defines a simplified interface for accessing data items for
    services and users. Services register their needed items as
    SQLAlchemy objects in the `getDatabaseAccess` method, which will
    then return a generated DatabaseAccess object with CRUD methods
    for their specified data points."""

    # TODO: Implement Database class
