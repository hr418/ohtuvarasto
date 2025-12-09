import os
from flask import Flask, render_template, request, redirect, url_for, flash
from varasto import Varasto

app = Flask(__name__)
app.secret_key = os.environ.get(
    'SECRET_KEY', 'dev-secret-key-change-in-production'
)

# In-memory storage for warehouses
warehouses = {}
warehouse_id_counter = 1


@app.route('/')
def index():
    """Display list of all warehouses."""
    return render_template('index.html', warehouses=warehouses)


@app.route('/add', methods=['GET', 'POST'])
def add_warehouse():
    """Add a new warehouse."""
    if request.method == 'POST':
        global warehouse_id_counter  # pylint: disable=global-statement
        name = request.form.get('name')
        tilavuus = float(request.form.get('tilavuus', 0))
        alku_saldo = float(request.form.get('alku_saldo', 0))

        warehouse = Varasto(tilavuus, alku_saldo)
        warehouses[warehouse_id_counter] = {
            'name': name,
            'varasto': warehouse
        }
        warehouse_id_counter += 1

        flash(f'Varasto "{name}" lisätty onnistuneesti!', 'success')
        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/edit/<int:warehouse_id>', methods=['GET', 'POST'])
def edit_warehouse(warehouse_id):
    """Edit an existing warehouse."""
    if warehouse_id not in warehouses:
        flash('Varastoa ei löytynyt!', 'error')
        return redirect(url_for('index'))

    if request.method == 'POST':
        return _update_warehouse(warehouse_id)

    return render_template('edit.html',
                         warehouse_id=warehouse_id,
                         warehouse=warehouses[warehouse_id])


def _update_warehouse(warehouse_id):
    """Helper function to update warehouse details."""
    name = request.form.get('name')
    tilavuus = float(request.form.get('tilavuus', 0))

    # Create a new warehouse with updated capacity and current saldo
    old_varasto = warehouses[warehouse_id]['varasto']
    alku_saldo = min(old_varasto.saldo, tilavuus)

    warehouses[warehouse_id]['name'] = name
    warehouses[warehouse_id]['varasto'] = Varasto(tilavuus, alku_saldo)

    flash(f'Varasto "{name}" päivitetty onnistuneesti!', 'success')
    return redirect(url_for('index'))


@app.route('/add_content/<int:warehouse_id>', methods=['POST'])
def add_content(warehouse_id):
    """Add content to a warehouse."""
    if warehouse_id not in warehouses:
        flash('Varastoa ei löytynyt!', 'error')
        return redirect(url_for('index'))

    maara = float(request.form.get('maara', 0))
    warehouses[warehouse_id]['varasto'].lisaa_varastoon(maara)

    flash(f'Lisättiin {maara} yksikköä varastoon!', 'success')
    return redirect(url_for('index'))


@app.route('/remove_content/<int:warehouse_id>', methods=['POST'])
def remove_content(warehouse_id):
    """Remove content from a warehouse."""
    if warehouse_id not in warehouses:
        flash('Varastoa ei löytynyt!', 'error')
        return redirect(url_for('index'))

    maara = float(request.form.get('maara', 0))
    otettu = warehouses[warehouse_id]['varasto'].ota_varastosta(maara)

    flash(f'Otettiin {otettu} yksikköä varastosta!', 'success')
    return redirect(url_for('index'))


@app.route('/delete/<int:warehouse_id>', methods=['POST'])
def delete_warehouse(warehouse_id):
    """Delete a warehouse."""
    if warehouse_id in warehouses:
        name = warehouses[warehouse_id]['name']
        del warehouses[warehouse_id]
        flash(f'Varasto "{name}" poistettu!', 'success')
    else:
        flash('Varastoa ei löytynyt!', 'error')

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
