import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use the application default credentials
project_id = 'apptareasflask'
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
  'projectId': project_id,
})

db = firestore.client()

docs = db.collection(u'users').get()

for doc in docs:
    print(doc.to_dict())