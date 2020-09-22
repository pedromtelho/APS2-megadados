class DBSession:
    tasks = {
        "44c0c224-6084-48d0-876b-43f30f157014": {
            "description": "Buy food",
            "completed": False
        },
        "953c3c2a-478b-48d7-9631-7b3113a1c4cc": {
            "description": "Finish exercise",
            "completed": False
        }
    }

    def __init__(self):
        self.tasks = DBSession.tasks


def get_db():
    return DBSession()
