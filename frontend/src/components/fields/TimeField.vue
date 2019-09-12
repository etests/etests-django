<template>
  <v-menu
    lazy
    :close-on-content-click="false"
    v-model="menu"
    transition="scale-transition"
    offset-y
    full-width
    :nudge-right="40"
    max-width="290px"
    min-width="290px"
  >
    <v-text-field
      slot="activator"
      :label="label"
      :value="value"
      prepend-inner-icon="mdi-clock-outline"
      readonly
    ></v-text-field>
    <v-time-picker :value="value" @input="handleInput" scrollable>
      <template>
        <v-spacer></v-spacer>
        <v-btn flat color="primary" @click="menu = false">OK</v-btn>
      </template>
    </v-time-picker>
  </v-menu>
</template>
<script>
export default {
  props: ["value", "label"],
  data() {
    return {
      menu: false
    };
  },
  methods: {
    handleInput(value) {
      this.$emit("input", value);
    }
  }
};
</script>
