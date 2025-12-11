<script>
	import Login from './components/Login.svelte';
	import Dashboard from './components/Dashboard.svelte';
	
	let encargado = null;

	function handleLogin(event) {
		encargado = event.detail;
	}

	function handleLogout() {
		encargado = null;
	}
</script>

<main>
	{#if !encargado}
		<Login on:login={handleLogin} />
	{:else}
		<Dashboard {encargado} on:logout={handleLogout} />
	{/if}
</main>

<style>
	main {
		padding: 0;
		margin: 0;
		width: 100%;
		min-height: 100vh;
		background: #f5f5f5;
	}
</style>