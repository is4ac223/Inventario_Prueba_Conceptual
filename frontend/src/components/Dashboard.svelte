<script>
	import { createEventDispatcher } from 'svelte';
	import RegistroMovimiento from './RegistroMovimiento.svelte';
	import VistaInventario from './VistaInventario.svelte';
	
	export let encargado;
	
	const dispatch = createEventDispatcher();
	
	let actualizarInventario = 0;

	function handleMovimientoRegistrado() {
		// Incrementar para forzar actualización del inventario
		actualizarInventario++;
	}

	function logout() {
		dispatch('logout');
	}
</script>

<div class="dashboard">
	<header>
		<div class="header-content">
			<h1>Sistema de Gestión de Inventario</h1>
			<div class="user-info">
				<span>👤 {encargado.nombre_completo}</span>
				<button class="btn-logout" on:click={logout}>Cerrar Sesión</button>
			</div>
		</div>
	</header>
	
	<div class="container">
		<div class="panel panel-left">
			<h2>Registrar Movimiento</h2>
			<RegistroMovimiento 
				{encargado} 
				on:movimientoRegistrado={handleMovimientoRegistrado}
			/>
		</div>
		
		<div class="panel panel-right">
			<h2>Estado del Inventario</h2>
			<VistaInventario refresh={actualizarInventario} />
		</div>
	</div>
</div>

<style>
	.dashboard {
		min-height: 100vh;
		background: #f5f5f5;
	}
	
	header {
		background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
		color: white;
		padding: 1.5rem 2rem;
		box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
	}
	
	.header-content {
		max-width: 1400px;
		margin: 0 auto;
		display: flex;
		justify-content: space-between;
		align-items: center;
	}
	
	h1 {
		margin: 0;
		font-size: 1.75rem;
		font-weight: 600;
	}
	
	.user-info {
		display: flex;
		align-items: center;
		gap: 1rem;
	}
	
	.user-info span {
		font-size: 1rem;
	}
	
	.btn-logout {
		padding: 0.5rem 1rem;
		background: rgba(255, 255, 255, 0.2);
		color: white;
		border: 1px solid rgba(255, 255, 255, 0.3);
		border-radius: 6px;
		cursor: pointer;
		font-weight: 500;
		transition: background 0.3s;
	}
	
	.btn-logout:hover {
		background: rgba(255, 255, 255, 0.3);
	}
	
	.container {
		max-width: 1400px;
		margin: 2rem auto;
		padding: 0 2rem;
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 2rem;
	}
	
	.panel {
		background: white;
		border-radius: 12px;
		padding: 2rem;
		box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
	}
	
	.panel h2 {
		margin: 0 0 1.5rem 0;
		color: #333;
		font-size: 1.5rem;
		border-bottom: 2px solid #667eea;
		padding-bottom: 0.5rem;
	}
	
	@media (max-width: 1024px) {
		.container {
			grid-template-columns: 1fr;
		}
	}
</style>
