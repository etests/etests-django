<template>
  <v-card class="elevation-2">
    <v-card-title>
      Instructions
    </v-card-title>
    <v-card-text>
        <v-btn @click="$router.push(`/test/${id}`)">Proceed</v-btn>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  data() {
    return {
      id: this.$route.params.id
    }
  },
}
</script>

<style module lang="stylus">

</style>
