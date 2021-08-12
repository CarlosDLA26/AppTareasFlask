import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Comunicamos con la base de datos o la aplicacion por default con Google cloud SDK
project_id = 'apptareasflask'
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
  'projectId': project_id,
})

db = firestore.client()

def get_users():
    return db.collection(u'users').get()

def get_todos(user_id):
    return db.collection(u'users').document(user_id)\
        .collection(u'todos').get()

def get_user(user_id):
    return db.collection(u'users').document(user_id).get()

def register_user(user_id, password):
    doc_ref = db.collection(u'users').document(user_id)
    doc_ref.set({
        'password': password
    })

def register_todo(user_id, description):
    todo_colelction_ref = db.collection(u'users').document(user_id).collection('todos')
    # Añadir un todo con un id aleatorio
    todo_colelction_ref.add({
        'descripcion': description,
        'done': False
    })

def delete_todo(user_id, todo_id):
    todo_ref = db.document('users/{}/todos/{}'.format(user_id, todo_id))
    todo_ref.delete()

def set_state(user_id, todo_id, state):
    todo_ref = db.document(f'users/{user_id}/todos/{todo_id}')
    todo_ref.update({
        'done': not bool(state),
    })