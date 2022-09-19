from dynamic_website_reverse_proxy.database import Database



def test_save_and_load(persistent_db):
    """Save something and load it."""
    persistent_db.save(123)
    assert persistent_db.load() == 123


def test_can_not_load_anything(persistent_db):
    assert persistent_db.load() is None


def test_loading_creates_copies(persistent_db):
    l = []
    persistent_db.save(l)
    assert persistent_db.load() is not l


def test_saving_again_uses_new_object(persistent_db):
    persistent_db.save(1)
    persistent_db.save(2)
    assert persistent_db.load() == 2


def test_creating_a_database_with_same_file_loads_same_contents(persistent_db):
    persistent_db2 = Database(persistent_db.file)
    persistent_db.save(1234)
    assert persistent_db2.load() == 1234
    

def test_can_save_functions(persistent_db):
    persistent_db.save(test_can_save_functions)
    assert persistent_db.load() == test_can_save_functions


def test_can_not_load_from_different_version(persistent_db):
    persistent_db.save(123)
    persistent_db.version += 1
    assert persistent_db.load() is None

