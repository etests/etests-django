<template>
  <FlexibleCardLayout>
    <form class="px-5 py-5 mb-4">
      <v-text-field
        v-model="email"
        label="E-mail"
        required
        @input="$v.email.$touch()"
        @blur="$v.email.$touch()"
      ></v-text-field>
      <v-btn @click="submit">Submit</v-btn>
    </form>
  </FlexibleCardLayout>
</template>

<script>
import { validationMixin } from "vuelidate";
import { required, email } from "vuelidate/lib/validators";
import FlexibleCardLayout from "@/components/layouts/FlexibleCardLayout.vue";

export default {
  mixins: [validationMixin],

  validations: {
    email: { required, email }
  },

  data: function() {
    return {
      email: ""
    };
  },

  components: {
    FlexibleCardLayout
  },

  methods: {
    submit() {
      this.$v.$touch();
    }
  }
};
</script>
