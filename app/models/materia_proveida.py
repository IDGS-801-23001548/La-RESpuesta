from app.extensions import db

class MateriaProveida(db.Model):

    __tablename__       = 'materia_proveida'
    idMateriaProveida   = db.Column(db.Integer, primary_key=True)
    idProveedor         = db.Column(db.Integer, db.ForeignKey('proveedor.id'), nullable=False)
    idMateriaPrima      = db.Column(db.Integer, db.ForeignKey('materia_prima.idMateriaPrima'), nullable=False)
    idUnidadMedida      = db.Column(db.Integer, db.ForeignKey('unidad_medida.idUnidadMedida'), nullable=False)

    ordenesCompra       = db.relationship(
        'OrdenCompra',
        backref='materiaProveida',
        lazy='dynamic'
    )
