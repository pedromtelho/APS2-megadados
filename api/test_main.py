from fastapi.testclient import TestClient
from .main import app
import uuid

client = TestClient(app)


def test_read_main_returns_not_found():
    response = client.get('/')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Not Found'}


def test_get_tasks():
    response = client.get('/task')
    assert response.status_code == 200
    assert response.json() == {}


def test_create_task_returns_string():
    response = client.post('/task', json={
        "description": "Buy baby diapers",
        "completed": False
    })

    assert response.status_code == 200
    assert str(response.content)


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

    uuid = response_create.content.decode('utf-8')

    response_read = client.get('/task/{}'.format(uuid[1:-1]))
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

    uuid = response_create.content.decode('utf-8')

    response_replace = client.put('/task/{}'.format(uuid[1:-1]), json={
        "description": "Replaced task",
        "completed": False
    })
    assert response_replace.status_code == 200


def test_delete_task_by_uuid():
    response_create = client.post('/task', json={
        "description": "Task description",
        "completed": False
    })

    uuid = response_create.content.decode('utf-8')

    response_delete = client.delete('/task/{}'.format(uuid[1:-1]))
    assert response_delete.status_code == 200


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

    uuid = response_create.content.decode('utf-8')

    response_alter = client.patch('/task/{}'.format(uuid[1:-1]), json={
        "description": "Altered task",
        "completed": False
    })
    assert response_alter.status_code == 200


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
