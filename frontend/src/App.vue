<template>
  <div id="app">
    <img id="logo" src="./assets/logos/logo_plain.png">
    <router-view/>
  </div>
</template>

<script>
export default {
  name: "App"
};
</script>

<style>
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
#logo {
  width: 200px;
  height: 200px;
  image-rendering: align;
  border-radius: 8px;
  box-shadow: 2px 2px 20px #2c3e50;
}
</style>
