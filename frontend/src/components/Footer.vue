<template>
  <v-footer dark height="20px" :app="fixed" :inset="fixed">
    <v-layout justify-center row wrap>
      <v-card flat class="flex white primary--text">
        <span>&copy;2019 &nbsp;<strong>eTests</strong></span>
        <v-btn v-for="icon in icons" :key="icon" color="primary" icon flat>
          <v-icon size="20px">{{ icon }}</v-icon>
        </v-btn>
      </v-card>
    </v-layout>
  </v-footer>
</template>

<script>
export default {
  props: {
    fixed: {
      required: false,
      default: false,
      type: Boolean
    }
  },
  data() {
    return {
      icons: [
        "mdi-facebook",
        "mdi-twitter",
        "mdi-google",
        "mdi-linkedin",
        "mdi-instagram"
      ]
    };
  }
};
</script>
