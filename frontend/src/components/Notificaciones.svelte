<script>
	import { onMount, onDestroy } from 'svelte';
	
	let notificaciones = [];
	let mostrarMenu = false;
	let intervalo;
	const API_URL = 'http://127.0.0.1:8000/api';
	
	// Obtener notificaciones no leídas
	async function obtenerNotificaciones() {
		try {
			const response = await fetch(`${API_URL}/notificaciones/no_leidas/`);
			if (response.ok) {
				notificaciones = await response.json();
			}
		} catch (error) {
			console.error('Error al obtener notificaciones:', error);
		}
	}
	
	// Marcar notificación como leída
	async function marcarLeida(id) {
		try {
			const response = await fetch(`${API_URL}/notificaciones/${id}/marcar_leida/`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				}
			});
			
			if (response.ok) {
				// Eliminar de la lista local
				notificaciones = notificaciones.filter(n => n.id !== id);
			}
		} catch (error) {
			console.error('Error al marcar notificación:', error);
		}
	}
	
	// Marcar todas como leídas
	async function marcarTodasLeidas() {
		try {
			const response = await fetch(`${API_URL}/notificaciones/marcar_todas_leidas/`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				}
			});
			
			if (response.ok) {
				notificaciones = [];
				mostrarMenu = false;
			}
		} catch (error) {
			console.error('Error al marcar todas las notificaciones:', error);
		}
	}
	
	function toggleMenu() {
		mostrarMenu = !mostrarMenu;
	}
	
	function formatearFecha(fecha) {
		const date = new Date(fecha);
		const ahora = new Date();
		const diff = Math.floor((ahora - date) / 1000); // diferencia en segundos
		
		if (diff < 60) return 'Hace un momento';
		if (diff < 3600) return `Hace ${Math.floor(diff / 60)} min`;
		if (diff < 86400) return `Hace ${Math.floor(diff / 3600)} h`;
		return `Hace ${Math.floor(diff / 86400)} días`;
	}
	
	onMount(() => {
		// Obtener notificaciones al cargar
		obtenerNotificaciones();
		
		// Actualizar cada 5 segundos para demostración (antes era 30)
		intervalo = setInterval(obtenerNotificaciones, 5000);
	});
	
	onDestroy(() => {
		if (intervalo) {
			clearInterval(intervalo);
		}
	});
</script>

<div class="notificaciones-container">
	<button class="notif-btn" on:click={toggleMenu}>
		<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
			<path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
			<path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
		</svg>
		{#if notificaciones.length > 0}
			<span class="badge">{notificaciones.length}</span>
		{/if}
	</button>
	
	{#if mostrarMenu}
		<div class="notif-menu">
			<div class="notif-header">
				<h3>Notificaciones</h3>
				{#if notificaciones.length > 0}
					<button class="btn-small" on:click={marcarTodasLeidas}>
						Marcar todas como leídas
					</button>
				{/if}
			</div>
			
			<div class="notif-lista">
				{#if notificaciones.length === 0}
					<div class="notif-vacia">
						<p>No hay notificaciones nuevas</p>
					</div>
				{:else}
					{#each notificaciones as notif}
						<div class="notif-item">
							<div class="notif-content">
								<p class="notif-mensaje">{notif.mensaje}</p>
								<span class="notif-fecha">{formatearFecha(notif.fecha_generacion)}</span>
							</div>
							<button class="btn-cerrar" on:click={() => marcarLeida(notif.id)}>
								×
							</button>
						</div>
					{/each}
				{/if}
			</div>
		</div>
	{/if}
</div>

<style>
	.notificaciones-container {
		position: relative;
	}
	
	.notif-btn {
		position: relative;
		background: #fff;
		border: 1px solid #ddd;
		border-radius: 8px;
		padding: 8px 12px;
		cursor: pointer;
		display: flex;
		align-items: center;
		gap: 8px;
		transition: all 0.3s ease;
	}
	
	.notif-btn:hover {
		background: #f8f9fa;
		border-color: #2196F3;
	}
	
	.notif-btn svg {
		color: #666;
	}
	
	.badge {
		position: absolute;
		top: -5px;
		right: -5px;
		background: #f44336;
		color: white;
		border-radius: 50%;
		width: 20px;
		height: 20px;
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: 11px;
		font-weight: bold;
	}
	
	.notif-menu {
		position: absolute;
		top: calc(100% + 10px);
		right: 0;
		background: white;
		border-radius: 12px;
		box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
		width: 380px;
		max-height: 500px;
		display: flex;
		flex-direction: column;
		z-index: 1000;
	}
	
	.notif-header {
		padding: 16px;
		border-bottom: 1px solid #eee;
		display: flex;
		justify-content: space-between;
		align-items: center;
	}
	
	.notif-header h3 {
		margin: 0;
		font-size: 18px;
		color: #333;
	}
	
	.btn-small {
		background: #2196F3;
		color: white;
		border: none;
		padding: 6px 12px;
		border-radius: 6px;
		font-size: 12px;
		cursor: pointer;
		transition: background 0.3s ease;
	}
	
	.btn-small:hover {
		background: #1976D2;
	}
	
	.notif-lista {
		overflow-y: auto;
		max-height: 400px;
	}
	
	.notif-vacia {
		padding: 40px 20px;
		text-align: center;
		color: #999;
	}
	
	.notif-item {
		padding: 16px;
		border-bottom: 1px solid #f0f0f0;
		display: flex;
		gap: 12px;
		align-items: start;
		transition: background 0.2s ease;
	}
	
	.notif-item:hover {
		background: #f8f9fa;
	}
	
	.notif-item:last-child {
		border-bottom: none;
	}
	
	.notif-content {
		flex: 1;
	}
	
	.notif-mensaje {
		margin: 0 0 8px 0;
		color: #333;
		font-size: 14px;
		line-height: 1.4;
	}
	
	.notif-fecha {
		color: #999;
		font-size: 12px;
	}
	
	.btn-cerrar {
		background: none;
		border: none;
		font-size: 24px;
		color: #999;
		cursor: pointer;
		padding: 0;
		width: 24px;
		height: 24px;
		display: flex;
		align-items: center;
		justify-content: center;
		border-radius: 4px;
		transition: all 0.2s ease;
	}
	
	.btn-cerrar:hover {
		background: #f0f0f0;
		color: #333;
	}
</style>
