<script>
	import { createEventDispatcher } from 'svelte';
	import { onMount } from 'svelte';
	
	export let encargado;
	
	const dispatch = createEventDispatcher();
	const API_URL = 'http://localhost:8000/api';
	
	let items = [];
	let tipoItem = 'producto';
	let itemSeleccionado = '';
	let tipoMovimiento = 'ENTRADA';
	let cantidad = '';
	let motivo = '';
	let loading = false;
	let error = '';
	let success = '';
	let advertencia = '';
	let requiereConfirmacion = false;

	const tiposMovimiento = [
		{ value: 'ENTRADA', label: 'Entrada' },
		{ value: 'SALIDA', label: 'Salida' },
		{ value: 'AJUSTE', label: 'Ajuste' },
		{ value: 'PERDIDA', label: 'Pérdida/Daño' }
	];

	onMount(() => {
		cargarItems();
	});

	async function cargarItems() {
		try {
			const endpoint = tipoItem === 'producto' ? 'productos' : 'materias-primas';
			const response = await fetch(`${API_URL}/${endpoint}/`);
			const data = await response.json();
			items = data;
		} catch (err) {
			console.error('Error al cargar items:', err);
		}
	}

	function handleTipoItemChange() {
		itemSeleccionado = '';
		cargarItems();
	}

	async function handleSubmit() {
		error = '';
		success = '';
		advertencia = '';
		loading = true;
		
		if (!itemSeleccionado || !cantidad || !motivo) {
			error = 'Complete todos los campos requeridos';
			loading = false;
			return;
		}

		try {
			const payload = {
				item_id: parseInt(itemSeleccionado),
				item_tipo: tipoItem === 'producto' ? 'producto' : 'materia_prima',
				tipo_movimiento: tipoMovimiento,
				cantidad: parseInt(cantidad),
				motivo: motivo,
				encargado_id: encargado.id,
				confirmar: requiereConfirmacion
			};

			const response = await fetch(`${API_URL}/registrar-movimiento/`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify(payload)
			});
			
			const data = await response.json();
			
			if (response.ok) {
				if (data.requiere_confirmacion) {
					advertencia = data.advertencia;
					requiereConfirmacion = true;
				} else {
					success = `${data.mensaje}\nStock anterior: ${data.stock_anterior} → Stock actual: ${data.stock_actual}`;
					limpiarFormulario();
					dispatch('movimientoRegistrado');
				}
			} else {
				if (data.item_id) {
					error = data.item_id[0];
				} else {
					error = JSON.stringify(data);
				}
			}
		} catch (err) {
			error = 'Error de conexión con el servidor';
			console.error(err);
		} finally {
			loading = false;
		}
	}

	function cancelarConfirmacion() {
		advertencia = '';
		requiereConfirmacion = false;
	}

	function limpiarFormulario() {
		itemSeleccionado = '';
		cantidad = '';
		motivo = '';
		requiereConfirmacion = false;
		advertencia = '';
	}

	$: itemSeleccionadoData = items.find(i => i.id === parseInt(itemSeleccionado));
</script>

<div class="registro-form">
	<form on:submit|preventDefault={handleSubmit}>
		<div class="form-group">
			<label>Tipo de Ítem:</label>
			<div class="radio-group">
				<label class="radio-label">
					<input 
						type="radio" 
						bind:group={tipoItem} 
						value="producto"
						on:change={handleTipoItemChange}
						disabled={loading}
					/>
					Producto
				</label>
				<label class="radio-label">
					<input 
						type="radio" 
						bind:group={tipoItem} 
						value="materia_prima"
						on:change={handleTipoItemChange}
						disabled={loading}
					/>
					Materia Prima
				</label>
			</div>
		</div>

		<div class="form-group">
			<label for="item">Seleccionar Ítem:</label>
			<select id="item" bind:value={itemSeleccionado} required disabled={loading}>
				<option value="">-- Seleccione un ítem --</option>
				{#each items as item}
					<option value={item.id}>
						{item.nombre} (Stock: {item.stock_actual})
					</option>
				{/each}
			</select>
		</div>

		{#if itemSeleccionadoData}
			<div class="item-info">
				<strong>Stock actual:</strong> {itemSeleccionadoData.stock_actual} unidades
				<br>
				<strong>Stock mínimo:</strong> {itemSeleccionadoData.stock_minimo} unidades
			</div>
		{/if}

		<div class="form-group">
			<label for="tipo-movimiento">Tipo de Movimiento:</label>
			<select id="tipo-movimiento" bind:value={tipoMovimiento} required disabled={loading}>
				{#each tiposMovimiento as tipo}
					<option value={tipo.value}>{tipo.label}</option>
				{/each}
			</select>
		</div>

		<div class="form-group">
			<label for="cantidad">Cantidad:</label>
			<input 
				id="cantidad"
				type="number" 
				bind:value={cantidad}
				placeholder="Ingrese la cantidad"
				required
				min="1"
				disabled={loading}
			/>
		</div>

		<div class="form-group">
			<label for="motivo">Motivo:</label>
			<textarea 
				id="motivo"
				bind:value={motivo}
				placeholder="Describa el motivo del movimiento (ej: Faltante en inventario físico, Botellas rotas en línea de producción)"
				required
				rows="3"
				disabled={loading}
			></textarea>
		</div>

		{#if advertencia}
			<div class="warning-message">
				<p><strong>⚠️ Advertencia:</strong></p>
				<p>{advertencia}</p>
				<div class="warning-actions">
					<button type="submit" class="btn-confirm">
						Confirmar de todos modos
					</button>
					<button type="button" class="btn-cancel" on:click={cancelarConfirmacion}>
						Cancelar
					</button>
				</div>
			</div>
		{/if}

		{#if error}
			<div class="error-message">{error}</div>
		{/if}

		{#if success}
			<div class="success-message">{success}</div>
		{/if}

		{#if !advertencia}
			<button type="submit" class="btn-submit" disabled={loading}>
				{loading ? 'Registrando...' : 'Registrar Movimiento'}
			</button>
		{/if}
	</form>
</div>

<style>
	.registro-form {
		width: 100%;
	}
	
	.form-group {
		margin-bottom: 1.25rem;
	}
	
	label {
		display: block;
		margin-bottom: 0.5rem;
		color: #333;
		font-weight: 500;
	}
	
	.radio-group {
		display: flex;
		gap: 1.5rem;
	}
	
	.radio-label {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		cursor: pointer;
		font-weight: 400;
	}
	
	input[type="radio"] {
		cursor: pointer;
	}
	
	select, input, textarea {
		width: 100%;
		padding: 0.625rem;
		border: 2px solid #e0e0e0;
		border-radius: 6px;
		font-size: 0.95rem;
		font-family: inherit;
		transition: border-color 0.3s;
		box-sizing: border-box;
	}
	
	select:focus, input:focus, textarea:focus {
		outline: none;
		border-color: #667eea;
	}
	
	textarea {
		resize: vertical;
	}
	
	.item-info {
		padding: 0.75rem;
		background: #e3f2fd;
		border-left: 4px solid #2196f3;
		border-radius: 4px;
		margin-bottom: 1rem;
		font-size: 0.9rem;
	}
	
	.btn-submit {
		width: 100%;
		padding: 0.875rem;
		background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
		color: white;
		border: none;
		border-radius: 6px;
		font-size: 1rem;
		font-weight: 600;
		cursor: pointer;
		transition: transform 0.2s, box-shadow 0.2s;
	}
	
	.btn-submit:hover:not(:disabled) {
		transform: translateY(-2px);
		box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
	}
	
	.btn-submit:disabled {
		opacity: 0.6;
		cursor: not-allowed;
	}
	
	.error-message {
		background: #fee;
		color: #c33;
		padding: 0.75rem;
		border-radius: 6px;
		margin-bottom: 1rem;
		border-left: 4px solid #c33;
	}
	
	.success-message {
		background: #efe;
		color: #2a7;
		padding: 0.75rem;
		border-radius: 6px;
		margin-bottom: 1rem;
		border-left: 4px solid #2a7;
		white-space: pre-line;
	}
	
	.warning-message {
		background: #fff3cd;
		color: #856404;
		padding: 1rem;
		border-radius: 6px;
		margin-bottom: 1rem;
		border-left: 4px solid #ffc107;
	}
	
	.warning-message p {
		margin: 0.5rem 0;
	}
	
	.warning-actions {
		display: flex;
		gap: 1rem;
		margin-top: 1rem;
	}
	
	.btn-confirm, .btn-cancel {
		flex: 1;
		padding: 0.625rem;
		border: none;
		border-radius: 6px;
		font-weight: 600;
		cursor: pointer;
		transition: opacity 0.2s;
	}
	
	.btn-confirm {
		background: #ffc107;
		color: #000;
	}
	
	.btn-cancel {
		background: #6c757d;
		color: white;
	}
	
	.btn-confirm:hover, .btn-cancel:hover {
		opacity: 0.9;
	}
</style>
