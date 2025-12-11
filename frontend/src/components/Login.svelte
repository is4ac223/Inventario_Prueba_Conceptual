<script>
	import { createEventDispatcher } from 'svelte';
	
	const dispatch = createEventDispatcher();
	const API_URL = 'http://127.0.0.1:8000/api';
	
	let nombreCompleto = '';
	let error = '';
	let loading = false;

	async function handleSubmit() {
		error = '';
		loading = true;
		
		try {
			const response = await fetch(`http://127.0.0.1:8000/api/login/`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({ nombre_completo: nombreCompleto })
			});
			
			const data = await response.json();
			
			if (response.ok) {
				dispatch('login', data.encargado);
			} else {
				error = data.error || 'Error al iniciar sesión';
			}
		} catch (err) {
			error = 'Error de conexión con el servidor';
			console.error(err);
		} finally {
			loading = false;
		}
	}
</script>

<div class="login-container">
	<div class="login-card">
		<h1>Sistema de Inventario</h1>
		<h2>Login - Encargado de Inventario</h2>
		
		<form on:submit|preventDefault={handleSubmit}>
			<div class="form-group">
				<label for="nombre">Nombre Completo:</label>
				<input 
					id="nombre"
					type="text" 
					bind:value={nombreCompleto}
					placeholder="Ingrese su nombre completo"
					required
					disabled={loading}
				/>
			</div>
			
			{#if error}
				<div class="error-message">{error}</div>
			{/if}
			
			<button type="submit" disabled={loading}>
				{loading ? 'Verificando...' : 'Ingresar'}
			</button>
		</form>
		
		<div class="info">
			<p><strong>Nota:</strong> Para demostración, ingrese el nombre completo registrado en el sistema.</p>
		</div>
	</div>
</div>

<style>
	.login-container {
		display: flex;
		justify-content: center;
		align-items: center;
		min-height: 100vh;
		background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
	}
	
	.login-card {
		background: white;
		padding: 2.5rem;
		border-radius: 12px;
		box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
		width: 100%;
		max-width: 400px;
	}
	
	h1 {
		color: #333;
		margin: 0 0 0.5rem 0;
		font-size: 1.8rem;
		text-align: center;
	}
	
	h2 {
		color: #666;
		margin: 0 0 2rem 0;
		font-size: 1.1rem;
		font-weight: 400;
		text-align: center;
	}
	
	.form-group {
		margin-bottom: 1.5rem;
	}
	
	label {
		display: block;
		margin-bottom: 0.5rem;
		color: #333;
		font-weight: 500;
	}
	
	input {
		width: 100%;
		padding: 0.75rem;
		border: 2px solid #e0e0e0;
		border-radius: 6px;
		font-size: 1rem;
		transition: border-color 0.3s;
		box-sizing: border-box;
	}
	
	input:focus {
		outline: none;
		border-color: #667eea;
	}
	
	input:disabled {
		background: #f5f5f5;
		cursor: not-allowed;
	}
	
	button {
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
	
	button:hover:not(:disabled) {
		transform: translateY(-2px);
		box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
	}
	
	button:disabled {
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
	
	.info {
		margin-top: 1.5rem;
		padding: 1rem;
		background: #f0f0f0;
		border-radius: 6px;
		font-size: 0.875rem;
		color: #666;
	}
	
	.info p {
		margin: 0;
	}
</style>
