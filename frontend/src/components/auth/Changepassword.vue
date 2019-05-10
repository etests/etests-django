<template>
  <v-layout>
    <v-flex xs12 sm6 offset-sm3>
      <v-card :class="$style.registercard">
        <form :class="$style.registerform">
          <v-text-field
            :append-icon="showOldPassword ? 'visibility' : 'visibility_off'"
            :type="showOldPassword ? 'text' : 'password'"
            name="input-10-2"
            label="Old Password"
            value=""
            class="input-group--focused"
            @click:append="showOldPassword = !showOldPassword"
          ></v-text-field>

          <v-text-field
            :append-icon="showNewPassword ? 'visibility' : 'visibility_off'"
            :rules="[passwordRules.required, passwordRules.min]"
            :type="showNewPassword ? 'text' : 'password'"
            name="input-10-2"
            label="New Password"
            hint="At least 8 characters"
            value=""
            class="input-group--focused"
            @click:append="showNewPassword = !shownewPassword"
          ></v-text-field>
          <v-btn @click="submit">Change Password</v-btn>
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

  data: function() {
    return {
      showNewPassword: false,
      showOldPassword: false,
      oldPassword: "",
      newPassword: "",
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
