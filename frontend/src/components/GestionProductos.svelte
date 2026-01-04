<script>
	import { onMount } from 'svelte';
	
	const API_URL = 'http://localhost:8000/api';
	
	let tipoItem = 'producto'; // 'producto' o 'materia_prima'
	let items = [];
	let loading = false;
	let error = '';
	let success = '';
	
	// Formulario
	let modoEdicion = false;
	let itemEditando = null;
	let formData = {
		nombre: '',
		descripcion: '',
		stock_actual: 0,
		stock_minimo: 0,
        costo_unitario: 0
	};
	
	onMount(() => {
		cargarItems();
	});
	
	async function cargarItems() {
		loading = true;
		error = '';
		try {
			const endpoint = tipoItem === 'producto' ? 'productos' : 'materias-primas';
			const response = await fetch(`${API_URL}/${endpoint}/`);
			if (!response.ok) throw new Error('Error al cargar items');
			items = await response.json();
		} catch (err) {
			error = 'Error al cargar los items: ' + err.message;
		} finally {
			loading = false;
		}
	}
	
	function handleTipoItemChange() {
		cargarItems();
		limpiarFormulario();
	}
	
	function limpiarFormulario() {
		modoEdicion = false;
		itemEditando = null;
		formData = {
			nombre: '',
			descripcion: '',
			stock_actual: 0,
			stock_minimo: 0,
			costo_unitario: 0
		};
		error = '';
		success = '';
	}
	
	function editarItem(item) {
		modoEdicion = true;
		itemEditando = item;
		formData = {
			nombre: item.nombre,
			descripcion: item.descripcion || '',
			stock_actual: item.stock_actual,
			stock_minimo: item.stock_minimo,
			costo_unitario: item.costo_unitario || 0
		};
		error = '';
		success = '';
	}
	
	async function guardarItem() {
		error = '';
		success = '';
		loading = true;
		
		try {
			const endpoint = tipoItem === 'producto' ? 'productos' : 'materias-primas';
			const url = modoEdicion 
				? `${API_URL}/${endpoint}/${itemEditando.id}/`
				: `${API_URL}/${endpoint}/`;
			
			const method = modoEdicion ? 'PUT' : 'POST';
			
			const response = await fetch(url, {
				method: method,
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify(formData)
			});
			
			if (!response.ok) {
				const errorData = await response.json();
				throw new Error(JSON.stringify(errorData));
			}
			
			success = modoEdicion 
				? 'Item actualizado exitosamente' 
				: 'Item creado exitosamente';
			
			await cargarItems();
			limpiarFormulario();
		} catch (err) {
			error = 'Error al guardar: ' + err.message;
		} finally {
			loading = false;
		}
	}
	
	async function eliminarItem(item) {
		if (!confirm(`¿Está seguro de eliminar "${item.nombre}"?`)) {
			return;
		}
		
		error = '';
		success = '';
		loading = true;
		
		try {
			const endpoint = tipoItem === 'producto' ? 'productos' : 'materias-primas';
			const response = await fetch(`${API_URL}/${endpoint}/${item.id}/`, {
				method: 'DELETE'
			});
			
			if (!response.ok) throw new Error('Error al eliminar');
			
			success = 'Item eliminado exitosamente';
			await cargarItems();
		} catch (err) {
			error = 'Error al eliminar: ' + err.message;
		} finally {
			loading = false;
		}
	}
</script>

<div class="gestion-container">
	<div class="header-section">
		<h2>Gestión de {tipoItem === 'producto' ? 'Productos' : 'Materias Primas'}</h2>
		<div class="tipo-selector">
			<label>
				<input 
					type="radio" 
					bind:group={tipoItem} 
					value="producto"
					on:change={handleTipoItemChange}
				/>
				Productos
			</label>
			<label>
				<input 
					type="radio" 
					bind:group={tipoItem} 
					value="materia_prima"
					on:change={handleTipoItemChange}
				/>
				Materias Primas
			</label>
		</div>
	</div>
	
	{#if error}
		<div class="alert alert-error">{error}</div>
	{/if}
	
	{#if success}
		<div class="alert alert-success">{success}</div>
	{/if}
	
	<div class="content-grid">
		<!-- Formulario -->
		<div class="form-section">
			<h3>{modoEdicion ? 'Editar' : 'Crear Nuevo'}</h3>
			<form on:submit|preventDefault={guardarItem}>
				<div class="form-group">
					<label for="nombre">Nombre *</label>
					<input 
						type="text" 
						id="nombre"
						bind:value={formData.nombre}
						required
					/>
				</div>
				
				<div class="form-group">
					<label for="descripcion">Descripción</label>
					<textarea 
						id="descripcion"
						bind:value={formData.descripcion}
						rows="3"
					></textarea>
				</div>
				
				<div class="form-group">
					<label for="costo_unitario">Costo Unitario/Precio *</label>
					<input 
						type="number" 
						id="costo_unitario"
						bind:value={formData.costo_unitario}
						min="0"
						step="0.01"
						required
					/>
				</div>
				
				<div class="form-row">
					<div class="form-group">
						<label for="stock_actual">Stock Actual *</label>
						<input 
							type="number" 
							id="stock_actual"
							bind:value={formData.stock_actual}
							min="0"
							required
						/>
					</div>
					
					<div class="form-group">
						<label for="stock_minimo">Stock Mínimo *</label>
						<input 
							type="number" 
							id="stock_minimo"
							bind:value={formData.stock_minimo}
							min="0"
							required
						/>
					</div>
				</div>
				
				
				<div class="form-actions">
					<button type="submit" class="btn btn-primary" disabled={loading}>
						{modoEdicion ? '💾 Actualizar' : '➕ Crear'}
					</button>
					
					{#if modoEdicion}
						<button type="button" class="btn btn-secondary" on:click={limpiarFormulario}>
							❌ Cancelar
						</button>
					{/if}
				</div>
			</form>
		</div>
		
		<!-- Lista de items -->
		<div class="list-section">
			<h3>Lista de {tipoItem === 'producto' ? 'Productos' : 'Materias Primas'}</h3>
			
			{#if loading}
				<div class="loading">Cargando...</div>
			{:else if items.length === 0}
				<div class="empty-state">
					No hay {tipoItem === 'producto' ? 'productos' : 'materias primas'} registrados
				</div>
			{:else}
				<div class="items-list">
					{#each items as item (item.id)}
						<div class="item-card" class:stock-bajo={item.stock_actual <= item.stock_minimo}>
							<div class="item-header">
								<h4>{item.nombre}</h4>
								<div class="item-actions">
									<button 
										class="btn-icon btn-edit" 
										on:click={() => editarItem(item)}
										title="Editar"
									>
										✏️
									</button>
									<button 
										class="btn-icon btn-delete" 
										on:click={() => eliminarItem(item)}
										title="Eliminar"
									>
										🗑️
									</button>
								</div>
							</div>
							
							{#if item.descripcion}
								<p class="item-descripcion">{item.descripcion}</p>
							{/if}
							
							<div class="item-stock">
								<div class="stock-info">
									<span class="label">Stock:</span>
									<span class="value">{item.stock_actual}</span>
								</div>
								<div class="stock-info">
									<span class="label">Mínimo:</span>
									<span class="value">{item.stock_minimo}</span>
								</div>
								<div class="stock-info">
									<span class="label">Precio:</span>
									<span class="value precio">${item.costo_unitario ? item.costo_unitario.toFixed(2) : '0.00'}</span>
								</div>
							</div>
							
							{#if item.stock_actual <= item.stock_minimo}
								<div class="stock-warning">
									⚠️ Stock bajo o agotado
								</div>
							{/if}
						</div>
					{/each}
				</div>
			{/if}
		</div>
	</div>
</div>

<style>
	.gestion-container {
		padding: 1rem;
	}
	
	.header-section {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 1.5rem;
	}
	
	.header-section h2 {
		margin: 0;
		color: #333;
	}
	
	.tipo-selector {
		display: flex;
		gap: 1rem;
		background: #f8f9fa;
		padding: 0.5rem 1rem;
		border-radius: 8px;
	}
	
	.tipo-selector label {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		cursor: pointer;
		font-weight: 500;
	}
	
	.tipo-selector input[type="radio"] {
		cursor: pointer;
	}
	
	.alert {
		padding: 1rem;
		border-radius: 8px;
		margin-bottom: 1rem;
	}
	
	.alert-error {
		background: #fee;
		color: #c33;
		border: 1px solid #fcc;
	}
	
	.alert-success {
		background: #efe;
		color: #3c3;
		border: 1px solid #cfc;
	}
	
	.content-grid {
		display: grid;
		grid-template-columns: 1fr 1.5fr;
		gap: 2rem;
	}
	
	.form-section, .list-section {
		background: white;
		padding: 1.5rem;
		border-radius: 12px;
		box-shadow: 0 2px 8px rgba(0,0,0,0.1);
	}
	
	.form-section h3, .list-section h3 {
		margin: 0 0 1.5rem 0;
		color: #667eea;
		font-size: 1.25rem;
		border-bottom: 2px solid #667eea;
		padding-bottom: 0.5rem;
	}
	
	.form-group {
		margin-bottom: 1rem;
	}
	
	.form-group label {
		display: block;
		margin-bottom: 0.5rem;
		font-weight: 500;
		color: #555;
	}
	
	.form-group input,
	.form-group textarea {
		width: 100%;
		padding: 0.75rem;
		border: 1px solid #ddd;
		border-radius: 6px;
		font-size: 1rem;
		font-family: inherit;
	}
	
	.form-group input:focus,
	.form-group textarea:focus {
		outline: none;
		border-color: #667eea;
		box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
	}
	
	.form-row {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 1rem;
	}
	
	.form-actions {
		display: flex;
		gap: 0.5rem;
		margin-top: 1.5rem;
	}
	
	.btn {
		padding: 0.75rem 1.5rem;
		border: none;
		border-radius: 6px;
		font-size: 1rem;
		font-weight: 500;
		cursor: pointer;
		transition: all 0.3s;
	}
	
	.btn-primary {
		background: #667eea;
		color: white;
	}
	
	.btn-primary:hover:not(:disabled) {
		background: #5568d3;
		transform: translateY(-1px);
		box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
	}
	
	.btn-primary:disabled {
		opacity: 0.6;
		cursor: not-allowed;
	}
	
	.btn-secondary {
		background: #6c757d;
		color: white;
	}
	
	.btn-secondary:hover {
		background: #5a6268;
	}
	
	.loading {
		text-align: center;
		padding: 2rem;
		color: #667eea;
		font-weight: 500;
	}
	
	.empty-state {
		text-align: center;
		padding: 2rem;
		color: #999;
	}
	
	.items-list {
		display: flex;
		flex-direction: column;
		gap: 1rem;
		max-height: 600px;
		overflow-y: auto;
	}
	
	.item-card {
		padding: 1rem;
		border: 1px solid #e0e0e0;
		border-radius: 8px;
		transition: all 0.3s;
	}
	
	.item-card:hover {
		box-shadow: 0 4px 12px rgba(0,0,0,0.1);
		transform: translateY(-2px);
	}
	
	.item-card.stock-bajo {
		border-color: #ff9800;
		background: #fff8f0;
	}
	
	.item-header {
		display: flex;
		justify-content: space-between;
		align-items: start;
		margin-bottom: 0.5rem;
	}
	
	.item-header h4 {
		margin: 0;
		color: #333;
		font-size: 1.1rem;
	}
	
	.item-actions {
		display: flex;
		gap: 0.5rem;
	}
	
	.btn-icon {
		background: none;
		border: none;
		font-size: 1.2rem;
		cursor: pointer;
		padding: 0.25rem;
		transition: transform 0.2s;
	}
	
	.btn-icon:hover {
		transform: scale(1.2);
	}
	
	.item-descripcion {
		color: #666;
		font-size: 0.9rem;
		margin: 0.5rem 0;
	}
	
	.item-stock {
		display: flex;
		gap: 2rem;
		margin-top: 0.75rem;
	}
	
	.stock-info {
		display: flex;
		gap: 0.5rem;
		align-items: center;
	}
	
	.stock-info .label {
		color: #666;
		font-size: 0.9rem;
	}
	
	.stock-info .value {
		font-weight: 600;
		color: #333;
	}
	
	.stock-info .value.precio {
		color: #667eea;
		font-weight: 700;
	}
	
	.stock-warning {
		margin-top: 0.75rem;
		padding: 0.5rem;
		background: #fff3cd;
		border: 1px solid #ffc107;
		border-radius: 4px;
		color: #856404;
		font-size: 0.9rem;
		text-align: center;
	}
	
	@media (max-width: 1024px) {
		.content-grid {
			grid-template-columns: 1fr;
		}
		
		.header-section {
			flex-direction: column;
			gap: 1rem;
			align-items: stretch;
		}
		
		.tipo-selector {
			justify-content: center;
		}
	}
</style>
