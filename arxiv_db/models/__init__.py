"""arXiv database SQLAlchemy models.

## Process to create:
This was generated with sqlacodegen on 2022-09-29 with the declarative
generator against a copy of the production database.

Some of the tables are represented with sqlalchemy tables since the
lack primary keys.

The class names were changed to remove the 'ArXiv' prefix.

Moved tables to associative_tables.py

Split out classes to individual files.

Added some needed imports.
"""

import importlib
import sys

def add_all_models_to_sqlalchemy():
    """Loads all modules in this pacakge.

    For SQLAlchemy ORM to work the model definitions need to be
    defined on the Base. This does that."""

    this_pkg = sys.modules[__name__]
    print(f"This is name {__name__} and pkg {this_pkg}")
    for mod in this_pkg.__loader__.get_resource_reader().contents():
        importlib.import_module(f'arxiv_db.models.{mod.removesuffix(".py")}')
