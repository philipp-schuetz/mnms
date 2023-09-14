<template>
	<header>
		<div><router-link to="/">Home</router-link></div>
		<div><router-link to="/admin">Admin</router-link></div>
		<div><router-link to="/groups">Groups</router-link></div>
	</header>
</template>

<style scoped>
header {
	display: grid;
	grid-template-columns: auto auto auto;
	background-color: #303030;
	height: 64px;
}
</style>
