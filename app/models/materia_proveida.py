from app.extensions import db


class MateriaProveida(db.Model):

    __tablename__           = 'materia_proveida'
    idMateriaProveida       = db.Column(db.Integer, primary_key=True)
    nombreMateriaProveida   = db.Column(db.String(25), nullable=False)
    idProveedor             = db.Column(db.Integer, db.ForeignKey('proveedor.id'), nullable=False)
    idMateriaPrima          = db.Column(db.Integer, db.ForeignKey('materia_prima.idMateriaPrima'), nullable=False)
    idUnidadMedida          = db.Column(db.Integer, db.ForeignKey('unidad_medida.idUnidadMedida'), nullable=False)

    # Relación inversa definida via backref en MateriaPrimaUnitaria
    # Acceso: materiaProveida.materiasPrimasUnitarias.all()
