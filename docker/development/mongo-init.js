// docker/development/mongo-init.js
// Script de inicialización de MongoDB para desarrollo

// Conectar a la base de datos
db = db.getSiblingDB('portfolio_db');

// Crear colecciones (opcional, se crean automáticamente al insertar)
db.createCollection('profiles');
db.createCollection('contact_information');
db.createCollection('social_networks');
db.createCollection('projects');
db.createCollection('work_experiences');
db.createCollection('education');
db.createCollection('additional_training');
db.createCollection('certifications');
db.createCollection('skills');
db.createCollection('tools');
db.createCollection('contact_messages');

// Crear índices para optimización
db.profiles.createIndex({ "id": 1 }, { unique: true });
db.contact_information.createIndex({ "id": 1 }, { unique: true });
db.social_networks.createIndex({ "order_index": 1 });
db.projects.createIndex({ "order_index": 1 });
db.work_experiences.createIndex({ "order_index": 1 });
db.education.createIndex({ "order_index": 1 });
db.skills.createIndex({ "order_index": 1 });
db.tools.createIndex({ "order_index": 1 });
db.contact_messages.createIndex({ "sent_at": -1 });

print('✅ Base de datos portfolio_db inicializada correctamente');
print('✅ Colecciones e índices creados');