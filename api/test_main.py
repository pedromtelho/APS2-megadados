from fastapi.testclient import TestClient
from .main import app
import uuid

client = TestClient(app)


def test_read_main_returns_not_found():
    response = client.get('/')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Not Found'}


def test_get_starter_tasks():
    response = client.get('/task')
    assert response.status_code == 200
    assert response.json() == {
        "44c0c224-6084-48d0-876b-43f30f157014": {
            "description": "Buy food",
            "completed": False
        },
        "953c3c2a-478b-48d7-9631-7b3113a1c4cc": {
            "description": "Finish exercise",
            "completed": False
        }
    }


def test_create_task_and_returns_string():
    response = client.post('/task', json={
        "description": "Finish tasks",
        "completed": False
    })

    assert response.status_code == 200
    assert str(response.content)

    # check if the task has been inserted in the list
    response_get = client.get('/task')
    uuid = response.content.decode('utf-8')[1:-1]
    assert response_get.json()[uuid] == {
        "description": "Finish tasks",
        "completed": False
    }


def test_create_invalid_task_returns_error():
    response = client.post('/task', json={
        "description": 123,
        "completed": 123
    })

    assert response.status_code == 422


def test_read_task_by_uuid():
    response_create = client.post('/task', json={
        "description": "Task description",
        "completed": False
    })

    uuid = response_create.content.decode('utf-8')[1:-1]

    response_read = client.get('/task/{}'.format(uuid))
    assert response_read.status_code == 200
    assert response_read.json() == {
        "description": "Task description",
        "completed": False
    }


def test_read_task_by_invalid_uuid_returns_not_found():
    response_create = client.post('/task', json={
        "description": "Task description",
        "completed": False
    })

    response_read = client.get('/task/{}'.format(uuid.uuid4()))
    assert response_read.status_code == 404
    assert response_read.json() == {'detail': 'Task not found'}


def test_replace_task_by_uuid():
    response_create = client.post('/task', json={
        "description": "Task description",
        "completed": False
    })

    uuid = response_create.content.decode('utf-8')[1:-1]

    response_replace = client.put('/task/{}'.format(uuid), json={
        "description": "Replaced task",
        "completed": False
    })
    assert response_replace.status_code == 200

    # check if the task has been replaced in the list
    response_get = client.get('/task')
    assert response_get.json()[uuid] == {
        "description": "Replaced task",
        "completed": False
    }

def test_delete_task_by_uuid():
    response_create = client.post('/task', json={
        "description": "Task description",
        "completed": False
    })

    uuid = response_create.content.decode('utf-8')[1:-1]

    response_delete = client.delete('/task/{}'.format(uuid))
    assert response_delete.status_code == 200

    # check if the task has been deleted from the list
    response_get = client.get('/task')
    assert not uuid in response_get.json()


def test_delete_task_by_invalid_uuid_returns_not_found():
    response_create = client.post('/task', json={
        "description": "Task description",
        "completed": False
    })

    response_delete = client.delete('/task/{}'.format(uuid.uuid4()))
    assert response_delete.status_code == 404
    assert response_delete.json() == {'detail': 'Task not found'}


def test_alter_task_by_uuid():
    response_create = client.post('/task', json={
        "description": "Task description",
        "completed": False
    })

    uuid = response_create.content.decode('utf-8')[1:-1]

    response_alter = client.patch('/task/{}'.format(uuid), json={
        "description": "Altered task",
        "completed": False
    })
    assert response_alter.status_code == 200
    
    # check if the task has been altered in the list
    response_get = client.get('/task')
    assert response_get.json()[uuid] == {
        "description": "Altered task",
        "completed": False
    }


def test_alter_task_by_invalid_uuid_returns_not_found():
    response_create = client.post('/task', json={
        "description": "Task description",
        "completed": False
    })

    response_alter = client.patch('/task/{}'.format(uuid.uuid4()), json={
        "description": "Altered task",
        "completed": False
    })
    assert response_alter.status_code == 404
    assert response_alter.json() == {'detail': 'Task not found'}

    