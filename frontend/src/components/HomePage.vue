<template>
  <div>
    <h1>{{ title }}</h1>
    <h2>{{ slogan }}</h2>
  </div>
</template>

<script>
export default {
  name: "HomePage",
  data() {
    return {
      title: "eTests",
      slogan: "an online testing platform"
    };
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1,
h2 {
  font-weight: normal;
}
</style>
