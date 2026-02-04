<script>
	import { onMount } from 'svelte';
	import { createEventDispatcher } from 'svelte';
	
	const dispatch = createEventDispatcher();
	const API_URL = 'http://localhost:8000/api';
	
	let estadoInventario = null;
	let loading = false;
	let error = '';
	let success = '';
	let loadingSnapshot = false;
	let loadingRestore = false;
	let mostrarConfirmacion = false;

	onMount(() => {
		cargarEstadoInventario();
	});

	async function cargarEstadoInventario() {
		loading = true;
		error = '';
		try {
			const response = await fetch(`${API_URL}/estado-inventario/`);
			const data = await response.json();
			
			if (response.ok) {
				estadoInventario = data;
			} else {
				error = data.error || 'Error al cargar estado del inventario';
			}
		} catch (err) {
			error = 'Error de conexión con el servidor';
			console.error(err);
		} finally {
			loading = false;
		}
	}

	async function guardarSnapshot() {
		loadingSnapshot = true;
		error = '';
		success = '';
		try {
			const response = await fetch(`${API_URL}/guardar-estado/`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				}
			});
			
			const data = await response.json();
			
			if (response.ok) {
				success = `✅ ${data.mensaje}\n🎯 Patrón usado: ${data.patron_usado}`;
				setTimeout(() => {
					success = '';
				}, 5000);
			} else {
				error = data.error || 'Error al guardar snapshot';
			}
		} catch (err) {
			error = 'Error de conexión con el servidor';
			console.error(err);
		} finally {
			loadingSnapshot = false;
		}
	}

	async function restaurarEstado() {
		mostrarConfirmacion = true;
	}

	async function confirmarRestauracion() {
		mostrarConfirmacion = false;
		loadingRestore = true;
		error = '';
		success = '';
		try {
			const response = await fetch(`${API_URL}/restaurar-estado/`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				}
			});
			
			const data = await response.json();
			
			if (response.ok) {
				success = `✅ ${data.mensaje}\n🎯 Patrón usado: ${data.patron_usado}`;
				// Recargar datos
				await cargarEstadoInventario();
				dispatch('estadoRestaurado');
				setTimeout(() => {
					success = '';
				}, 5000);
			} else {
				error = data.error || 'Error al restaurar estado';
			}
		} catch (err) {
			error = 'Error de conexión con el servidor';
			console.error(err);
		} finally {
			loadingRestore = false;
		}
	}

	function cancelarRestauracion() {
		mostrarConfirmacion = false;
	}
</script>

<div class="estado-inventario">
	<div class="header">
		<h2>📊 Estado del Inventario</h2>
		<button class="btn-refresh" on:click={cargarEstadoInventario} disabled={loading}>
			🔄 Actualizar
		</button>
	</div>

	{#if loading}
		<div class="loading">Cargando información del inventario...</div>
	{/if}

	{#if error}
		<div class="error-message">{error}</div>
	{/if}

	{#if success}
		<div class="success-message">{success}</div>
	{/if}

	{#if estadoInventario && !loading}
		<div class="info-general">
			<div class="info-card">
				<h3>📍 Información General</h3>
				<p><strong>Ubicación:</strong> {estadoInventario.ubicacion}</p>
				<p><strong>Capacidad Máxima:</strong> {estadoInventario.capacidad_maxima} unidades</p>
				<p><strong>Última Revisión:</strong> {new Date(estadoInventario.fecha_ultima_revision).toLocaleDateString()}</p>
			</div>
		</div>

		<div class="estadisticas">
			<div class="stat-card">
				<div class="stat-icon">🧪</div>
				<div class="stat-info">
					<h4>Materias Primas</h4>
					<p class="stat-number">{estadoInventario.estadisticas.total_tipos_materias_primas}</p>
					<p class="stat-label">Tipos diferentes</p>
					<p class="stat-stock">Stock total: {estadoInventario.estadisticas.stock_total_materias_primas}</p>
				</div>
			</div>

			<div class="stat-card">
				<div class="stat-icon">📦</div>
				<div class="stat-info">
					<h4>Productos</h4>
					<p class="stat-number">{estadoInventario.estadisticas.total_tipos_productos}</p>
					<p class="stat-label">Tipos diferentes</p>
					<p class="stat-stock">Stock total: {estadoInventario.estadisticas.stock_total_productos}</p>
				</div>
			</div>

			<div class="stat-card">
				<div class="stat-icon">📈</div>
				<div class="stat-info">
					<h4>Total General</h4>
					<p class="stat-number">{estadoInventario.estadisticas.total_tipos_materias_primas + estadoInventario.estadisticas.total_tipos_productos}</p>
					<p class="stat-label">Tipos de ítems</p>
					<p class="stat-stock">Stock: {estadoInventario.estadisticas.stock_total_materias_primas + estadoInventario.estadisticas.stock_total_productos}</p>
				</div>
			</div>
		</div>

		<!-- Sección Memento -->
		<div class="memento-section">
			<h3>💾 Gestión de Estados (Patrón Memento)</h3>
			<p class="memento-description">
				Utiliza el patrón Memento para crear snapshots del inventario y restaurar estados anteriores.
				Útil para auditoría y recuperación de datos.
			</p>
			
			<div class="memento-actions">
				<button 
					class="btn-snapshot" 
					on:click={guardarSnapshot}
					disabled={loadingSnapshot}
				>
					{#if loadingSnapshot}
						⏳ Guardando...
					{:else}
						💾 Guardar Snapshot
					{/if}
				</button>

				<button 
					class="btn-restore" 
					on:click={restaurarEstado}
					disabled={loadingRestore}
				>
					{#if loadingRestore}
						⏳ Restaurando...
					{:else}
						↩️ Restaurar Estado Anterior
					{/if}
				</button>
			</div>

			<div class="memento-info">
				<p><strong>ℹ️ Información:</strong></p>
				<ul>
					<li><strong>Guardar Snapshot:</strong> Crea un respaldo del estado actual del inventario</li>
					<li><strong>Restaurar Estado:</strong> Recupera el último estado guardado (ubicación, capacidad, fecha de revisión)</li>
					<li>Los snapshots se gestionan en memoria durante la sesión actual</li>
				</ul>
			</div>
		</div>
	{/if}
</div>

<!-- Modal de Confirmación -->
{#if mostrarConfirmacion}
	<!-- svelte-ignore a11y-click-events-have-key-events -->
	<!-- svelte-ignore a11y-no-static-element-interactions -->
	<div class="modal-overlay" on:click={cancelarRestauracion}>
		<!-- svelte-ignore a11y-click-events-have-key-events -->
		<!-- svelte-ignore a11y-no-static-element-interactions -->
		<div class="modal-content" on:click|stopPropagation>
			<div class="modal-header">
				<h3>⚠️ Confirmar Restauración</h3>
			</div>
			<div class="modal-body">
				<p>¿Estás seguro de que deseas restaurar el inventario al estado anterior?</p>
				<p class="modal-warning">Esta acción modificará los stocks actuales de todos los ítems y no se puede deshacer.</p>
			</div>
			<div class="modal-actions">
				<button class="btn-modal-cancel" on:click={cancelarRestauracion}>
					Cancelar
				</button>
				<button class="btn-modal-confirm" on:click={confirmarRestauracion}>
					Confirmar Restauración
				</button>
			</div>
		</div>
	</div>
{/if}

<style>
	.estado-inventario {
		padding: 1.5rem;
		background: white;
		border-radius: 8px;
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
	}

	.header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 1.5rem;
		padding-bottom: 1rem;
		border-bottom: 2px solid #f0f0f0;
	}

	.header h2 {
		margin: 0;
		color: #333;
	}

	.btn-refresh {
		padding: 0.5rem 1rem;
		background: #667eea;
		color: white;
		border: none;
		border-radius: 6px;
		cursor: pointer;
		font-weight: 600;
		transition: all 0.3s;
	}

	.btn-refresh:hover:not(:disabled) {
		background: #5568d3;
		transform: translateY(-2px);
	}

	.btn-refresh:disabled {
		opacity: 0.6;
		cursor: not-allowed;
	}

	.loading {
		text-align: center;
		padding: 2rem;
		color: #666;
		font-style: italic;
	}

	.error-message {
		background: #fee;
		color: #c33;
		padding: 1rem;
		border-radius: 6px;
		margin-bottom: 1rem;
		border-left: 4px solid #c33;
	}

	.success-message {
		background: #efe;
		color: #2a7;
		padding: 1rem;
		border-radius: 6px;
		margin-bottom: 1rem;
		border-left: 4px solid #2a7;
		white-space: pre-line;
	}

	.info-general {
		margin-bottom: 2rem;
	}

	.info-card {
		background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
		color: white;
		padding: 1.5rem;
		border-radius: 8px;
	}

	.info-card h3 {
		margin: 0 0 1rem 0;
	}

	.info-card p {
		margin: 0.5rem 0;
	}

	.estadisticas {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
		gap: 1.5rem;
		margin-bottom: 2rem;
	}

	.stat-card {
		background: #f8f9fa;
		padding: 1.5rem;
		border-radius: 8px;
		display: flex;
		gap: 1rem;
		transition: transform 0.3s, box-shadow 0.3s;
	}

	.stat-card:hover {
		transform: translateY(-5px);
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
	}

	.stat-icon {
		font-size: 3rem;
		line-height: 1;
	}

	.stat-info {
		flex: 1;
	}

	.stat-info h4 {
		margin: 0 0 0.5rem 0;
		color: #333;
		font-size: 1rem;
	}

	.stat-number {
		font-size: 2.5rem;
		font-weight: 700;
		color: #667eea;
		margin: 0;
		line-height: 1;
	}

	.stat-label {
		margin: 0.25rem 0;
		color: #666;
		font-size: 0.85rem;
	}

	.stat-stock {
		margin: 0.5rem 0 0 0;
		color: #2a7;
		font-weight: 600;
		font-size: 0.9rem;
	}

	.memento-section {
		background: linear-gradient(135deg, #fff9e6 0%, #ffe9f0 100%);
		padding: 1.5rem;
		border-radius: 8px;
		border-left: 6px solid #ff6b6b;
	}

	.memento-section h3 {
		margin: 0 0 1rem 0;
		color: #333;
	}

	.memento-description {
		margin-bottom: 1.5rem;
		color: #555;
		line-height: 1.6;
	}

	.memento-actions {
		display: flex;
		gap: 1rem;
		margin-bottom: 1.5rem;
		flex-wrap: wrap;
	}

	.btn-snapshot, .btn-restore {
		flex: 1;
		min-width: 200px;
		padding: 1rem 1.5rem;
		border: none;
		border-radius: 6px;
		font-weight: 600;
		font-size: 1rem;
		cursor: pointer;
		transition: all 0.3s;
	}

	.btn-snapshot {
		background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
		color: white;
	}

	.btn-snapshot:hover:not(:disabled) {
		transform: translateY(-2px);
		box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
	}

	.btn-restore {
		background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
		color: white;
	}

	.btn-restore:hover:not(:disabled) {
		transform: translateY(-2px);
		box-shadow: 0 4px 12px rgba(245, 87, 108, 0.4);
	}

	.btn-snapshot:disabled, .btn-restore:disabled {
		opacity: 0.6;
		cursor: not-allowed;
	}

	.memento-info {
		background: white;
		padding: 1rem;
		border-radius: 6px;
		font-size: 0.9rem;
	}

	.memento-info p {
		margin: 0 0 0.5rem 0;
		font-weight: 600;
	}

	.memento-info ul {
		margin: 0.5rem 0 0 0;
		padding-left: 1.5rem;
	}

	.memento-info li {
		margin: 0.5rem 0;
		color: #555;
		line-height: 1.5;
	}

	/* Modal de Confirmación */
	.modal-overlay {
		position: fixed;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background: rgba(0, 0, 0, 0.6);
		display: flex;
		justify-content: center;
		align-items: center;
		z-index: 1000;
		animation: fadeIn 0.2s ease-out;
	}

	@keyframes fadeIn {
		from {
			opacity: 0;
		}
		to {
			opacity: 1;
		}
	}

	.modal-content {
		background: white;
		border-radius: 12px;
		max-width: 500px;
		width: 90%;
		box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
		animation: slideUp 0.3s ease-out;
	}

	@keyframes slideUp {
		from {
			transform: translateY(50px);
			opacity: 0;
		}
		to {
			transform: translateY(0);
			opacity: 1;
		}
	}

	.modal-header {
		background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
		color: white;
		padding: 1.5rem;
		border-radius: 12px 12px 0 0;
	}

	.modal-header h3 {
		margin: 0;
		font-size: 1.25rem;
	}

	.modal-body {
		padding: 2rem;
	}

	.modal-body p {
		margin: 0 0 1rem 0;
		color: #333;
		line-height: 1.6;
		font-size: 1rem;
	}

	.modal-warning {
		background: #fff3cd;
		color: #856404;
		padding: 0.75rem;
		border-radius: 6px;
		border-left: 4px solid #ffc107;
		font-weight: 500;
		font-size: 0.95rem;
	}

	.modal-actions {
		padding: 0 2rem 2rem 2rem;
		display: flex;
		gap: 1rem;
		justify-content: flex-end;
	}

	.btn-modal-cancel,
	.btn-modal-confirm {
		padding: 0.75rem 1.5rem;
		border: none;
		border-radius: 6px;
		font-weight: 600;
		font-size: 1rem;
		cursor: pointer;
		transition: all 0.3s;
	}

	.btn-modal-cancel {
		background: #6c757d;
		color: white;
	}

	.btn-modal-cancel:hover {
		background: #5a6268;
		transform: translateY(-2px);
	}

	.btn-modal-confirm {
		background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
		color: white;
	}

	.btn-modal-confirm:hover {
		transform: translateY(-2px);
		box-shadow: 0 4px 12px rgba(245, 87, 108, 0.4);
	}

	.btn-snapshot:disabled, .btn-restore:disabled {
		opacity: 0.6;
		cursor: not-allowed;
	}

	.memento-info {
		background: white;
		padding: 1rem;
		border-radius: 6px;
		font-size: 0.9rem;
	}

	.memento-info p {
		margin: 0 0 0.5rem 0;
		font-weight: 600;
	}

	.memento-info ul {
		margin: 0.5rem 0 0 0;
		padding-left: 1.5rem;
	}

	.memento-info li {
		margin: 0.5rem 0;
		color: #555;
		line-height: 1.5;
	}
</style>
