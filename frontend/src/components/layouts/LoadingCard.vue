<template>
  <v-flex xs12 sm6 md4 lg3>
    <v-card :class="[$style.loadingCard, 'elevation-1']"> </v-card>
  </v-flex>
</template>

<style module lang="stylus">
.loadingCard{
  width: 250px;
  height: 230px;
  width: 90%;
  border-radius: 8px;
  margin: 10px auto;
  animation: pulse 1.5s infinite ease-in-out;
}
@keyframes pulse {
    0% {
        background-color: rgba(245, 245, 245, 0.3);
    }
    50% {
        background-color: rgba(245, 245, 245, 0.9);
    }
    100% {
        background-color: rgba(245, 245, 245, 0.3);
    }
}
</style>
