<script>
	import { createEventDispatcher } from 'svelte';
	import RegistroMovimiento from './RegistroMovimiento.svelte';
	import VistaInventario from './VistaInventario.svelte';
	import GestionProductosTerminados from './GestionProductosTerminados.svelte';
	import GestionMateriasPrimas from './GestionMateriasPrimas.svelte';
	import Notificaciones from './Notificaciones.svelte';
	import EstadoInventario from './EstadoInventario.svelte';
	
	export let encargado;
	
	const dispatch = createEventDispatcher();
	
	let seccionActual = 'inventario'; // 'inventario', 'productos', 'materias', 'estado'
	let actualizarInventario = 0;

	function handleMovimientoRegistrado() {
		// Incrementar para forzar actualización del inventario
		actualizarInventario++;
	}

	function cambiarSeccion(seccion) {
		seccionActual = seccion;
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
				<Notificaciones />
				<span>👤 {encargado.nombre_completo}</span>
				<button class="btn-logout" on:click={logout}>Cerrar Sesión</button>
			</div>
		</div>
	</header>
	
	<!-- Navegación de secciones -->
	<nav class="nav-sections">
		<div class="nav-container">
			<button 
				class="nav-btn" 
				class:active={seccionActual === 'inventario'}
				on:click={() => cambiarSeccion('inventario')}
			>
				📦 Movimientos de Inventario
			</button>
			<button 
				class="nav-btn" 
				class:active={seccionActual === 'estado'}
				on:click={() => cambiarSeccion('estado')}
			>
				📊 Estado del Inventario
			</button>
			<button 
				class="nav-btn" 
				class:active={seccionActual === 'productos'}
				on:click={() => cambiarSeccion('productos')}
			>
				🏭 Gestionar Productos Terminados
			</button>
			<button 
				class="nav-btn" 
				class:active={seccionActual === 'materias'}
				on:click={() => cambiarSeccion('materias')}
			>
				🧪 Gestionar Materias Primas
			</button>
		</div>
	</nav>
	
	<div class="container">
		{#if seccionActual === 'inventario'}
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
		{:else if seccionActual === 'estado'}
			<div class="panel panel-full">
				<EstadoInventario />
			</div>
		{:else if seccionActual === 'productos'}
			<div class="panel panel-full">
				<GestionProductosTerminados />
			</div>
		{:else if seccionActual === 'materias'}
			<div class="panel panel-full">
				<GestionMateriasPrimas />
			</div>
		{/if}
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
	
	.nav-sections {
		background: white;
		border-bottom: 2px solid #e0e0e0;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
	}
	
	.nav-container {
		max-width: 1400px;
		margin: 0 auto;
		padding: 0 2rem;
		display: flex;
		gap: 0.5rem;
	}
	
	.nav-btn {
		padding: 1rem 1.5rem;
		background: none;
		border: none;
		border-bottom: 3px solid transparent;
		cursor: pointer;
		font-size: 1rem;
		font-weight: 500;
		color: #666;
		transition: all 0.3s;
		white-space: nowrap;
	}
	
	.nav-btn:hover {
		color: #667eea;
		background: rgba(102, 126, 234, 0.05);
	}
	
	.nav-btn.active {
		color: #667eea;
		border-bottom-color: #667eea;
		background: rgba(102, 126, 234, 0.05);
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
	
	.panel-full {
		grid-column: 1 / -1;
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
		
		.nav-container {
			flex-direction: column;
			gap: 0;
		}
		
		.nav-btn {
			text-align: left;
			border-bottom: 1px solid #e0e0e0;
			border-left: 3px solid transparent;
		}
		
		.nav-btn.active {
			border-bottom: 1px solid #e0e0e0;
			border-left-color: #667eea;
		}
	}
</style>
