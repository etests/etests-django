<template>
  <v-layout>
    <v-flex xs12 sm6 offset-sm3>
      <v-card :class="$style.registercard">
        <form :class="$style.registerform">
          <v-text-field
            v-model="email"
            label="E-mail"
            required
            @input="$v.email.$touch()"
            @blur="$v.email.$touch()"
          ></v-text-field>
          <v-text-field
            :append-icon="showPassword ? 'visibility' : 'visibility_off'"
            :type="showPassword ? 'text' : 'password'"
            name="input-10-2"
            label="Password"
            value=""
            class="input-group--focused"
            @click:append="showPassword = !showPassword"
          ></v-text-field>
          <v-btn @click="submit">Login</v-btn>
        </form>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
import { validationMixin } from "vuelidate";
import { required, email } from "vuelidate/lib/validators";

export default {
  mixins: [validationMixin],

  validations: {
    email: { required, email }
  },

  data: function() {
    return {
      email: "",
      showPassword: false,
      password: "",
      passwordRules: {
        required: value => !!value || "Required.",
        min: v => v.length >= 8 || "Min 8 characters"
      }
    };
  },

  methods: {
    submit() {
      this.$v.$touch();
    }
  }
};
</script>

<style module lang="stylus">
@require '~@stylus/theme/colors';

.registercard{
  padding: 10px;
  margin :50px auto
}
.registerform {
  margin: 5px auto;
  width: 75%;
}
</style>
