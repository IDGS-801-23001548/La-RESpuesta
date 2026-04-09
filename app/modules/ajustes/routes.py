from flask import render_template, redirect, url_for, flash, request, render_template, make_response
from . import ajustes
from app.extensions import db
from flask_security.decorators import roles_required
import csv
import io
from datetime import datetime
from pathlib import Path
from flask_login import login_required
from flask_security import roles_required
import subprocess
import os
from .forms import ImportForm, RestoreForm
from werkzeug.utils import secure_filename
from sqlalchemy import text


DB_USER         = os.getenv('DB_USER')
DB_PASSWORD     = os.getenv('DB_PASSWORD')
DB_HOST         = os.getenv('DB_HOST')
DB_NAME         = os.getenv('DB_NAME')

@ajustes.route("/ajustes", methods = ['GET'])
@login_required
@roles_required('admin')
def vista_ajustes():

    restore_form = RestoreForm()
    import_form = ImportForm()

    return render_template(
        "admin/ajustes/ajustes.html",
        restore_form=restore_form,
        import_form=import_form
    )

# --------------------- BACKUP -----------------------------------
@ajustes.route("/backup", methods=["GET"])
@login_required
@roles_required('admin')
def backup():

    filename = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"
    filepath = Path("temp") / filename
    filepath.parent.mkdir(exist_ok=True)

    comando = [
        r"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqldump.exe",
        "-h", DB_HOST,
        "-u", DB_USER,
        f"-p{DB_PASSWORD}",
        DB_NAME
    ]

    with open(filepath, "w", encoding="utf-8") as f:
        subprocess.run(comando, stdout=f)

    response = make_response(open(filepath, "rb").read())
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    response.headers["Content-Type"] = "application/sql"

    return response

# --------------------- RESTORE -----------------------------------
@ajustes.route("/restore", methods=["POST"])
@login_required
@roles_required('admin')
def restore():

    form = RestoreForm()

    if form.validate_on_submit():

        file = form.file.data
        filename = secure_filename(file.filename)

        if not filename.endswith(".sql"):
            flash("Formato inválido. Solo se permiten archivos .sql", "danger")
            return redirect(url_for("ajustes.vista_ajustes"))

        filepath = Path("temp") / filename
        file.save(filepath)

        try:
            comando = [
                r"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe",
                "-h", DB_HOST,
                "-u", DB_USER,
                f"-p{DB_PASSWORD}",
                DB_NAME
            ]

            with open(filepath, "rb") as f:
                subprocess.run(comando, stdin=f, check=True)

            flash("Base de datos restaurada correctamente", "success")

        except Exception as e:
            flash(f"Error al restaurar: {str(e)}", "danger")

    else:
        flash("Archivo inválido o faltante", "danger")

    return redirect(url_for("ajustes.vista_ajustes"))

# --------------------- EXPORT -----------------------------------
TABLAS_PERMITIDAS = ["user", "producto", "categoria", "conversor", "unidad_medida", "Categoria", "corte"]

@ajustes.route("/export/<tabla>", methods=["GET"])
@login_required
@roles_required('admin')
def export_tabla(tabla):

    if tabla not in TABLAS_PERMITIDAS:
        flash("Tabla no permitida", "danger")
        return redirect(url_for("ajustes.vista_ajustes"))

    resultado = db.session.execute(text(f"SELECT * FROM {tabla}"))
    filas = resultado.fetchall()

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(resultado.keys())

    for fila in filas:
        writer.writerow(fila)

    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = f"attachment; filename={tabla}.csv"
    response.headers["Content-Type"] = "text/csv"

    flash(f"Exportación de '{tabla}' completada", "success")

    return response

# --------------------- IMPORT -----------------------------------
@ajustes.route("/import", methods=["POST"])
@login_required
@roles_required('admin')
def import_tabla():

    form = ImportForm()

    if form.validate_on_submit():

        file = form.file.data
        tabla = form.tabla.data
        filename = secure_filename(file.filename)

        if not filename.endswith(".csv"):
            flash("Formato inválido. Solo CSV", "danger")
            return redirect(url_for("ajustes.vista_ajustes"))

        try:
            stream = io.StringIO(file.stream.read().decode("UTF-8"))
            reader = csv.reader(stream)

            columnas = next(reader)

            # 🔹 Validar columnas contra la tabla
            columnas_db = db.session.execute(
                text(f"SHOW COLUMNS FROM {tabla}")
            ).fetchall()

            columnas_db = [col[0] for col in columnas_db]

            if not all(col in columnas_db for col in columnas):
                flash("El CSV no corresponde a la tabla seleccionada", "danger")
                return redirect(url_for("ajustes.vista_ajustes"))

            count = 0

            for row in reader:

                if len(row) != len(columnas):
                    flash("Error en formato del CSV", "danger")
                    return redirect(url_for("ajustes.vista_ajustes"))

                data = dict(zip(columnas, row))

                columnas_sql = ", ".join(columnas)
                placeholders = ", ".join([f":{col}" for col in columnas])

                query = text(f"INSERT INTO {tabla} ({columnas_sql}) VALUES ({placeholders})")

                db.session.execute(query, data)
                count += 1

            db.session.commit()

            flash(f"Importación exitosa: {count} registros insertados", "success")

        except Exception as e:
            db.session.rollback()
            print("ERROR IMPORT:", e)
            flash("Error al importar el archivo. Verifica estructura y datos.", "danger")

    else:
        flash("Formulario inválido", "danger")

    return redirect(url_for("ajustes.vista_ajustes"))