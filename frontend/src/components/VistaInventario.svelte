<script>
	import { onMount } from 'svelte';
	
	export let refresh = 0;
	
	const API_URL = 'http://localhost:8000/api';
	
	let productos = [];
	let materiasPrimas = [];
	let loading = true;

	$: if (refresh >= 0) {
		cargarInventario();
	}

	onMount(() => {
		cargarInventario();
		// Actualizar cada 10 segundos
		const interval = setInterval(cargarInventario, 10000);
		return () => clearInterval(interval);
	});

	async function cargarInventario() {
		loading = true;
		try {
			const [resProductos, resMaterias] = await Promise.all([
				fetch(`${API_URL}/productos/`),
				fetch(`${API_URL}/materias-primas/`)
			]);
			
			productos = await resProductos.json();
			materiasPrimas = await resMaterias.json();
		} catch (err) {
			console.error('Error al cargar inventario:', err);
		} finally {
			loading = false;
		}
	}

	function getStockStatus(item) {
		if (item.stock_actual === 0) return 'sin-stock';
		if (item.stock_actual <= item.stock_minimo) return 'bajo-stock';
		return 'normal';
	}

	function getStockLabel(item) {
		if (item.stock_actual === 0) return 'Sin Stock';
		if (item.stock_actual <= item.stock_minimo) return 'Stock Bajo';
		return 'Normal';
	}
</script>

<div class="inventario">
	{#if loading}
		<div class="loading">Cargando inventario...</div>
	{:else}
		<div class="seccion">
			<h3>📦 Productos ({productos.length})</h3>
			<div class="tabla-container">
				<table>
					<thead>
						<tr>
							<th>Nombre</th>
							<th>Stock Actual</th>
							<th>Stock Mínimo</th>
							<th>Precio</th>
							<th>Estado</th>
						</tr>
					</thead>
					<tbody>
						{#if productos.length === 0}
							<tr>
								<td colspan="5" class="empty">No hay productos registrados</td>
							</tr>
						{:else}
							{#each productos as producto}
								<tr class={getStockStatus(producto)}>
									<td class="nombre">{producto.nombre}</td>
									<td class="stock">{producto.stock_actual}</td>
									<td>{producto.stock_minimo}</td>
									<td>${producto.precio_unitario}</td>
									<td>
										<span class="badge badge-{getStockStatus(producto)}">
											{getStockLabel(producto)}
										</span>
									</td>
								</tr>
							{/each}
						{/if}
					</tbody>
				</table>
			</div>
		</div>

		<div class="seccion">
			<h3>🧪 Materias Primas ({materiasPrimas.length})</h3>
			<div class="tabla-container">
				<table>
					<thead>
						<tr>
							<th>Nombre</th>
							<th>Stock Actual</th>
							<th>Stock Mínimo</th>
							<th>Costo</th>
							<th>Estado</th>
						</tr>
					</thead>
					<tbody>
						{#if materiasPrimas.length === 0}
							<tr>
								<td colspan="5" class="empty">No hay materias primas registradas</td>
							</tr>
						{:else}
							{#each materiasPrimas as materia}
								<tr class={getStockStatus(materia)}>
									<td class="nombre">{materia.nombre}</td>
									<td class="stock">{materia.stock_actual}</td>
									<td>{materia.stock_minimo}</td>
									<td>${materia.costo_unitario}</td>
									<td>
										<span class="badge badge-{getStockStatus(materia)}">
											{getStockLabel(materia)}
										</span>
									</td>
								</tr>
							{/each}
						{/if}
					</tbody>
				</table>
			</div>
		</div>

		<div class="info-actualizado">
			<small>Última actualización: {new Date().toLocaleTimeString()}</small>
		</div>
	{/if}
</div>

<style>
	.inventario {
		width: 100%;
	}
	
	.loading {
		text-align: center;
		padding: 2rem;
		color: #666;
		font-size: 1.1rem;
	}
	
	.seccion {
		margin-bottom: 2rem;
	}
	
	h3 {
		margin: 0 0 1rem 0;
		color: #444;
		font-size: 1.2rem;
		display: flex;
		align-items: center;
		gap: 0.5rem;
	}
	
	.tabla-container {
		overflow-x: auto;
		border-radius: 8px;
		border: 1px solid #e0e0e0;
	}
	
	table {
		width: 100%;
		border-collapse: collapse;
		background: white;
	}
	
	thead {
		background: #f8f9fa;
	}
	
	th {
		padding: 0.875rem;
		text-align: left;
		font-weight: 600;
		color: #555;
		border-bottom: 2px solid #e0e0e0;
		font-size: 0.9rem;
	}
	
	td {
		padding: 0.75rem 0.875rem;
		border-bottom: 1px solid #f0f0f0;
		font-size: 0.9rem;
	}
	
	tbody tr:hover {
		background: #f8f9fa;
	}
	
	.nombre {
		font-weight: 500;
		color: #333;
	}
	
	.stock {
		font-weight: 600;
		font-size: 1rem;
	}
	
	.empty {
		text-align: center;
		color: #999;
		font-style: italic;
		padding: 2rem;
	}
	
	.badge {
		display: inline-block;
		padding: 0.25rem 0.75rem;
		border-radius: 12px;
		font-size: 0.8rem;
		font-weight: 600;
	}
	
	.badge-normal {
		background: #d4edda;
		color: #155724;
	}
	
	.badge-bajo-stock {
		background: #fff3cd;
		color: #856404;
	}
	
	.badge-sin-stock {
		background: #f8d7da;
		color: #721c24;
	}
	
	tr.bajo-stock .stock {
		color: #f57c00;
	}
	
	tr.sin-stock .stock {
		color: #d32f2f;
	}
	
	tr.normal .stock {
		color: #2e7d32;
	}
	
	.info-actualizado {
		text-align: right;
		margin-top: 1rem;
		color: #999;
	}
</style>
